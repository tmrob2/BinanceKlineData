from setuptools import setup, find_packages

setup(
    name='BINANCE_KLINE_QUERY',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'SQLAlchemy',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        kline_query=dbase_maintenance:get_candle_stick_data
    ''',
)