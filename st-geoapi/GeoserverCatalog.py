from geoserver.catalog import Catalog
from Config import Config

catalog = None


class GeoserverCatalog:
    def __init__(self):
        global catalog
        catalog = Catalog(Config.GEOSERVER_URL + '/rest',
                          Config.GEOSERVER_USER, Config.GEOSERVER_PASSWD)

    def getLayers(self):
        return catalog.get_layers()

    def getLayer(self, workspace, pg_table):
        return catalog.get_layer(workspace + ':' + pg_table)

    def get_stores(self, names, workspace):
        return catalog.get_stores(names, workspace)

    def get_store(self, names):
        return catalog.get_store(names)

    def create_style(self, name, sld, create, workspace):
        return catalog.create_style(name, sld, overwrite=create, workspace=workspace)

    def get_styles(self):
        return catalog.get_styles()

    def get_style(self, name):
        return catalog.get_style(name)

    def set_layer_style(self, workspace, tablename, stylename):
        try:
            layer = self.getLayer(workspace, tablename)

            styles = catalog.get_styles()
            selected_style = None
            for stl in styles:
                if stl.name == stylename:
                    selected_style = stl
                    break

            if layer and selected_style:
                layer.default_style = selected_style
                catalog.save(layer)
                return True
        except Exception as e:
            return e.args[0]

    def getWorkspace(self, name):
        return catalog.get_workspace(name)

    def create_datastore(self, name, workspace, host, port, database, user, passwd, dbtype):
        try:
            ds = catalog.create_datastore(name, workspace)
            ds.connection_parameters.update(
                host=host,
                port=port,
                database=database,
                user=user,
                passwd=passwd,
                type=dbtype)
            catalog.save(ds)
            ds = catalog.get_store(name)
        except Exception as e:
            return e.args[0]
        return ds

    def publish_featuretype(self, store, table, native_srs, srs):
        try:
            print("store", store[0])
            if store[0]:
                ft = catalog.publish_featuretype(
                    table, store[0], native_srs, srs, jdbc_virtual_table=None)
                print(ft)
                return ft
        except Exception as e:
            return print(e)
