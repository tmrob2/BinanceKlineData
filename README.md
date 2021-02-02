#Binance CLI helper

This is a tool which connects to binance and downloads kline data to a postgres
database using SQLAlchemy

## Database Connection Setup
Connecting to the database relies on constructing a URI as a dictionary object and 
can be done using the following template
```python
DATABASE = {
            "drivername": "postgresql",
            "username": "mydbusrname",
            "password": "strong%password%from%password%generator",
            "host": '192.168.0.xxx', # server location if on local use 'localhost'
            "database": "mydatabasename",
            "port": 5432 # default postgres port
        }
```
## Creating a config.py
Passwords, database connections, and api connection key:secret pairs should be
stored in a ```config.py```. The layout of ```config.py``` can be copied from 
```config.py.backup``` inserting your specific passwords, keys, and database
connection information. 

## Installing CLI Tool
### Prerequisites

Create a local environment with ```virtualenv``` using python3.7. The binance futures api requires python
version 3.7 to work. 

Binance futures python api wrapper is required and must be installed before the CLI
tool can be installed. A special version of the Binance_Futures python api interface
is required and can cloned from ```https://github.com/tmrob2/Binance_Futures_python.git```.

To install Binance Futures python from the url above, activate the local environment,
navigate to the cloned Binance_Futures_python directory and install the setup.py using:
```sh
foo@bar:~\..\Binance_Futures_python$ pip3 install -e .
```
making sure to put the ```.``` at the end to reference the local directory.

### Installing CLI Tool

To install the CLI tool navigate back to the project directory and install the setup.py file using 
the below shell command, making sure that the local environment is activated.
```sh
foo@bar:~\..\BinanceKlineData$ pip3 install -e .
```


### Usage
To use the cli tool, open a terminal and activate the local environment. To understand the syntax and 
parameters use the following ```--help``` parameter. Parameters are typed and optioned leaving little
to error if the terminal help docs are read. 
```sh
(binance_kline_env)foo@bar:~$ kline_data --help
```
An example might be to get the daily data from testnet for the symbol BTCUSDT:
```sh
(binance_kline_env)foo@bar:~$ kline_query  --interval 1d --test y BTCUSDT
```
The syntax of the command is ```kline_data [OPTIONS] [ARGUMENT]```. The argument is always a ticker symbol.

