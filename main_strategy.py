import logging
import sys
# import  datetime
import time
from datetime import datetime, date, timedelta
import os
import pandas as pd
import numpy as np
from TA_Lib import SMA,HA
import xlwings as xw
from main_broker_api import All_Broker
import talib

pd.set_option('expand_frame_repr', False)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(levelname)-10s  %(message)s')
file_handler = logging.FileHandler('logs/MultiClient_MultiBroker_{}'.format(time.strftime('%Y-%m-%d.log')))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

nine_fifteen = datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
three_thirty = datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
nine_sixteen = datetime.now().replace(hour=9, minute=16, second=0, microsecond=0)
to_dt = datetime.now()
from_dt = to_dt - timedelta(days=5)
to_dt = to_dt.strftime('%Y-%m-%d')


def get_vwap(df:pd.DataFrame):
    try:
        print(df.columns)
        df['time'] = df.index
        columns_df = list(df.columns)
        columns_df.append('vwap')
        df['Quantity_Rolling_Sum'] = df.groupby(df['time'].dt.date)['volume'].cumsum()
        df['PriceXVolume'] = (df['HA_close'] + df['HA_high']+df['HA_low'])/3 * df['volume']
        df['PriceXVolumeCUMSUM'] = df.groupby(df['time'].dt.date)['PriceXVolume'].cumsum()
        df['vwap'] = df['PriceXVolumeCUMSUM'] / df['Quantity_Rolling_Sum']
        df = df[columns_df]
        return df
    except:
        print(sys.exc_info())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def fix_values(value, tick_size):
    return round(int(value / tick_size) * tick_size, len(str(tick_size)))


def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)

    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute Average True Range (ATR)

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])

    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = 'ATR_' + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not 'TR' in df.columns:
        df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
        df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

        df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

        df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df, 'TR', atr, period, alpha=True)

    return df


