from models import create_engine, create_table, Base, Binance_funding_btcusdt
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.url import URL
import config
import pandas as pd
import binance_d
from binance_d.model.constant import CandlestickInterval
from binance_d.requestclient import FuncResponse
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

@click.group()
def cli():
    """
    A cli helper to update binance data for channel calculations
    
    Some useful information on times: 
    BTCUSDT: M Futures contract start date: 2020-8-11
    """

@click.command()
@click.option('--interval', default="1d", help="kline interval", type=click.Choice([constants.INTERVALS.i_1d, constants.INTERVALS.i_8h]))
@click.option('--test', default='y', help="connect to testnet or mainnet", type=click.BOOL)
@click.option('--start', help="The start date to extract data from, date format: '%Y-%m-%d'")
@click.argument('symbol', type=click.Choice([
    constants.SYMBOLS.BNBUSDT, constants.SYMBOLS.BTCUSDT, constants.SYMBOLS.ETHUSDT, constants.SYMBOLS.BTCUSD_PERP,
    constants.SYMBOLS.BNBUSD_PERP]))
def get_kline_and_funding(interval, test, symbol, start):
    if start is None:
        print("A start date must be given")
        return
    tbl_dict = {
        "btc1d": constants.DBTABLE.btciD,
        "btc_perp1d": constants.DBTABLE.btcperpiD,
        "btc8h": constants.DBTABLE.btci8h,
        "eth1d": constants.DBTABLE.ethiD,
        "bnb1d": constants.DBTABLE.bnbiD,
        "bnb_perp1d": constants.DBTABLE.bnbperpiD,
        "fund_eth": constants.DBTABLE.fund_eth,
        "fund_btc": constants.DBTABLE.fund_btc,
        "fund_bnb": constants.DBTABLE.fund_bnb,
        "fund_btc_perp": constants.DBTABLE.fund_btc_perp,
        "fund_bnb_perp": constants.DBTABLE.fund_bnb_perp
    }

    symbol_abbr = {
        constants.SYMBOLS.ETHUSDT: "eth",
        constants.SYMBOLS.BNBUSDT: "bnb",
        constants.SYMBOLS.BTCUSDT: "btc",
        constants.SYMBOLS.BTCUSD_PERP: "btc_perp",
        constants.SYMBOLS.BNBUSD_PERP: "bnb_perp",
    }

    date_format = "%Y-%m-%d %H:%M:%S"

    session.query(tbl_dict[f"{symbol_abbr[symbol]}{interval}"]).delete()
    session.query(tbl_dict[f"fund_{symbol_abbr[symbol]}"]).delete()
    session.commit()
    initial_date = None
    initial_date = datetime.datetime.strptime(start, date_format)
    if test:
        client = binance_f.RequestClient(api_key=config.Config.BINANCE_TESTNET_API_KEY,
                                         secret_key=config.Config.BINANCE_TESTNET_API_SECRET,
                                         url=config.Config.TESTNET_URI)
    else:
        if symbol == constants.SYMBOLS.BTCUSD_PERP or symbol == constants.SYMBOLS.BNBUSD_PERP:
            client = binance_d.RequestClient(api_key=config.Config.BINANCE_API_KEY,
                                             secret_key=config.Config.BINANCE_TESTNET_API_SECRET,
                                             url=config.Config.URID)
        else:
            client = binance_f.RequestClient(api_key=config.Config.BINANCE_API_KEY,
                                             secret_key=config.Config.BINANCE_TESTNET_API_SECRET,
                                             url=config.Config.URI)
    ls = []
    while initial_date < datetime.datetime.utcnow():
        tdelta = datetime.timedelta(days=200)
        end_date_dt = initial_date + tdelta
        if end_date_dt > datetime.datetime.utcnow():
            end_date_dt = datetime.datetime.utcnow()
        end_date_ts = int(datetime.datetime.timestamp(end_date_dt) * 1000)
        start_date_ts = int(datetime.datetime.timestamp(initial_date) * 1000)
        data: FuncResponse = client.get_candlestick_data(symbol=symbol, interval=interval, startTime=start_date_ts, endTime=end_date_ts, limit=1500)
        initial_date = end_date_dt + datetime.timedelta(days=1)
        for candlestick in data.response:
            d = candlestick.__dict__
            d["id"] = f"{symbol}-{d['openTime']}"
            d["openTime"] = datetime.datetime.utcfromtimestamp(d['openTime'] / 1e3)
            d["closeTime"] = datetime.datetime.utcfromtimestamp(d['closeTime'] / 1e3)
            ls.append(d)
    df = pd.DataFrame(ls)
    click.echo(f"Retrieved {df.shape[0]} rows of data for {symbol}")
    # push to sql
    df.to_sql(name=tbl_dict[f"{symbol_abbr[symbol]}{interval}"].__tablename__, con=engine, if_exists='append', index=False, chunksize=1000)
    funding_ls = []
    response_len = 1000
    start_time = 1567864800000 #int(datetime.datetime.timestamp(initial_date) * 1000)
    counter = 0
    while response_len == 1000:
        click.echo(f"Getting funding rate: {counter}")
        funding: FuncResponse = client.get_funding_rate(symbol=symbol, startTime=start_time, limit=1000)
        response_len = len(funding.response)
        # generate a list of dicts from the data as list of dicts can be easily converted into a pandas dataframe object

        for funding_row in funding.response:
            d_fund = funding_row.__dict__
            d_fund["id"] = f"{symbol}-{d_fund['fundingTime']}"
            new_funding_time = int(d_fund["fundingTime"])
            d_fund["fundingTime"] = datetime.datetime.utcfromtimestamp(d_fund['fundingTime'] / 1e3)
            funding_ls.append(d_fund)
            start_time_date_format = datetime.datetime.utcfromtimestamp(new_funding_time / 1e3)
            utc_dt = start_time_date_format + datetime.timedelta(hours=8)
            start_time = int(utc_dt.replace(tzinfo=datetime.timezone.utc).timestamp()) * 1000

        counter += 1

    click.echo(f"Retrieved {len(funding_ls)} funding data rows")
    df_fund = pd.DataFrame(funding_ls)
    df_fund.to_sql(name=tbl_dict[f"fund_{symbol_abbr[symbol]}"].__tablename__, con=engine, if_exists='append', index=False, chunksize=1000)