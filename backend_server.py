import db
from Const import Const


class BitcoinDepotServer:
    def __init__(self):
        self.db = db

    def get_current_states_and_cities(self):
        '''returns json of city/state '''
        state_list_dict = []
        states_docs = self.db.states_collection.find({})
        for doc in states_docs:
            state = doc[Const.STATE_KEY]
            city_list = doc[Const.CITY_KEY]
            state_list_dict.append({state: city_list})

        state_list_dict
        json_data = {"data": state_list_dict}

        return json_data

    def get_current_current_atms(self):
        '''returns json of all atms '''

        atm_list_dict = []
        atm_docs = self.db.atms_collection.find({})
        for doc in atm_docs:
            try:
                state = doc[Const.STATE_KEY]
                city = doc[Const.CITY_KEY]

                address = doc[Const.ADDRESS_KEY]
                hours = doc[Const.HOURS_KEY]
                store_name = doc[Const.NAME_KEY]
                transaction_type = doc[Const.TYPE_KEY]
                zip_code = doc[Const.ZIP_KEY]
                location = doc[Const.LOCATION_KEY]

                lat, lng = self.get_lat_longi(location)

                atm_info_dict = {Const.STATE_KEY: state, Const.CITY_KEY: city, Const.ADDRESS_KEY: address,
                                 Const.HOURS_KEY: hours, Const.STORE_KEY: store_name,
                                 Const.TRANSACTION_KEY: transaction_type, Const.ZIP_KEY: zip_code, Const.LAT_KEY: lat,
                                 Const.LONGI_KEY: lng}

                atm_list_dict.append(atm_info_dict)
            except:
                # goal is to add logic to find id of record causing to failure
                pass

        json_data = {"data": atm_list_dict}

        return json_data

    def get_lat_longi(self, location):
        coordinates = location['coordinates']

        lat = float(coordinates[0])
        longi = float(coordinates[1])
        return lat, longi