def SuperTrend(df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute SuperTrend

    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])

    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """
    try:
        ATR(df, period, ohlc=ohlc)
        atr = 'ATR_' + str(period)
        st = 'ST_' + str(period) + '_' + str(multiplier)
        stx = 'STX_' + str(period) + '_' + str(multiplier)

        """
        SuperTrend Algorithm :

            BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
            BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR

            FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                                THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
            FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                                THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

            SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                            Current FINAL UPPERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                    Current FINAL LOWERBAND
                                ELSE
                                    IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                        Current FINAL UPPERBAND
        """

        # Compute basic upper and lower bands
        df['basic_ub'] = (df[ohlc[3]] + df[ohlc[3]]) / 2 + multiplier * df[atr]
        df['basic_lb'] = (df[ohlc[3]] + df[ohlc[3]]) / 2 - multiplier * df[atr]

        # Compute final upper and lower bands
        df['final_ub'] = 0.00
        df['final_lb'] = 0.00

        for i in range(period, len(df)):
            df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[
                i - 1] or df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[
                i - 1]
            df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[
                i - 1] or df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[
                i - 1]

        # Set the Supertrend value
        df[st] = 0.00
        for i in range(period, len(df)):
            df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and \
                                                     df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and \
                                         df[ohlc[3]].iat[i] > df['final_ub'].iat[i] else \
                    df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and \
                                             df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
                        df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and \
                                                 df[ohlc[3]].iat[i] < df['final_lb'].iat[i] else 0.00

            # Mark the trend direction up/down
        df['SUPERTREND'] = np.where((df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)

        # Remove basic and final bands from the columns
        df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'], inplace=True, axis=1)

        df.fillna(0, inplace=True)
        return df['SUPERTREND']
    except:
        print(sys.exc_info())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def do_assertion(name,variable):
    assert variable is not None,f"Variable {name} is None"

def add_rows(old_instruments_df_dict,main_broker,instrument_sheet,instruments_df,users_df_dict): # TODO Add this in main Code for adding Rows
    instruments_df = instrument_sheet.range('A1').options(pd.DataFrame, header=1, index=False,
                                                          expand='table').value

    instruments_df['running_trend'] = None
    instruments_df['multiplier'] = None
    instruments_df['entry_price'] = None
    instruments_df['entry_time'] = None
    instruments_df['multiplier'] = None
    instruments_df['exit_price'] = None
    instruments_df['exit_time'] = None
    instruments_df['status'] = 0
    instruments_df['target_price'] = None
    instruments_df['sl_price'] = None
    instruments_df['Row_Type'] = 'T'
    instruments_df['profit'] = None
    instruments_df['Trend'] = None
    instruments_df['run_done'] = 0
    instruments_df['vwap_last'] = 0
    instruments_df['quantity'] = 1
    instruments_df['close_positions'] = 0

    instruments_df_dict = instruments_df.to_dict('index')
    for each_instrument in instruments_df_dict:
        this_instrument = instruments_df_dict[each_instrument]
        this_instrument['entry_order_ids'] = {x: {'order_id': None, 'order_status': None, 'broker': users_df_dict[x]['broker']} for x in users_df_dict}
        this_instrument['exit_order_ids'] = {x: {'order_id': None, 'order_status': None, 'broker': users_df_dict[x]['broker']} for x in users_df_dict}

        row = All_Broker.All_Broker.instrument_df[(All_Broker.All_Broker.instrument_df['tradingsymbol'] == this_instrument['instrument'])]
        this_instrument['instrument_row'] = row
        this_instrument['instrument_token'] = int(row.iloc[-1]['instrument_token'])
        this_instrument['tradingsymbol'] = row.iloc[-1]['tradingsymbol']
        this_instrument['lot_size'] = int(row.iloc[-1]['lot_size'])
        this_instrument['order'] = None
        this_instrument['tick_size'] = row.iloc[-1]['tick_size']
        this_instrument['quantity'] = this_instrument['quantity'] * this_instrument['lot_size']
        this_instrument['exchange_token'] = row.iloc[-1]['exchange_token']
    instrument_list = [instruments_df_dict[x]['instrument_token'] for x in instruments_df_dict]

    main_broker.instrument_list = instrument_list

    for each_instrument in instrument_list:
        if each_instrument not in main_broker.latest_ltp:
            main_broker.latest_ltp[each_instrument] = {'ltp': None}
    main_broker.subscribe_instrument(main_broker.instrument_list)

    for each_key in instruments_df_dict:
        if each_key not in old_instruments_df_dict:
            old_instruments_df_dict[each_key] = dict(instruments_df_dict[each_key])

    return old_instruments_df_dict

def main():
    # Variables
    paper_trade = 0
    users_df_dict = None
    main_broker = None
    users_df = None
    instruments_df = None
    # instruments_df_dict = None

    #Workbook
    wb = xw.Book('multi.xls')
    # sheet
    live_pnl_sheet = wb.sheets['LIVE PNL']

    ## DO login for All users
    process_name = 'User Login Process'
    try:
        logger.info(f"Doing {process_name}")
        user_sheet = wb.sheets['User Details']
        users_df = user_sheet.range('A1').options(pd.DataFrame,header=1,index=False,
                                       expand='table').value
        users_df.index = users_df['Name']
        users_df = users_df.head(1)  # todo: change this
        users_df['broker'] = None
        users_df_dict = users_df.to_dict('index')
        for each_key in users_df_dict:
            try:
                this_user = users_df_dict[each_key]
                this_user['broker'] = All_Broker.All_Broker(**this_user)
                # print("Hi")
            except:
                logger.info(f"Error in Logging in for Name : {each_key} Error : {sys.exc_info()}")
    except:
        logger.info(f"Error in {process_name}. Error : {sys.exc_info()} ")


    process_name = 'Setting Main Broker'
    try:
        logger.info(f"{process_name} for Data Feed")
        main_broker = users_df_dict[list(users_df_dict.keys())[0]]['broker']##### Main Broker for Getting LTPS and Historic Data
        assert main_broker.broker_name in ['ZERODHA','IIFL'],f"Main Broker for Data Feed is not ZERODHA or IIFL"
    except:
        logger.info(f"Error in {process_name}")

    ## Remove this Later

    # del users_df_dict['c']

    process_name = 'Get All Instruments to Trade'
    update_rows = 0
    instruments_df_dict = dict()
    instrument_sheet = wb.sheets['Instrument details']

    try:
        instruments_df_dict = add_rows(instruments_df_dict, main_broker, instrument_sheet, instruments_df, users_df_dict)# TODO Add this in main Code for adding Rows

    except:
        logger.info(f"Error in {process_name}. Error : {sys.exc_info()} ")

    ## Running Strategy Now for All the Instruments
    main_broker.get_live_ticks()
    time.sleep(5)
    logger.info(f"Starting Strategy")
    final_df = pd.DataFrame(columns=list(instruments_df.columns)+['ltp','tradingsymbol'])
    # main_broker : All_Broker.All_Broker
    del users_df_dict[0]

    while True:
        if update_rows == 1:# TODO Add this in main Code for adding Rows
            update_rows = 0# TODO Add this in main Code for adding Rows
            instruments_df_dict = add_rows(instruments_df_dict, main_broker, instrument_sheet, instruments_df, users_df_dict)  # TODO Add this in main Code for adding Rows

        if datetime.now() < nine_sixteen:
            continue

        final_df = final_df[['tradingsymbol', 'exchange', 'quantity', 'timeframe', 'multiplier', 'entry_price', 'entry_time', 'exit_price', 'exit_time'
            , 'target_price', 'sl_price', 'Row_Type', 'profit', 'ltp']]
        final_df['Trend'] = np.where(final_df['multiplier'] == 1, 'BUY', 'SELL')

        final_all_user_df = pd.DataFrame()
        for each_user in users_df_dict:
            try:
                this_user = users_df_dict[each_user]
                if this_user['broker'] is None:
                    continue
                no_of_lots = this_user['No of Lots']
                final_df_temp = final_df.copy(deep=True)
                final_df_temp['quantity'] = final_df_temp['quantity'] * no_of_lots
                final_df_temp['profit'] = (final_df_temp['ltp'] - final_df_temp['entry_price'])*final_df_temp['quantity']*final_df_temp['multiplier']
                final_df_temp['user_id'] = this_user.all_data_kwargs['accountUserName']
                final_all_user_df = final_all_user_df.append(final_df_temp,ignore_index=True)
            except:
                logger.info(f"{sys.exc_info()}")

        final_all_user_df.to_csv("PNLATRTS_All_User.csv")# TODO PNL of all users by the lot executed by the user

        order_book_dict = dict()
        for each_user in users_df_dict:
            try:
                this_user = users_df_dict[each_user]
                if this_user['broker'] is None:
                    continue
                order_book = this_user.get_order_book()
                order_book['username'] = this_user.all_data_kwargs['accountUserName']
                if  this_user.broker_name in order_book_dict:
                    order_book_dict[this_user.broker_name] = order_book[this_user.broker_name].append(order_book,ignore_index=True)
                else:
                    order_book_dict[this_user.broker_name] = order_book
            except:
                logger.info(f"{sys.exc_info()}")

        for each_key in order_book_dict:
            try:
                order_book_dict[each_key] = list(order_book_dict[each_key].to_dict('index').values())
            except:
                logger.info(f"Error in Creating Order Book {sys.exc_info()}")


        #TODO order_book_dict # This contains Orderbook of all the clients


        curr_date = datetime.now()
        for each_key in instruments_df_dict:
            process_name = 'Main Strategy'
            try:
                this_instrument = instruments_df_dict[each_key]
                ltp = main_broker.latest_ltp[this_instrument['instrument_token']]['ltp']

                if (int((curr_date - nine_fifteen).seconds / 60) % this_instrument['timeframe'] > 0) or (int((curr_date - nine_fifteen).seconds / 60) % this_instrument['timeframe'] == 0 and curr_date.second > 30) and this_instrument['run_done'] == 1:
                    this_instrument['run_done'] = 0

                if int((curr_date - nine_fifteen).seconds / 60) % this_instrument['timeframe'] == 0 and curr_date.second <= 30 and this_instrument['run_done'] == 0 and this_instrument['status'] == 0:
                    this_instrument['run_done'] = 1
                    logger.info(f"Running the {process_name} for {this_instrument['tradingsymbol']}")
                    df = main_broker.get_data(this_instrument['instrument_token'], str(int(this_instrument['timeframe'])), 'minute', from_dt, to_dt)
                    df = df[df.index < datetime.now().replace(microsecond=0, second=0)]
                    time_df_col = df.index
                    df = HA(df, ohlc=['open', 'high', 'low', 'close'])
                    df.index = time_df_col
                    df = get_vwap(df)
                    df['SUPERTREND'] = SuperTrend(df, this_instrument['ATR TS Period'], this_instrument['ATR TS Multiplier'], ohlc=['HA_open', 'HA_high', 'HA_low', 'HA_close'])
                    this_instrument['vwap_last'] = df['vwap'].tail(2).head(1).values[0]
                    vwap = df['vwap'].tail(1).values[0]


                    atr_trend_bullish = 0
                    atr_trend_bearish = 0

                    if this_instrument['ATRTS'] == 'YES':

                        if this_instrument['atrts_signal'] == 'new':
                            atr_trend_bearish = 1 if ((df['SUPERTREND'].tail(1).head(1).values[0] == 'down') & (df['SUPERTREND'].tail(2).head(1).values[0] == 'up'))   else 0
                            atr_trend_bullish = 1 if ((df['SUPERTREND'].tail(1).head(1).values[0] == 'up') & (df['SUPERTREND'].tail(2).head(1).values[0] == 'down'))  else 0
                        if this_instrument['atrts_signal'] == 'existing':
                            atr_trend_bearish = 1 if ((df['SUPERTREND'].tail(1).head(1).values[0] == 'down'))   else 0
                            atr_trend_bullish = 1 if ((df['SUPERTREND'].tail(1).head(1).values[0] == 'up'))  else 0

                    else:
                        atr_trend_bullish = 1
                        atr_trend_bearish = 1


                    vwap_trend_bullish = 0
                    vwap_trend_bearish = 0

                    logger.info(f"Previous Vwap : {this_instrument['vwap_last']} Now Vwap : {vwap}")
                    if this_instrument['vwap'] == 'YES' and this_instrument['vwap_last'] != 0:

                        if this_instrument['vwap_signal'] == 'new':
                            vwap_trend_bullish = 1 if (df['HA_close'].tail(1).head(1).values[0] > vwap) and (df['HA_close'].tail(2).head(1).values[0] < this_instrument['vwap_last'])  else 0
                            vwap_trend_bearish = 1 if (df['HA_close'].tail(1).head(1).values[0] < vwap) and (df['HA_close'].tail(2).head(1).values[0] > this_instrument['vwap_last'])  else 0

                        if this_instrument['vwap_signal'] == 'existing':
                            vwap_trend_bullish = 1 if (df['HA_close'].tail(1).head(1).values[0] > vwap)  else 0
                            vwap_trend_bearish = 1 if (df['HA_close'].tail(1).head(1).values[0] < vwap)  else 0
                    else:
                        vwap_trend_bullish = 1
                        vwap_trend_bearish = 1

                    this_instrument['vwap_last'] = vwap

                    ma_trend_bullish = 0
                    ma_trend_bearish = 0
                    if this_instrument['moving_average'] == 'YES':
                        df['moving_average'] = talib.ma(df['HA_close'],timeperiod= int(this_instrument['moving_average_period']))
                        row_name = 'moving_average'
                        if this_instrument['moving_average_signal'] == 'new':
                            ma_trend_bullish = 1 if (df[row_name].tail(1).values[0] < df['HA_close'].tail(1).values[0]) and (df[row_name].tail(2).head(1).values[0] >= df['HA_close'].tail(2).head(1).values[0]) else 0
                            ma_trend_bearish = 1 if (df[row_name].tail(1).values[0] >= df['HA_close'].tail(1).values[0]) and (df[row_name].tail(2).head(1).values[0] < df['HA_close'].tail(2).head(1).values[0]) else 0

                        # if this_instrument['dc_signal'] == 'existing':
                        #     ma_trend_bullish = 1 if (df[row_name].tail(1).values[0] < df['HA_close'].tail(1).values[0])  else 0
                        #     ma_trend_bearish = 1 if (df[row_name].tail(1).values[0] >= df['HA_close'].tail(1).values[0])  else 0
                    else:
                        ma_trend_bullish = 1
                        ma_trend_bearish = 1


                    if this_instrument['use_priceba'] == 'YES':
                        price_above_trend_bullish = 1 if ltp > this_instrument['buy_above'] else 0
                        price_above_trend_bearish = 1
                    else:
                        price_above_trend_bearish = 1
                        price_above_trend_bullish = 1


                    if this_instrument['use_pricesb'] == 'YES':
                        price_trend_bullish = 1 if ltp < this_instrument['sell_below'] else 0
                        price_trend_bearish = 1
                    else:
                        price_trend_bearish = 1
                        price_trend_bullish = 1



                    if  price_above_trend_bullish and price_trend_bullish and ma_trend_bullish and vwap_trend_bullish and atr_trend_bullish and  this_instrument['multiplier'] != 1 and this_instrument['transaction_type'] == 'BUY':
                        logger.info(f" In Buy Loop. for {this_instrument['tradingsymbol']}")
                        logger.info(f" Buy Signal has been Activated for {this_instrument['tradingsymbol']}")
                        this_instrument['status'] = 1
                        this_instrument['multiplier'] = 1

                        this_instrument['entry_price'] = fix_values(df['HA_close'].tail(1).values[0] * (1 - this_instrument['buy_ltp_percent'] / 100), this_instrument['tick_size'])
                        this_instrument['entry_time'] = datetime.now()
                        if this_instrument['target_type'].lower() == 'percentage':
                            this_instrument['target_price'] = fix_values(this_instrument['entry_price'] * (1 + this_instrument['target'] / 100), this_instrument['tick_size'])
                        elif this_instrument['target_type'].lower() == 'value':
                            this_instrument['target_price'] = fix_values(this_instrument['entry_price'] + this_instrument['target'], this_instrument['tick_size'])

                        if this_instrument['stoploss_type'].lower() == 'percentage':
                            this_instrument['sl_price'] = fix_values(this_instrument['entry_price']* (1 - this_instrument['stoploss'] / 100), this_instrument['tick_size'])

                        elif this_instrument['stoploss_type'].lower() == 'VALUE':
                            this_instrument['sl_price'] = fix_values(this_instrument['entry_price'] - this_instrument['multiplier'] * this_instrument['stoploss_value'], this_instrument['tick_size'])

                        if paper_trade == 0:
                            order = {'variety' :'regular',
                                    'exchange' : this_instrument['exchange'],
                                    'tradingsymbol' : this_instrument['tradingsymbol'],
                                    'quantity':int(this_instrument['quantity']),
                                     'product' : this_instrument['product_type'],
                                    'transaction_type' : this_instrument['transaction_type'],
                                    'order_type' :this_instrument['order_type'],
                                    'price': this_instrument['entry_price'] ,
                                    'validity': 'DAY',
                                    'disclosed_quantity' : None ,
                                    'trigger_price' :None ,
                                    'squareoff' : None ,
                                    'stoploss' : None ,
                                    'trailing_stoploss' : None,
                                    'tag' : None }
                            this_instrument['order'] = order
                            for each_user in users_df_dict:
                                try:
                                    this_user = users_df_dict[each_user]
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity']*this_user['No of Lots'])
                                    order_id,message =  this_user['broker'].place_order(**new_order)
                                    this_instrument['entry_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")
                                except:
                                    logger.info(f"Error in Sell Order Placement for {this_user['Name']} Error {sys.exc_info()}")



                        logger.info(f" Instrument_Details : {this_instrument}")


                    elif price_above_trend_bearish and price_trend_bearish and ma_trend_bearish and vwap_trend_bearish and atr_trend_bearish and this_instrument['multiplier']!= -1 and this_instrument['transaction_type'] =='SELL':
                        logger.info(f" In Sell Loop. for {this_instrument['tradingsymbol']}")
                        logger.info(f" Sell Signal has been Activated for {this_instrument['tradingsymbol']}")
                        this_instrument['status'] = 1
                        this_instrument['multiplier'] = 1

                        this_instrument['entry_price'] = fix_values(df['HA_close'].tail(1).values[0] * (1 - this_instrument['sell_ltp_percent'] / 100), this_instrument['tick_size'])
                        this_instrument['entry_time'] = datetime.now()
                        if this_instrument['order_type'] == 'MARKET':
                            this_instrument['entry_price'] = ltp


                        if this_instrument['target_type'].lower() == 'percentage':
                            this_instrument['target_price'] = fix_values(this_instrument['entry_price'] * (1 - this_instrument['target'] / 100), this_instrument['tick_size'])
                        elif this_instrument['target_type'].lower() == 'value':
                            this_instrument['target_price'] = fix_values(this_instrument['entry_price'] - this_instrument['target'], this_instrument['tick_size'])

                        if this_instrument['stoploss_type'].lower() == 'percentage':
                            this_instrument['sl_price'] = fix_values(this_instrument['entry_price'] * (1 + this_instrument['stoploss'] / 100), this_instrument['tick_size'])

                        elif this_instrument['stoploss_type'].lower() == 'VALUE':
                            this_instrument['sl_price'] = fix_values(this_instrument['entry_price'] - this_instrument['multiplier'] * this_instrument['stoploss_value'], this_instrument['tick_size'])


                        if paper_trade == 0:
                            order = {'variety': 'regular',
                                     'exchange': this_instrument['exchange'],
                                     'tradingsymbol': this_instrument['tradingsymbol'],
                                     'quantity': int(this_instrument['quantity']),
                                     'product': this_instrument['product_type'],
                                     'transaction_type': this_instrument['transaction_type'],
                                     'order_type': this_instrument['order_type'],
                                     'price': ltp,
                                     'validity': 'DAY',
                                     'disclosed_quantity': None,
                                     'trigger_price': None,
                                     'squareoff': None,
                                     'stoploss': None,
                                     'trailing_stoploss': None,
                                     'tag': None}

                            this_instrument['order'] = order
                            for each_user in users_df_dict:
                                try:
                                    this_user = users_df_dict[each_user]
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity']*this_user['No of Lots'])
                                    order_id,message =  this_user['broker'].place_order(**new_order)
                                    this_instrument['entry_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Sell Order Placed for {each_user} Order_id {order_id}")
                                except:
                                    logger.info(f"Error in Sell Order Placement for {this_user['Name']} Error {sys.exc_info()}")

                        logger.info(f" Instrument_Details : {this_instrument}")


                if this_instrument['status'] == 1:
                    if paper_trade == 1:  #

                        if ltp * this_instrument['multiplier'] <= this_instrument['entry_price'] * this_instrument['multiplier']:
                            logger.info(f"Entry has been taken for {this_instrument['tradingsymbol']}")
                            this_instrument['entry_time'] = datetime.now()
                            this_instrument['status'] = 2
                            continue

                        if datetime.now() > this_instrument['entry_time'] + timedelta(minutes=int(this_instrument['wait_time'])):
                            logger.info(f" Cancelling the Placed Order for {this_instrument['tradingsymbol']}")
                            this_instrument['Row_Type'] = 'T'
                            this_instrument['multiplier'] = None
                            this_instrument['entry_price'] = None
                            this_instrument['entry_time'] = None
                            this_instrument['multiplier'] = None
                            this_instrument['exit_price'] = None
                            this_instrument['exit_time'] = None
                            this_instrument['status'] = 0
                            this_instrument['entry_order_id'] = None
                            this_instrument['target_price'] = None
                            this_instrument['sl_price'] = None
                            this_instrument['sl_order_id'] = None
                            this_instrument['target_order_id'] = None
                            this_instrument['Row_Type'] = 'T'
                            continue

                    if paper_trade == 0:
                        if ltp * this_instrument['multiplier'] <= this_instrument['entry_price'] * this_instrument['multiplier']:
                            for each_user in this_instrument['entry_order_ids']:
                                this_user_order_details = this_instrument['entry_order_ids'][each_user]
                                broker = this_user_order_details['broker']
                                order_id = this_user_order_details['order_id']
                                main_order = this_instrument['order']
                                order_status,status_message = broker.get_order_status(order_id=order_id)
                                this_user_order_details['order_status'] = order_status
                                if order_status == 'COMPLETE':
                                    continue
                                elif order_status == 'REJECTED':
                                    logger.info(f"Order Rejected for {each_user} having Order ID : {order_id}")
                                    continue
                                else:

                                    order = this_instrument['order']
                                    order['order_type'] = 'MARKET'
                                    order['price'] = None
                                    broker.cancel_order(order_id = order_id)
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity'] * this_user['No of Lots'])
                                    order_id, message = this_user['broker'].place_order(**new_order)
                                    this_instrument['entry_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")



                            logger.info(f" Entry has been taken for {this_instrument['tradingsymbol']} ")
                            this_instrument['entry_time'] = datetime.now()
                            this_instrument['status'] = 2
                            # Place SL Order
                            order = {'variety': 'regular',
                                     'exchange': this_instrument['exchange'],
                                     'tradingsymbol': this_instrument['tradingsymbol'],
                                     'quantity': int(this_instrument['quantity']),
                                     'product': this_instrument['product_type'],
                                     'transaction_type': 'SELL' if this_instrument['transaction_type'] is 'BUY' else 'SELL',
                                     'order_type': 'SL',
                                     'price': this_instrument['sl_price'],
                                     'validity': 'DAY',
                                     'disclosed_quantity': None,
                                     'trigger_price': this_instrument['sl_price'] - this_instrument['tick_size'] if this_instrument['transaction_type'] is 'BUY' else this_instrument['sl_price'] + 1*this_instrument['tick_size'],
                                     'squareoff': None,
                                     'stoploss': None,
                                     'trailing_stoploss': None,
                                     'tag': None}

                            for each_user in users_df_dict:
                                try:
                                    this_user = users_df_dict[each_user]
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity']*this_user['No of Lots'])
                                    order_id,message =  this_user['broker'].place_order(**new_order)
                                    this_instrument['exit_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")
                                except:
                                    logger.info(f"Error in SL Order Placement for {this_user['Name']} Error {sys.exc_info()}")

                            continue

                if this_instrument['status'] == 2:  # Order Placed was executed
                    this_instrument['ltp'] = ltp
                    this_instrument['profit'] = (ltp - this_instrument['entry_price']) * this_instrument['multiplier'] * this_instrument['quantity'] * this_instrument['lot_size']
                    final_df = final_df[final_df['Row_Type']!='T']
                    this_instrument['Row_Type'] = 'T'
                    final_df = final_df.append(this_instrument, ignore_index=True)

                        # logger.info(f"{ltp} {this_instrument['multiplier']} {this_instrument['target_price']} {this_instrument['sl_price']}")
                    if ltp * this_instrument['multiplier'] >= this_instrument['target_price'] * this_instrument['multiplier'] :
                        logger.info(f"Target has been Hit for {this_instrument['tradingsymbol']}")
                        this_instrument['exit_time'] = datetime.now()
                        this_instrument['exit_price'] = ltp
                        this_instrument['status'] = 0
                        this_instrument['vwap_signal'] = 'new'  #TODO Tuhin Add this in main code
                        this_instrument['atrts_signal'] = 'new' #TODO Tuhin Add this main code
                        this_instrument['moving_average_signal'] = 'new' #TODO Tuhin Add this main code
                        #Cancel Pending SL Order and Placing a Market Order
                        for each_user in users_df_dict:
                            try:
                                this_user = users_df_dict[each_user]
                                order_id = this_instrument['exit_order_ids'][each_user]['order_id']
                                order_status,message = this_user['broker'].get_order_status(order_id)
                                this_instrument['exit_order_ids'][each_user]['order_status'] = order_status
                                if order_status == 'PENDING':
                                    this_user['broker'].cancel_order(order_id)
                                    order = {'variety': 'regular',
                                             'exchange': this_instrument['exchange'],
                                             'tradingsymbol': this_instrument['tradingsymbol'],
                                             'quantity': int(this_instrument['quantity']),
                                             'product': this_instrument['product_type'],
                                             'transaction_type': 'SELL' if this_instrument['transaction_type'] is 'BUY' else 'SELL',
                                             'order_type': 'MARKET',
                                             'price': None,
                                             'validity': 'DAY',
                                             'disclosed_quantity': None,
                                             'trigger_price': None,
                                             'squareoff': None,
                                             'stoploss': None,
                                             'trailing_stoploss': None,
                                             'tag': None}
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity'] * this_user['No of Lots'])
                                    order_id, message = this_user['broker'].place_order(**new_order)
                                    this_instrument['exit_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")
                            except:
                                logger.info(f"Error in Closing Order Placement for {this_user['Name']} Error {sys.exc_info()}")

                        # final_df = final_df[final_df['Row_Type']!='T']
                        this_instrument['Row_Type'] = 'F'
                        final_df = final_df.append(this_instrument, ignore_index=True)

                        this_instrument['Row_Type'] = 'T'
                        this_instrument['multiplier'] = None
                        this_instrument['entry_price'] = None
                        this_instrument['entry_time'] = None
                        this_instrument['multiplier'] = None
                        this_instrument['exit_price'] = None
                        this_instrument['exit_time'] = None
                        this_instrument['status'] = 0
                        this_instrument['entry_order_id'] = None
                        this_instrument['target_price'] = None
                        this_instrument['sl_price'] = None
                        this_instrument['sl_order_id'] = None
                        this_instrument['target_order_id'] = None
                        this_instrument['Row_Type'] = 'T'



                    elif ltp * this_instrument['multiplier'] <= this_instrument['sl_price'] * this_instrument['multiplier'] :

                        logger.info(f"Stoploss has been Hit for {this_instrument['tradingsymbol']}")
                        this_instrument['exit_time'] = datetime.now()
                        this_instrument['exit_price'] = ltp
                        this_instrument['status'] = 0
                        this_instrument['vwap_signal'] = 'new'  #TODO Tuhin Add this in main code
                        this_instrument['atrts_signal'] = 'new' #TODO Tuhin Add this main code
                        this_instrument['moving_average_signal'] = 'new' #TODO Tuhin Add this main code

                        # Cancel Pending SL Order and Placing a Market Order
                        for each_user in users_df_dict:
                            try:
                                this_user = users_df_dict[each_user]
                                order_id = this_instrument['exit_order_ids'][each_user]['order_id']
                                order_status,message = this_user['broker'].get_order_status(order_id)
                                this_instrument['exit_order_ids'][each_user]['order_status'] = order_status
                                time.sleep(1)
                                if order_status == 'PENDING':
                                    this_user['broker'].cancel_order(order_id)
                                    time.sleep(1)
                                    order = {'variety': 'regular',
                                             'exchange': this_instrument['exchange'],
                                             'tradingsymbol': this_instrument['tradingsymbol'],
                                             'quantity': int(this_instrument['quantity']),
                                             'product': this_instrument['product_type'],
                                             'transaction_type': 'SELL' if this_instrument['transaction_type'] is 'BUY' else 'SELL',
                                             'order_type': 'MARKET',
                                             'price': None,
                                             'validity': 'DAY',
                                             'disclosed_quantity': None,
                                             'trigger_price': None,
                                             'squareoff': None,
                                             'stoploss': None,
                                             'trailing_stoploss': None,
                                             'tag': None}
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity'] * this_user['No of Lots'])
                                    order_id, message = this_user['broker'].place_order(**new_order)
                                    this_instrument['exit_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")
                            except:
                                logger.info(f"Error in Closing Order Placement for {this_user['Name']} Error {sys.exc_info()}")

                        # final_df = final_df[final_df['Row_Type'] != 'T']
                        this_instrument['Row_Type'] = 'F'
                        final_df = final_df.append(this_instrument, ignore_index=True)

                        this_instrument['Row_Type'] = 'T'
                        this_instrument['multiplier'] = None
                        this_instrument['entry_price'] = None
                        this_instrument['entry_time'] = None
                        this_instrument['multiplier'] = None
                        this_instrument['exit_price'] = None
                        this_instrument['exit_time'] = None
                        this_instrument['status'] = 0
                        this_instrument['entry_order_id'] = None
                        this_instrument['target_price'] = None
                        this_instrument['sl_price'] = None
                        this_instrument['sl_order_id'] = None
                        this_instrument['target_order_id'] = None
                        this_instrument['Row_Type'] = 'T'


                    if this_instrument['close_positions'] == 1:

                        this_instrument['exit_time'] = datetime.now()
                        this_instrument['exit_price'] = ltp
                        this_instrument['status'] = 0
                        this_instrument['vwap_signal'] = 'new'  #TODO Tuhin Add this in main code
                        this_instrument['atrts_signal'] = 'new' #TODO Tuhin Add this main code
                        this_instrument['moving_average_signal'] = 'new' #TODO Tuhin Add this main code
                        # Cancel Pending SL Order and Placing a Market Order
                        for each_user in users_df_dict:
                            try:
                                this_user = users_df_dict[each_user]
                                order_id = this_instrument['exit_order_ids'][each_user]['order_id']
                                order_status = this_user['broker'].get_order_status(order_id)
                                this_instrument['exit_order_ids'][each_user]['order_status'] = order_status
                                if order_status == 'PENDING':
                                    this_user['broker'].cancel_order(order_id)
                                    order = {'variety': 'regular',
                                             'exchange': this_instrument['exchange'],
                                             'tradingsymbol': this_instrument['tradingsymbol'],
                                             'quantity': int(this_instrument['quantity']),
                                             'product': this_instrument['product_type'],
                                             'transaction_type': 'SELL' if this_instrument['transaction_type'] is 'BUY' else 'SELL',
                                             'order_type': 'MARKET',
                                             'price': None,
                                             'validity': 'DAY',
                                             'disclosed_quantity': None,
                                             'trigger_price': None,
                                             'squareoff': None,
                                             'stoploss': None,
                                             'trailing_stoploss': None,
                                             'tag': None}
                                    new_order = dict(order)
                                    new_order['quantity'] = int(new_order['quantity'] * this_user['No of Lots'])
                                    order_id, message = this_user['broker'].place_order(**new_order)
                                    this_instrument['exit_order_ids'][each_user]['order_id'] = order_id
                                    logger.info(f"Order Placed for {each_user} Order_id {order_id}")
                            except:
                                logger.info(f"Error in Closing Order Placement for {this_user['Name']} Error {sys.exc_info()}")

                        # final_df = final_df[final_df['Row_Type'] != 'T']
                        this_instrument['Row_Type'] = 'F'
                        final_df = final_df.append(this_instrument, ignore_index=True)

                        this_instrument['Row_Type'] = 'T'
                        this_instrument['multiplier'] = None
                        this_instrument['entry_price'] = None
                        this_instrument['entry_time'] = None
                        this_instrument['multiplier'] = None
                        this_instrument['exit_price'] = None
                        this_instrument['exit_time'] = None
                        this_instrument['status'] = 0
                        this_instrument['entry_order_id'] = None
                        this_instrument['target_price'] = None
                        this_instrument['sl_price'] = None
                        this_instrument['sl_order_id'] = None
                        this_instrument['target_order_id'] = None
                        this_instrument['Row_Type'] = 'T'

                        # Cancel the SL Order placed and Place a opposite Limit Order which with Buffer and Close open position
                        this_instrument['close_positions'] = 0
                        continue
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                logger.info('Error in While True loop Strategy Function.')





if __name__ == '__main__':
    instruments_df_dict = dict()
    main()
