import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import talib

from Libs.Utils.exception_handler import getAlgoLogger
from .Instrument import Instrument
from .PNL import PNL
from ..Static.ta_lib_extended import SuperTrend
from ..Static import modifiers, TA_Lib, NINE_15

logger = getAlgoLogger(__name__)

def strategy(instrument: Instrument, strategy_pref_obj, pnl_manager_obj: 'PNL'):
    # todo: check the requirement of this once, positions are getting managed in a separate PNL class
    # self.final_df = self.final_df[self.final_df['Row_Type'] != 'T']
    try:
        curr_date = datetime.now()

        try:
            product_type = "MIS"
            if instrument["exchange"] == "MCX":
                product_type = "NRML"
            selected_order_type = instrument["order_type"]
            if selected_order_type.upper() == "MARKET":
                ORDER_TYPE = "MARKET"
                instrument["wait_time"] = 0
                instrument["buy_ltp_percent"] = 0
                instrument["sell_ltp_percent"] = 0
            else:  # elif selected_order_type.upper() == "LIMIT":
                ORDER_TYPE = "LIMIT"

            ltp = instrument.ltp
            # instrument["LTP"] = ltp  # todo: confirm if this is not needed
            if (int((curr_date - NINE_15).seconds / 60) % instrument['timeframe'] > 0) or (
                    int((curr_date - NINE_15).seconds / 60) % instrument['timeframe'] == 0
                    and curr_date.second > 30) and instrument['run_done'] == 1:
                instrument['run_done'] = 0

            if int((curr_date - NINE_15).seconds / 60) % instrument['timeframe'] == 0 \
                    and curr_date.second <= 30 and instrument['run_done'] == 0:
                instrument['run_done'] = 1
                logger.info(f"Running the Strategy for {instrument.symbol}")

                # fetch ohlc, calculate HA, calculate ATR, calculate vwap, store vwap last
                ohlc_df, vwap_last = instrument.prepare_ohlc_data()
                print(f"{instrument.symbol}\n"
                      f"Data DF: {ohlc_df.tail(1)}")
                # --------------------- run algo for calculating the indicator values --------------------
                rsi_trend_bullish, rsi_trend_bearish = instrument.calc_rsi()
                dc_trend_bullish, dc_trend_bearish = instrument.calc_dc()
                volume_trend = instrument.calc_vol()
                oi_trend_bullish, oi_trend_bearish = instrument.calc_oi()
                atr_trend_bullish, atr_trend_bearish = instrument.calc_atrts()
                vwap_trend_bullish, vwap_trend_bearish = instrument.calc_vwap_trend()
                vwap = instrument['vwap_now']
                # -----------------------------------------------------------------------------------------
                logger.info(f"Previous Vwap : {instrument['vwap_last']} Now Vwap : {vwap}")
                logger.info(f"rsi_trend_bullish : {rsi_trend_bullish} rsi_trend_bearish : {rsi_trend_bearish} "
                            f"volume_trend {volume_trend} oi_trend_bullish : {oi_trend_bullish} "
                            f"oi_trend_bearish : {oi_trend_bearish} vwap : {vwap} ltp: {ltp} "
                            f"vwap_trend_bearish : {vwap_trend_bearish} vwap_trend_bullish : {vwap_trend_bullish} ")

                # --------------------- action based on indicator values ----------------------------------
                if atr_trend_bullish and dc_trend_bullish and vwap_trend_bullish and oi_trend_bullish and volume_trend and rsi_trend_bullish and instrument['multiplier'] != 1:
                    logger.info(f" In Buy Loop. for {instrument.symbol}")
                    logger.info(f"Multiplier : {instrument['multiplier']} Status :  {instrument['status']}")

                    if instrument['multiplier'] == -1 and instrument['status'] == 2:

                        if instrument['exit_criteria'] in ['sl_trigger', 'both']:
                            return  # todo: verify: continue replaced with return (due to loop replacement)
                        logger.info(f" Closing Open Sell Position.")
                        if strategy_pref_obj.paper_trade == 0:
                            oms.close_position(symbol=instrument.symbol, product=product_type, order_type=ORDER_TYPE)

                        # todo: add exit position logic in PNL class inspired from code segment below
                        instrument['profit'] = ((ltp - instrument['entry_price']) *
                                                instrument['multiplier'] * instrument['quantity'] *
                                                instrument['lot_size'])
                        instrument['exit_time'] = datetime.now()
                        instrument['exit_price'] = ltp
                        instrument['status'] = 0

                        # final_df = final_df[final_df['Row_Type'] != 'T']
                        instrument['Row_Type'] = 'F'
                        this_row_df = pd.DataFrame(instrument, index=[0])
                        self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                        self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                        self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                        self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
                        instrument.reset_flags()

                    if instrument['multiplier'] is None and instrument['buy_flag']:
                        logger.info(f"Buy Signal has been Activated for {instrument.symbol}")
                        instrument['status'] = 1
                        instrument['multiplier'] = 1

                        instrument['entry_price'] = modifiers.fix_values(
                            df['HA_close'].tail(1).values[0] * (
                                    1 - instrument['buy_ltp_percent'] / 100),
                            instrument['tick_size'])
                        instrument['entry_time'] = datetime.now()
                        instrument['target_price'] = modifiers.fix_values(
                            instrument['entry_price'] * (1 + instrument['target'] / 100),
                            instrument['tick_size'])
                        if instrument['stoploss_type'] == 'ATR':

                            instrument['sl_price'] = modifiers.fix_values(
                                instrument['entry_price'] - instrument['multiplier'] *
                                df['ATR'].tail(1).values[0] * (instrument['stoploss_atr'] / 100),
                                instrument['tick_size'])

                        elif instrument['stoploss_type'] == 'VALUE':
                            instrument['sl_price'] = modifiers.fix_values(
                                instrument['entry_price'] - instrument['multiplier'] *
                                instrument['stoploss_value'], instrument['tick_size'])

                        if strategy_pref_obj.paper_trade == 0:
                            instrument['entry_order_id'] = oms.place_buy_order_om(
                                price=instrument['entry_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type=ORDER_TYPE,
                                prod_type=product_type,
                                exchange=instrument['exchange'])

                            # --------------- todo: place order with current user ----------------
                            instrument.current_user.place_order(**{price=instrument['entry_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type=ORDER_TYPE,
                                prod_type=product_type,
                                exchange=instrument['exchange']})
                        else:
                            logger.info("Buy Order Noted for Paper Trade")

                        logger.info(f"Instrument_Details : {instrument}")

                elif (atr_trend_bearish and dc_trend_bearish and vwap_trend_bearish and oi_trend_bearish and
                      volume_trend and rsi_trend_bearish and instrument['multiplier'] != -1):
                    logger.info(f" In Sell Loop. for {instrument.symbol}")
                    logger.info(f"{instrument.symbol} : {instrument}")
                    logger.info(f"Multiplier : {instrument['multiplier']}"
                                f" Status :  {instrument['status']}")

                    if instrument['multiplier'] == 1 and instrument['status'] == 2:
                        if instrument['exit_criteria'] in ['sl_trigger', 'both']:
                            continue
                        logger.info(f"Closing Open Buy Position.")
                        if strategy_pref_obj.paper_trade == 0:
                            oms.close_position(symbol=instrument.symbol, product=product_type,
                                               order_type=ORDER_TYPE)
                        instrument['profit'] = (ltp - instrument['entry_price']) \
                                                    * instrument['multiplier'] \
                                                    * instrument['quantity'] \
                                                    * instrument['lot_size']
                        instrument['exit_time'] = datetime.now()
                        # todo: use the price of the order placed inside close position order (above)
                        instrument['exit_price'] = ltp
                        instrument['status'] = 0
                        # final_df = final_df[final_df['Row_Type'] != 'T']
                        instrument['Row_Type'] = 'F'
                        this_row_df = pd.DataFrame(instrument, index=[0])
                        self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                        self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                        self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                        self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
                        instrument.reset_flags()

                    if instrument['multiplier'] is None and instrument['sell_flag']:
                        logger.info(
                            f" Sell Signal has been Activated for {instrument.symbol}")

                        instrument['status'] = 1
                        instrument['multiplier'] = -1

                        instrument['entry_price'] = modifiers.fix_values(
                            df['HA_close'].tail(1).values[0] * (1 -
                                                                instrument['multiplier'] *
                                                                instrument['sell_ltp_percent'] / 100),
                            instrument['tick_size'])

                        instrument['entry_time'] = datetime.now()
                        instrument['target_price'] = modifiers.fix_values(
                            instrument['entry_price'] * (1 - instrument['target'] / 100),
                            instrument['tick_size'])
                        if instrument['stoploss_type'] == 'ATR':

                            instrument['sl_price'] = modifiers.fix_values(
                                instrument['entry_price'] - instrument['multiplier'] *
                                df['ATR'].tail(1).values[0] * (instrument['stoploss_atr'] / 100),
                                instrument['tick_size'])

                        elif instrument['stoploss_type'] == 'VALUE':
                            instrument['sl_price'] = modifiers.fix_values(
                                instrument['entry_price'] - instrument['multiplier'] *
                                instrument['stoploss_value'], instrument['tick_size'])

                        if strategy_pref_obj.paper_trade == 0:
                            instrument['entry_order_id'] = oms.place_sell_order_om(
                                price=instrument['entry_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type=ORDER_TYPE,
                                prod_type=product_type,
                                exchange=instrument['exchange'])
                        else:
                            logger.info("Sell Order noted for Paper Trade.")
                        logger.info(f" Instrument_Details : {instrument}")

            if instrument['status'] == 1:  # Order Placed waiting for Execution
                if strategy_pref_obj.paper_trade == 1:  #
                    current_time = datetime.now()
                    if ltp * instrument['multiplier'] <= instrument['entry_price'] * \
                            instrument['multiplier']:
                        logger.info(f"Entry has been taken for {instrument.symbol}")
                        instrument['entry_time'] = current_time
                        instrument['status'] = 2

                    wait_time = instrument['entry_time'] + timedelta(minutes=int(instrument['wait_time']))
                    if current_time > wait_time and ORDER_TYPE == "LIMIT":
                        logger.info(f" Cancelling the Placed Order for {instrument.symbol}")
                        instrument.reset_flags(reset_values=False)

                elif strategy_pref_obj.paper_trade == 0:  # Check_Order_Execution
                    entry_order_id = instrument['entry_order_id']
                    main_order_status = oms.get_order_status(entry_order_id)
                    # todo: remove this
                    main_order_status = instrument.current_user.get_order_status(instrument['entry_order_id'])
                    if main_order_status == 'COMPLETE' and instrument['exit_criteria'] not in ['signal_change']:
                        logger.info(f"Entry has been taken for {instrument.symbol}"
                                    f" Order_id : {instrument['entry_order_id']}")
                        instrument['entry_time'] = datetime.now()
                        instrument['status'] = 2

                        logger.info(f"Placing Target and Stoploss Order")

                        if instrument['multiplier'] == 1:
                            instrument['sl_order_id'] = oms.place_sell_order_om(
                                price=instrument['sl_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type="SL",
                                trgr_price=instrument['sl_price'],
                                prod_type=product_type,
                                exchange=instrument['exchange'])

                            instrument['target_order_id'] = oms.place_sell_order_om(
                                price=instrument['target_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type="LIMIT",
                                prod_type=product_type,
                                exchange=instrument['exchange'])

                            logger.info(f"Target Order ID : {instrument['target_order_id']} and "
                                        f"Stoploss Order ID : {instrument['sl_order_id']}")

                        if instrument['multiplier'] == -1:
                            instrument['sl_order_id'] = oms.place_buy_order_om(
                                price=instrument['sl_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type="SL",
                                trgr_price=instrument['sl_price'],
                                prod_type=product_type,
                                exchange=instrument['exchange'])

                            instrument['target_order_id'] = oms.place_buy_order_om(
                                price=instrument['target_price'],
                                qty=int(instrument['quantity']) * int(instrument['lot_size']),
                                symbol=instrument.symbol,
                                order_type="LIMIT",
                                prod_type=product_type,
                                exchange=instrument['exchange'])

                            logger.info(
                                f"Target Order ID : {instrument['target_order_id']} and Stoploss Order ID : {instrument['sl_order_id']}")

                    if main_order_status == 'COMPLETE' and (instrument['exit_criteria'] in
                                                            ['signal_change', 'both']):
                        instrument['status'] = 2
                        continue

                    wait_time = instrument['entry_time'] + timedelta(
                        minutes=int(instrument['wait_time']))
                    if datetime.now() > wait_time and ORDER_TYPE == "LIMIT":
                        logger.info(f" Cancelling the Placed Order for {instrument.symbol}")
                        # todo: cancel order for users with "PENDING" status.
                        oms.close_position(symbol=instrument.symbol, product=product_type,
                                           order_type=ORDER_TYPE)
                        instrument['Row_Type'] = 'T'
                        instrument['multiplier'] = None
                        instrument['entry_price'] = None
                        instrument['entry_time'] = None
                        instrument['exit_price'] = None
                        instrument['exit_time'] = None
                        instrument['status'] = 0
                        instrument['entry_order_id'] = None
                        instrument['target_price'] = None
                        instrument['sl_price'] = None
                        instrument['sl_order_id'] = None
                        instrument['target_order_id'] = None

            # Order Placed was executed and Stoploss and target Order were placed Calculate Pnl and Store it in CSV
            if instrument['status'] == 2:  # todo: see here for tsl addition
                instrument['profit'] = ((ltp - instrument['entry_price']) *
                                             instrument['multiplier'] *
                                             instrument['quantity'] *
                                             instrument['lot_size'])
                # final_df = final_df[final_df['Row_Type']!='T']
                instrument['Row_Type'] = 'T'
                this_row_df = pd.DataFrame(instrument, index=[0])
                self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])

                if strategy_pref_obj.paper_trade == 1:
                    # logger.info(f"{ltp} {instrument['multiplier']} {instrument['target_price']} {instrument['sl_price']}")
                    if (ltp * instrument['multiplier'] >=
                            instrument['target_price'] * instrument['multiplier'] and
                            instrument['exit_criteria'] not in ['signal_change']):
                        logger.info(f"Target has been Hit for {instrument.symbol}")
                        instrument['exit_time'] = datetime.now()
                        instrument['exit_price'] = ltp
                        instrument['status'] = 0

                        # final_df = final_df[final_df['Row_Type']!='T']
                        instrument['Row_Type'] = 'F'
                        this_row_df = pd.DataFrame(instrument, index=[0])
                        self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                        self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                        self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                        self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
                        instrument.reset_flags()

                    elif ltp * instrument['multiplier'] <= instrument['sl_price'] * \
                            instrument[
                                'multiplier'] and instrument['exit_criteria'] not in ['signal_change']:

                        logger.info(f"Stoploss has been Hit for {instrument.symbol}")
                        instrument['exit_time'] = datetime.now()
                        instrument['exit_price'] = ltp
                        instrument['status'] = 0

                        # final_df = final_df[final_df['Row_Type'] != 'T']
                        instrument['Row_Type'] = 'F'
                        this_row_df = pd.DataFrame(instrument, index=[0])
                        self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                        self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                        self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                        self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
                        instrument.reset_flags()

                if strategy_pref_obj.paper_trade == 0 and instrument['exit_criteria'] not in ['signal_change']:
                    target_order_status = oms.get_order_status(instrument['target_order_id'])
                    stoploss_order_status = oms.get_order_status(instrument['sl_order_id'])

                    if target_order_status == 'COMPLETE' or stoploss_order_status == 'COMPLETE':
                        if target_order_status == 'COMPLETE':
                            logger.info(f"Target has been Hit for {instrument.symbol}")
                            oms.close_position(symbol=instrument.symbol, product=product_type,
                                               order_type=ORDER_TYPE)
                        else:
                            logger.info(f"Stoploss has been Hit for {instrument.symbol}")
                            oms.close_position(symbol=instrument.symbol, product=product_type,
                                               order_type=ORDER_TYPE)
                        instrument['exit_price'] = ltp
                        instrument['exit_time'] = datetime.now()

                        # final_df = final_df[final_df['Row_Type']!='T']
                        instrument['Row_Type'] = 'F'
                        this_row_df = pd.DataFrame(instrument, index=[0])
                        self.final_df = pd.concat([self.final_df, this_row_df], ignore_index=True)
                        self.final_df = self.final_df[app_data.POSITIONS_COLUMNS]
                        self.final_df['Trend'] = np.where(self.final_df['multiplier'] == 1, 'BUY', 'SELL')
                        self.final_df.to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
                        instrument.reset_flags()
        except Exception as err:
            logger_dev.warning(f"Error inside for loop: {err.__str__()}", exc_info=True)
            traceback.print_exc()

        try:
            self.final_df[app_data.POSITIONS_COLUMNS].to_csv(settings.DATA_FILES["POSITIONS_FILE_NAME"])
        except Exception as e_inner:
            logger_dev.warning(f"Exception in writing to position csv file, {e_inner.__str__()}", exc_info=True)
    except Exception as e_outer:
        logger_dev.warning(f"While loop Error: {e_outer.__str__()}", exc_info=True)
        traceback.print_exc()
