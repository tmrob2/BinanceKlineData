from models import create_engine, create_table, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.url import URL
import config
import pandas as pd
import binance_f
from binance_f.model.constant import CandlestickInterval
from binance_f.requestclient import FuncResponse
import datetime
import time
import click
import constants

engine = create_engine(URL(**config.Config.DATABASE))
create_table(engine)
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

@click.command()
@click.option('--interval', default="1d", help="kline interval", type=click.Choice([constants.INTERVALS.i_1d, constants.INTERVALS.i_8h]))
@click.option('--test', default='y', help="connect to testnet or mainnet", type=click.BOOL)
@click.argument('symbol', type=click.Choice([constants.SYMBOLS.BNBUSDT, constants.SYMBOLS.BTCUSDT]))
def get_candle_stick_data(interval, test, symbol):
    tbl_dict = {"1d": constants.DBTABLE.iD, "8h": constants.DBTABLE.i8h}
    session.query(tbl_dict[interval]).delete()
    session.commit()
    if test:
        client = binance_f.RequestClient(api_key=config.Config.BINANCE_TESTNET_API_KEY,
                                         secret_key=config.Config.BINANCE_TESTNET_API_SECRET,
                                         url=config.Config.TESTNET_URI)
    else:
        client = binance_f.RequestClient(api_key=config.Config.BINANCE_API_KEY,
                                         secret_key=config.Config.BINANCE_TESTNET_API_SECRET,
                                         url=config.Config.URI)
    data: FuncResponse = client.get_candlestick_data(symbol=symbol, interval=interval, startTime=None, endTime=None, limit=1500)
    # generate a list of dicts from the data as list of dicts can be easily converted into a pandas dataframe object
    ls = []
    for candlestick in data.response:
        d = candlestick.__dict__
        d["id"] = f"{symbol}-{d['openTime']}"
        d["openTime"] = datetime.datetime.utcfromtimestamp(d['openTime'] / 1e3)
        d["closeTime"] = datetime.datetime.utcfromtimestamp(d['closeTime'] / 1e3)
        ls.append(d)
    df = pd.DataFrame(ls)
    # push to sql
    df.to_sql(name=tbl_dict[interval].__tablename__, con=engine, if_exists='append', index=False, chunksize=1000)