from models import (Binance_v2_1d_btcusdt, Binance_v2_8h_btcusdt, Binance_v2_1d_bnbusdt,
                    Binance_v2_1d_ethusdt, Binance_funding_ethusdt, Binance_funding_btcusdt,
                    Binance_funding_bnbusdt, Binance_v2_1d_btcusd_perp, Binance_funding_btcusd_perp)

class SYMBOLS:
    BNBUSDT = "BNBUSDT"
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    BTCUSD_PERP = "BTCUSD_PERP"


class INTERVALS:
    i_1m = "1m"
    i_1d = "1d"
    i_8h = "8h"

class DBTABLE:
    btciD = Binance_v2_1d_btcusdt
    btcperpiD = Binance_v2_1d_btcusd_perp
    btci8h = Binance_v2_8h_btcusdt
    ethiD = Binance_v2_1d_ethusdt
    bnbiD = Binance_v2_1d_bnbusdt
    fund_btc = Binance_funding_btcusdt
    fund_btc_perp = Binance_funding_btcusd_perp
    fund_eth = Binance_funding_ethusdt
    fund_bnb = Binance_funding_bnbusdt