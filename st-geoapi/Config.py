import os


class Config(object):
    DEBUG = False
    JSON_AS_ASCII = False
    GEOSERVER_URL = os.environ.get("GEOSERVER_URL")
    GEOSERVER_GC_URL = os.environ.get("GEOSERVER_GC_URL")
    GEOSERVER_USER = os.environ.get("GEOSERVER_USER")
    GEOSERVER_PASSWD = os.environ.get("GEOSERVER_PASSWD")

    GEOSERVER_PUBLIC_URL = os.environ.get("GEOSERVER_PUBLIC_URL")
    GEOSERVER_GC_PUBLIC_URL = os.environ.get("GEOSERVER_GC_PUBLIC_URL")

    MAPSTORE_URL = os.environ.get("MAPSTORE_URL")
    MAPSTORE_USER = os.environ.get("MAPSTORE_USER")
    MAPSTORE_PASSWD = os.environ.get("MAPSTORE_PASSWD")

    MAPSTORE_PUBLIC_URL = os.environ.get("MAPSTORE_PUBLIC_URL")
