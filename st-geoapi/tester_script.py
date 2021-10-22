from flask import Flask
from flask import jsonify
from GeoserverCatalog import GeoserverCatalog
from GeoserverRestService import GeoserverRestService
def test():
    cat = GeoserverCatalog() 
    cat.create_datastore('store_test',
                         'Alain',
                         'postgres',
                         'localhost',
                         '5432',
                         'postgres',
                         'keopsyad',
                         'PostGIS')

    print('HI')







test()