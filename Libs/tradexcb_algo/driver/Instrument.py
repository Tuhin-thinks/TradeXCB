from datetime import datetime
from typing import Union

import pandas as pd
import talib

from Libs.Utils.exception_handler import getFutureLogger
from .User import User
from ..Brokers.BrokerMapping.main_broker import Broker
from ..Static.TA_Lib import HA, ATR
from ..Static.ta_lib_extended import SuperTrend

logger = getFutureLogger(__name__)


class Instrument:
    def __init__(self, instrument_details: dict, broker, strategy_pref_obj):
        self.current_user: Union[None, 'User'] = None
        self.instrument_details = instrument_details
        self.broker: Broker = broker  # here broker is the main_broker that will be used for all the data
        self.transaction_type = self.instrument_details['transaction_type']
        self.symbol = self.instrument_details['tradingsymbol']
        self.strategy_pref_obj = strategy_pref_obj

        self.data_cache = {}
        self.is_refresh_required = {}

    @property
    def ltp(self):
        # todo: write code to get ltp of an instrument from api
        #   This can also take into account the usage of websockets, to take ltp from a pool of ltp for faster operation
        #   LTP pool is supposed to be created from master broker and to be made operational inside 'Strategy' class
        ...

    def get_ohlc(self, from_dt: datetime, to_date: datetime):
        """
        Get ohlc data using master broker.
        
        Args:
            from_dt: ohlc data start date
            to_date: ohlc data end date

        Returns:
            Dataframe containing the ohlc data or None if ohlc data not found
        """
        # todo: complete this function
        ...

    def get_vwap(self, df: pd.DataFrame):
        try:
            df['time'] = df.index
            columns_df = list(df.columns)
            columns_df.append('vwap')
            df['Quantity_Rolling_Sum'] = df.groupby(df['time'].dt.date)['volume'].cumsum()
            df['PriceXVolume'] = (df['HA_close'] + df['HA_high'] + df['HA_low']) / 3 * df['volume']
            df['PriceXVolumeCUMSUM'] = df.groupby(df['time'].dt.date)['PriceXVolume'].cumsum()
            df['vwap'] = df['PriceXVolumeCUMSUM'] / df['Quantity_Rolling_Sum']
            df = df[columns_df]
            return df

        except Exception as e:
            logger.exception(f"Failed to calculate VWAP for instrument: {self.symbol}, {e.__str__()}", exc_info=True)

    def reset_flags(self, reset_values=True):
        """
        Function to reset all instrument flags when positions exited/closed
        
        Args:
            reset_values(bool): to control if to reset signal values

        Returns:
            None
        """
        self.instrument_details['Row_Type'] = 'T'
        self.instrument_details['multiplier'] = None
        self.instrument_details['entry_price'] = None
        self.instrument_details['entry_time'] = None
        self.instrument_details['exit_price'] = None
        self.instrument_details['exit_time'] = None
        self.instrument_details['status'] = 0
        self.instrument_details['entry_order_id'] = None
        self.instrument_details['target_price'] = None
        self.instrument_details['sl_price'] = None
        self.instrument_details['sl_order_id'] = None
        self.instrument_details['target_order_id'] = None

        if reset_values:
            # Resetting Values
            self.instrument_details['dc_signal'] = 'new'
            self.instrument_details['rsi_signal'] = 'new'
            self.instrument_details['oi_signal'] = 'new'
            self.instrument_details['atrts_signal'] = 'new'
            self.instrument_details['vwap_signal'] = 'new'

    def __getitem__(self, item_name: str):
        return self.instrument_details.get(item_name, None)

    def __setitem__(self, key, value):
        self.instrument_details[key] = value

    def set_current_user(self, user_instance: 'User'):
        self.current_user = user_instance

    def prepare_ohlc_data(self):
        if not self.is_refresh_required:
            return self.data_cache['ohlc_df'], self.data_cache['vwap_last']

        ohlc_df = self.broker.get_ohlc(from_date, to_date)
        df_time_index = ohlc_df.index
        ohlc_df = HA(ohlc_df, ohlc=['open', 'high', 'low', 'close'])
        ohlc_df.index = df_time_index
        ohlc_df['ATR'] = talib.ATR(ohlc_df['HA_high'], ohlc_df['HA_low'], ohlc_df['HA_close'],
                                   self.instrument_details['atr_period'])
        ohlc_df = self.get_vwap(ohlc_df)
        vwap_last = ohlc_df['vwap'].tail(2).head(1).values[0]
        vwap = ohlc_df['vwap'].tail(1).values[0]
        # -------------- store calculated data in cache for a session --------------
        self.data_cache['ohlc_df'] = ohlc_df
        self.data_cache['vwap_last'] = vwap_last
        self.data_cache['vwap_now'] = vwap

        return ohlc_df, vwap_last

    def calc_rsi(self):
        if not self.is_refresh_required:
            rsi_data = self.data_cache['rsi']
            return rsi_data['rsi_trend_bullish'], rsi_data['rsi_trend_bearish']

        rsi_trend_bullish = 1
        rsi_trend_bearish = 1
        ohlc_df = self.data_cache['ohlc_df']
        if self.instrument_details['use_rsi'] == 'YES':
            ohlc_df['RSI'] = talib.RSI(ohlc_df['HA_close'], timeperiod=self.instrument_details['RSI'])
            ohlc_df['RSI_MA'] = talib.EMA(ohlc_df['RSI'], timeperiod=self.instrument_details['rsi_ma_period'])
            if self.instrument_details['rsi_signal'] == 'new':
                rsi_trend_bullish = 1 if (ohlc_df['RSI'].tail(1).values[0] > ohlc_df['RSI_MA'].tail(1).values[
                    0]) and (ohlc_df['RSI'].tail(1).values[0] > self.instrument_details['overbought']) else 0
                rsi_trend_bearish = 1 if (ohlc_df['RSI'].tail(1).values[0] < ohlc_df['RSI_MA'].tail(1).values[
                    0]) and (ohlc_df['RSI'].tail(1).values[0] < self.instrument_details['oversold']) else 0

            if self.instrument_details['rsi_signal'] == 'existing':
                rsi_trend_bullish = 1 if (
                        ohlc_df['RSI'].tail(1).values[0] > ohlc_df['RSI_MA'].tail(1).values[0]) else 0
                rsi_trend_bearish = 1 if (
                        ohlc_df['RSI'].tail(1).values[0] < ohlc_df['RSI_MA'].tail(1).values[0]) else 0

        # ------------------- store rsi values in cache ---------------------
        self.data_cache['rsi']['rsi_trend_bullish'] = rsi_trend_bullish
        self.data_cache['rsi']['rsi_trend_bearish'] = rsi_trend_bearish
        return rsi_trend_bullish, rsi_trend_bearish

    def calc_vol(self):
        if not self.is_refresh_required:
            return self.data_cache['volume_trend']

        ohlc_df = self.data_cache['ohlc_df']
        if self.instrument_details['use_vol'] == "YES":
            ohlc_df['volume_ma'] = talib.EMA(ohlc_df['volume'], timeperiod=self.instrument_details['volume_ma_tp'])
            volume_condition = ohlc_df['volume'].tail(1).values[0] / ohlc_df['volume_ma'].tail(1).values[0]
            volume_trend = 1 if volume_condition > self.instrument_details['volume_ma_mulitple'] else 0

        else:
            volume_trend = 1

        self.data_cache['volume_trend'] = volume_trend
        return volume_trend

    def calc_dc(self):
        if not self.is_refresh_required:
            return self.data_cache['dc']['dc_trend_bullish'], self.data_cache['dc']['dc_trend_bearish']

        ohlc_df = self.data_cache['ohlc_df']
        dc_trend_bullish = 1
        dc_trend_bearish = 1
        if self.instrument_details['dc'] == 'YES':
            ohlc_df['dc_high'] = ohlc_df['HA_high'].rolling(self.instrument_details['dc_high'],
                                                            min_periods=self.instrument_details['dc_high']
                                                            ).max().shift(1)
            ohlc_df['dc_low'] = ohlc_df['HA_low'].rolling(self.instrument_details['dc_low'],
                                                          min_periods=self.instrument_details['dc_low']).min().shift(1)
            ohlc_df['dc_median'] = (ohlc_df['dc_high'] + ohlc_df['dc_low']) * 0.5

            logger.info(f"{self.symbol} : dc_low : {ohlc_df['dc_low'].tail(1).values[0]}"
                        f" dc_high : {ohlc_df['dc_high'].tail(1).values[0]}")

            row_name = 'dc_high' if self.instrument_details['dc_line'].upper() == 'HIGH' else \
                'dc_low' if self.instrument_details['dc_line'].upper() == 'LOW' else 'dc_median' if \
                    self.instrument_details['dc_line'].upper() == 'MEDIAN' else 'dc_median'

            if self.instrument_details['dc_signal'] == 'new':
                dc_trend_bullish = 1 if (ohlc_df[row_name].tail(1).values[0] <
                                         ohlc_df['HA_close'].tail(1).values[
                                             0]) and (ohlc_df[row_name].tail(2).head(1).values[0] >=
                                                      ohlc_df['HA_close'].tail(2).head(1).values[
                                                          0]) else 0
                dc_trend_bearish = 1 if (ohlc_df[row_name].tail(1).values[0] >=
                                         ohlc_df['HA_close'].tail(1).values[0]) and (
                                                ohlc_df[row_name].tail(2).head(1).values[0] <
                                                ohlc_df['HA_close'].tail(2).head(1).values[0]) else 0

            if self.instrument_details['dc_signal'] == 'existing':
                dc_trend_bullish = (1 if (ohlc_df[row_name].tail(1).values[0] < ohlc_df['HA_close'].tail(1).values[0])
                                    else 0)
                dc_trend_bearish = (1 if (ohlc_df[row_name].tail(1).values[0] >= ohlc_df['HA_close'].tail(1).values[0])
                                    else 0)

            self.data_cache['dc']['dc_trend_bullish'] = dc_trend_bullish
            self.data_cache['dc']['dc_trend_bearish'] = dc_trend_bearish

        return dc_trend_bullish, dc_trend_bearish

    def calc_oi(self):
        if not self.is_refresh_required:
            return self.data_cache['oi']['oi_trend_bullish'], self.data_cache['oi']['oi_trend_bearish']

        ohlc_df = self.data_cache['ohlc_df']
        oi_trend_bullish = 1
        oi_trend_bearish = 1
        if self.instrument_details['use_oi'] == 'YES':
            ohlc_df['oi_ema'] = talib.EMA(ohlc_df['oi'], timeperiod=self.instrument_details['oi_ma_period'])

            if self.instrument_details['oi_signal'] == 'new':
                oi_trend_bullish = (1 if (ohlc_df['oi_ema'].tail(1).values[0] >= ohlc_df['oi'].tail(1).values[0])
                                         and (ohlc_df['oi_ema'].tail(2).head(1).values[0] <
                                              ohlc_df['oi'].tail(2).head(1).values[0]) else 0)

                oi_trend_bearish = (1 if (ohlc_df['oi_ema'].tail(1).values[0] < ohlc_df['oi'].tail(1).values[0])
                                         and (ohlc_df['oi_ema'].tail(2).head(1).values[0] >=
                                              ohlc_df['oi'].tail(2).head(1).values[0]) else 0)

            if self.instrument_details['oi_signal'] == 'existing':
                oi_trend_bullish = 1 if (
                        ohlc_df['oi_ema'].tail(1).values[0] >= ohlc_df['oi'].tail(1).values[0]) else 0
                oi_trend_bearish = 1 if (
                        ohlc_df['oi_ema'].tail(1).values[0] < ohlc_df['oi'].tail(1).values[0]) else 0

        self.data_cache['oi']['oi_trend_bullish'] = oi_trend_bullish
        self.data_cache['oi']['oi_trend_bearish'] = oi_trend_bearish

        return oi_trend_bullish, oi_trend_bearish

    def calc_atrts(self):
        if not self.is_refresh_required:
            atrts = self.data_cache['atrts']
            return atrts['atrts_trend_bullish'], atrts['atrts_trend_bearish']

        ohlc_df = self.data_cache['ohlc_df']
        atr_trend_bullish = 1
        atr_trend_bearish = 1
        if self.instrument_details['ATRTS'] == 'YES':
            ohlc_df['SUPERTREND'] = SuperTrend(ohlc_df, self.instrument_details['ATR TS Period'],
                                               self.instrument_details['ATR TS Multiplier'],
                                               ohlc=['HA_open', 'HA_high', 'HA_low', 'HA_close'])
            if self.instrument_details['atrts_signal'] == 'new':
                atr_trend_bearish = 1 if ((ohlc_df['SUPERTREND'].tail(1).head(1).values[0] == 'down') & (
                        ohlc_df['SUPERTREND'].tail(2).head(1).values[0] == 'up')) else 0
                atr_trend_bullish = 1 if ((ohlc_df['SUPERTREND'].tail(1).head(1).values[0] == 'up') & (
                        ohlc_df['SUPERTREND'].tail(2).head(1).values[0] == 'down')) else 0
            if self.instrument_details['atrts_signal'] == 'existing':
                atr_trend_bearish = 1 if (
                    (ohlc_df['SUPERTREND'].tail(1).head(1).values[0] == 'down')) else 0
                atr_trend_bullish = 1 if (
                    (ohlc_df['SUPERTREND'].tail(1).head(1).values[0] == 'up')) else 0

        self.data_cache['atrts']['atr_trend_bullish'] = atr_trend_bullish
        self.data_cache['atrts']['atr_trend_bearish'] = atr_trend_bearish

        return atr_trend_bullish, atr_trend_bearish
    
    def calc_vwap_trend(self):
        if not self.is_refresh_required:
            vwap_details = self.data_cache['vwap']
            return vwap_details['vwap_trend_bullish'], vwap_details['vwap_trend_bearish']

        ohlc_df = self.data_cache['ohlc_df']
        vwap = self.data_cache['vwap_now']
        logger.info(f"Previous Vwap : {self.instrument_details['vwap_last']} Now Vwap : {vwap}")
        vwap_trend_bullish = 1
        vwap_trend_bearish = 1
        if self.instrument_details['vwap'] == 'YES' and self.data_cache['vwap_last'] != 0:

            if self.instrument_details['vwap_signal'] == 'new':
                vwap_trend_bullish = 1 if (ohlc_df['HA_close'].tail(1).head(1).values[0] > vwap) and (
                        ohlc_df['HA_close'].tail(2).head(1).values[0] < self.data_cache['vwap_last']) else 0
                vwap_trend_bearish = 1 if (ohlc_df['HA_close'].tail(1).head(1).values[0] < vwap) and (
                        ohlc_df['HA_close'].tail(2).head(1).values[0] > self.data_cache['vwap_last']) else 0

            if self.instrument_details['vwap_signal'] == 'existing':
                vwap_trend_bullish = 1 if (ohlc_df['HA_close'].tail(1).head(1).values[0] > vwap) else 0
                vwap_trend_bearish = 1 if (ohlc_df['HA_close'].tail(1).head(1).values[0] < vwap) else 0

        self.data_cache['vwap_last'] = vwap
        self.data_cache['vwap_trend']['vwap_trend_bullish'] = vwap_trend_bullish
        self.data_cache['vwap_trend']['vwap_trend_bearish'] = vwap_trend_bearish

        return vwap_trend_bullish, vwap_trend_bearish
