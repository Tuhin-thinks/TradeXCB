from Libs.tradexcb_algo.driver.Instrument import Instrument


class User:
    def __init__(self, usr_details: dict):
        self.creds = usr_details

    def execute_strategy(self, instrument: 'Instrument'):
        """
        Takes the instrument instance and runs the strategy, based on last step followed and next step to be followed.
        And also take into consideration, the result of the last row.
        Args:
            instrument: instance of class Instrument

        Returns:
            None
        """
        instrument.set_current_user(self)
        instrument.run_algo()  # todo: implement this function in Instrument class
