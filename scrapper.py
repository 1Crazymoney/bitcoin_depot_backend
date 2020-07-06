import requests
import re
import pandas as pd
import json
import db
from Const import Const


class BitcoinDepotScrapper:
    def __init__(self):
        self.db = db
        pass

    def get_current_atms_from_site(self):
        '''scrapes website for atm info'''
        r = requests.get(Const.BITCOIN_DEPOT_HOME_URL)
        website_content = r.text

        map_points = re.findall("(?<=MAP_POINTS__ = )(.*)(?=<\/script)", website_content)
        if len(map_points) == 1:
            map_points = json.loads(map_points[0])
        else:
            return False

        atm_location_df = pd.DataFrame(map_points)
        return atm_location_df

    def populate_database(self):
        '''Inserts data in mongodb'''
        df = self.get_current_atms_from_site()
        if df.empty:
            return
        state_table_status = self.update_state_table(df)
        atm_location_table_status = self.update_atm_location_table(df)

        message = 'Successfully updated both tables'
        if not state_table_status and atm_location_table_status:
            message = 'Database insert failed'

        print(message)

    def update_atm_location_table(self, df):
        '''Updates existing atm locations and inserts new ones if not found'''
        for index, row in df.iterrows():
            state = row['state']
            address = row['address']
            city = row['city']
            hours = row['hours']
            lat = row['lat']
            lng = row['lng']
            store_name = row['name']
            transaction_type = row['type']
            zipcode = row['zip']
            location_gps = {"type": "Point",
                            "coordinates": [lat, lng]}

            query_find = {"address": address}
            update_info = {"$set": {Const.STATE_KEY: state, Const.CITY_KEY: city, Const.HOURS_KEY: hours,
                                    Const.ADDRESS_KEY: address, Const.NAME_KEY: store_name,
                                    Const.TYPE_KEY: transaction_type, Const.ZIP_KEY: zipcode,
                                    Const.LOCATION_KEY: location_gps}}
            self.db.atms_collection.find_one_and_update(query_find, update_info, upsert=True)

        return True

    def update_state_table(self, df):
        '''Update state table when new cities and states are added to site.'''
        state_list = df.state.unique().tolist()

        for state in state_list:
            city_list = df['city'][df['state'] == state].unique().tolist()
            query_find = {Const.STATE_KEY: state}
            update_info = {"$set": {Const.CITY_KEY: city_list}}
            self.db.states_collection.find_one_and_update(query_find, update_info, upsert=True)
        return True

# if __name__ == '__main__':
#     bot = BitcoinDepotScrapper()
#     bot.populate_database()
