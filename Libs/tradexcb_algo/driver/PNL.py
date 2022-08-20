from Libs.globals import *
from Libs.Utils.calculations import get_symbol_hash
from Libs.Utils.exception_handler import getFutureLogger
from .Instrument import Instrument

logger = getFutureLogger(__name__)


class PNL:
    class PNLEntry:
        def __init__(self, instrument: 'Instrument'):
            self.instrument = instrument

    def __init__(self):
        self.entries: typing.Dict[str, typing.Any] = {}

    def add_entry(self, instrument):
        symbol_hash = get_symbol_hash(instrument, key_factor=instrument.transaction_type)
        if symbol_hash in self.entries:
            logger.warning(f"Cannot take duplicate entry of {instrument.symbol} [{instrument.transaction_type}]")
            return
        self.entries[symbol_hash] = self.PNLEntry(instrument)
