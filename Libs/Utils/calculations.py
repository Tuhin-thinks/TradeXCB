from datetime import datetime

import numpy as np
from Libs.Utils import settings
from Libs.globals import *
import hashlib
import json

nine_fifteen = datetime.today().replace(hour=9, minute=15, second=0, microsecond=0)  # start time
three_35 = datetime.today().replace(hour=15, minute=35, second=0, microsecond=0)  # stop time


def dict_hash(dictionary: typing.Dict[str, typing.Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def is_refresh_required(time_frame):
    """
    calculate next update time,
    return boolean, remaining_time

    if remaining_time.isdigit() == False:
        show the exact string in status bar
    else:
        show the remaining time (digit) concatenated with some info string

    :param time_frame: time frame in minutes
    :return: bool, str
    """
    if (datetime.now() >= three_35 or datetime.now() < nine_fifteen) or not is_weekday():
        return False, "Last data updated 03.35pm, Next day update starts at 9.15am"
    pending_wait = ((time_frame - settings.adjust_minutes) * 60) - (datetime.now() - nine_fifteen).seconds % (
            (time_frame - settings.adjust_minutes) * 60)  # pending wait in secs.
    if pending_wait <= 1:  # tolerance of 1s
        return True, str(int(pending_wait))
    else:
        return False, str(int(pending_wait))


def vwap_crossover_check(row_data):
    """
    This function to be used inside .apply() of any dataframe
    :param row_data: pandas row data
    :return: output to set to particular columns
    """
    if row_data['Vwap_PE'] == 0:  # check to get rin of ZeroDivisionError and RunTimeWarning
        ce_vwap_crossover = ""
    else:
        ratio_ce = np.divide(row_data['Price_CE'], row_data['Vwap_CE'])
        if ratio_ce > 1:
            ce_vwap_crossover = "CE ABOVE VWAP"
        elif ratio_ce < 1:
            ce_vwap_crossover = "CE BELOW VWAP"
        else:
            ce_vwap_crossover = ""

    if row_data['Vwap_PE'] == 0:  # check to get rin of ZeroDivisionError and RunTimeWarning
        pe_vwap_crossover = ""
    else:
        ratio_pe = np.divide(row_data['Price_PE'], row_data['Vwap_PE'])
        if ratio_pe > 1:
            pe_vwap_crossover = "PE ABOVE VWAP"
        elif ratio_pe < 1:
            pe_vwap_crossover = "PE BELOW VWAP"
        else:
            pe_vwap_crossover = ""

    return ce_vwap_crossover, pe_vwap_crossover


def delta_crossover_check(row_data):
    """
        This function to be used inside .apply() of any dataframe
        :param row_data: pandas row data
        :return: output to set to particular column
    """
    if row_data['DELTA_PE'] == 0:  # check to get rin of ZeroDivisionError and RunTimeWarning
        return ''
    ratio = np.divide(abs(row_data['DELTA_CE']), abs(row_data['DELTA_PE']))
    if ratio > 1:
        return "DELTA CE GOING UP"
    elif ratio < 1:
        return "DELTA PE GOING UP"
    else:
        return ""


def is_weekday():
    today_ = datetime.today()
    return today_.isoweekday() < 6


def get_default_exit_time():
    return datetime.today().replace(hour=15, minute=30, second=0).strftime("%H.%M.%S")


def get_default_entry_time():
    _3_30 = datetime.today().replace(hour=15, minute=30, second=0).strftime("%H.%M.%S")
    _9_15 = datetime.today().replace(hour=9, minute=15, second=0).strftime("%H.%M.%S")
    if datetime.now() > datetime.strptime(_3_30, "%H.%M.%S"):
        return _9_15
    else:
        return datetime.now().strftime("%H.%M.%S")
