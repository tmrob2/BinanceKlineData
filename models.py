from sqlalchemy import create_engine, Column, Boolean, Integer, String, DateTime, Float, BigInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import config


Base = declarative_base()


def db_connect():
    return create_engine(URL(**config.Config.DATABASE))


def create_table(engine):
    Base.metadata.create_all(engine)

class Binance_v2_1d_btcusdt(Base):
    __tablename__ = "binance_v2_1d_btcusdt"
    id = Column(String, primary_key=True)
    openTime = Column('openTime', TIMESTAMP)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    volume = Column('volume', Float)
    closeTime = Column('closeTime', TIMESTAMP)
    quoteAssetVolume = Column('quoteAssetVolume', Float)
    numTrades = Column('numTrades', Integer)
    takerBuyBaseAssetVolume = Column('takerBuyBaseAssetVolume', Float)
    takerBuyQuoteAssetVolume = Column('takerBuyQuoteAssetVolume', Float)
    ignore = Column('ignore', BigInteger)

class Binance_v2_8h_btcusdt(Base):
    __tablename__ = "binance_v2_8h_btcusdt"
    id = Column(String, primary_key=True)
    openTime = Column('openTime', TIMESTAMP)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    volume = Column('volume', Float)
    closeTime = Column('closeTime', TIMESTAMP)
    quoteAssetVolume = Column('quoteAssetVolume', Float)
    numTrades = Column('numTrades', Integer)
    takerBuyBaseAssetVolume = Column('takerBuyBaseAssetVolume', Float)
    takerBuyQuoteAssetVolume = Column('takerBuyQuoteAssetVolume', Float)
    ignore = Column('ignore', BigInteger)