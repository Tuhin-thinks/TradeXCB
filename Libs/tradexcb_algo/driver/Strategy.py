from typing import Union, List
import pandas as pd

from Libs.Utils import settings
from Libs.tradexcb_algo.driver import User, Instrument
from Libs.Files.handle_user_details import read_user_api_details


class Strategy:
    class StrategyPreferences:
        def __init__(self, paper_trade: int):
            self.paper_trade = paper_trade

    def __init__(self, paper_trade: int):
        self.strategy_rows = []
        self.instrument_obj_list: List[Instrument.Instrument] = []
        self.user_obj_list: List[User.User] = []
        self.strategy_pref_pbj = self.StrategyPreferences(paper_trade=paper_trade)

    def load_strategy(self):
        """
        Reads the Excel file and create dictionary of rows from the Excel file.

        Returns:
            None
        """
        sheet_df = pd.read_excel(settings.DATA_FILES['tradexcb_excel_file'], sheet_name="Sheet1")
        self.strategy_rows = sheet_df.reset_index().to_dict(orient="records")

    def init_instrument_instances(self):
        """
        Function to create instrument objects from row_dict dictionary rows from Excel file.
        Returns:
            None
        """
        for row_dict in self.strategy_rows:
            instrument_obj = Instrument.Instrument(instrument_details=row_dict,
                                                   broker=self.main_broker,  # todo: pass main broker from here
                                                   strategy_pref_obj=self.strategy_pref_pbj)
            self.instrument_obj_list.append(instrument_obj)

    def init_user_instances(self):
        """
        Read user details from sqlite3 local database and create user instances.
        Returns:
            None
        """
        # read all rows from user api details
        user_api_details_list = read_user_api_details()
        for user_creds in user_api_details_list:
            user_obj = User.User(user_creds)
            self.user_obj_list.append(user_obj)

    def run_strategy(self):
        """
        Runs the main strategy loop and the basic synchronization process
        Returns:
            None
        """
        # todo: check when the data recalculation is required. [currently based on n-user iteration completion]
        for instrument_obj in self.instrument_obj_list:
            # execute instrument row for every user
            for user_obj in self.user_obj_list:
                user_obj.execute_strategy(instrument_obj)
