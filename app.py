from flask import Flask

from scrapper import BitcoinDepotScrapper
from backend_server import BitcoinDepotServer

app = Flask(__name__)


@app.route('/')
def flask_mongo_db_atlas():
    return "flask mongodb atlas!"


@app.route('/get_states')
def get_states_and_cities():
    bds = BitcoinDepotServer()
    status = bds.get_current_states_and_cities()
    return status


@app.route('/get_atm_location')
def get_atms():
    bot = BitcoinDepotServer()
    status = bot.get_current_current_atms()
    return status


@app.route('/check_stores')
def check_stores():
    bot = BitcoinDepotScrapper()
    status = bot.populate_database()
    return status


if __name__ == '__main__':
    app.run(port=8000, debug=True)
