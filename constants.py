from models import Binance_v2_1d_btcusdt, Binance_v2_8h_btcusdt

class SYMBOLS:
    BNBUSDT = "BNBUSDT"
    BTCUSDT = "BTCUSDT"


class INTERVALS:
    i_1m = "1m"
    i_1d = "1d"
    i_8h = "8h"

class DBTABLE:
    iD = Binance_v2_1d_btcusdt
    i8h = Binance_v2_8h_btcusdt