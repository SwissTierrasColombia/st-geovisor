from geo.Geoserver import Geoserver
from geoserver.catalog import Catalog
from Config import Config

geo = None
catalog = None


class GeoserverRestService:
    def __init__(self):
        global geo, catalog
        geo = Geoserver(Config.GEOSERVER_URL, Config.GEOSERVER_USER, Config.GEOSERVER_PASSWD)
        catalog = Catalog(Config.GEOSERVER_URL + '/rest', Config.GEOSERVER_USER, Config.GEOSERVER_PASSWD)

    def create_workspace(self, name):
        try:
            geo.create_workspace(workspace=name)
            ws = catalog.get_workspace(name)
            return ws
        except Exception as e:
            return e


    def publish_pglayer(self, store, pg_table, workspace):
        try:
            geo.publish_featurestore(store, pg_table, workspace)
            layer = catalog.get_layer(workspace + ':' + pg_table)
            return layer
        except Exception as e:
            return print(e)

    def create_feature_store(self, store_name, workspace, db, host, port, schema, pg_user, pg_password):
        result = geo.create_featurestore(store_name=store_name,
                                         workspace=workspace,
                                         db=db,
                                         host=host,
                                         port=port,
                                         schema=schema,
                                         pg_user=pg_user,
                                         pg_password=pg_password)
        return result
