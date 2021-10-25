import requests
from requests.auth import HTTPBasicAuth
import json
import xmltodict
from GeoserverCatalog import GeoserverCatalog
from Config import Config
from urllib.parse import urlsplit
from osgeo import ogr
from osgeo import osr

set_up = None


class MapstoreService:
    def __init__(self):
        global set_up

    def login(self):
        try:
            user = Config.MAPSTORE_USER
            password = Config.MAPSTORE_PASSWD
            response = requests.post(Config.MAPSTORE_URL + "/session/login", auth=HTTPBasicAuth(user, password),
                                     data={})
            response_data = json.loads(response.text)
            print(response_data)
            return response_data
        except Exception as e:
            return e.args[0]

    def get_maps(self, access_token):
        try:
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/xml'
            }
            response = requests.get(Config.MAPSTORE_URL + "/extjs/search/category/MAP",
                                    headers=headers,
                                    data={})
            response_data = json.loads(response.text)
            return response_data
        except Exception as e:
            return e.args[0]

    def get_usergroups(self, access_token):
        try:
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json'
            }
            response = requests.get(Config.MAPSTORE_URL + "/usergroups/?all=true&users=false",
                                    headers=headers,
                                    data={})
            xmldict = xmltodict.parse(response.text)
            user_group = xmldict['UserGroupList']['UserGroup']
            return user_group
        except Exception as e:
            return e.args[0]

    def modify_map_permissions(self, access_token, id, groupname):
        try:
            groupname_id = None
            usergroups = self.get_usergroups(access_token)
            for group in usergroups:
                if group['groupName'] == groupname:
                    groupname_id = group['id']

            if groupname_id is None:
                return False

            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/xml'
            }
            payload = '''
               <SecurityRuleList>
                    <SecurityRule>
                        <canRead>true</canRead>
                        <canWrite>false</canWrite>
                        <group>
                            <id>''' + groupname_id + '''</id>
                            <groupName>''' + groupname + '''</groupName>
                        </group>
                    </SecurityRule>
               </SecurityRuleList>
                '''

            response = requests.post(Config.MAPSTORE_URL + '/resources/resource/' + id + '/permissions',
                                     headers=headers,
                                     data=payload)
            print(response)
            return response
        except Exception as e:
            return e.args[0]

    def create_map(self, access_token, catalog_name, catalog_title,
                   mapname, mapdescription,
                   layers, workspace):
        try:
            catalog_url = Config.GEOSERVER_GC_URL
            geoserver_catalog = GeoserverCatalog()
            av_styles = geoserver_catalog.get_styles()
            print(av_styles)
            avStyles_Arr = ''

            # print(avStyles_Arr)
            maxX = []
            maxY = []
            minX = []
            minY = []
            url_layer = Config.GEOSERVER_GC_URL
            postgis_layers = ''
            for layer in layers:

                ly = geoserver_catalog.getLayer(workspace, layer['tablename'])
                if ly:
                    layer_data = geoserver_catalog.getLayer(
                        workspace, layer['tablename'])  # Return Layer data

                    projection = layer_data.resource.projection
                    bounds = layer_data.resource.latlon_bbox
                    maxX.append(float(bounds[1]))
                    maxY.append(float(bounds[3]))
                    minX.append(float(bounds[0]))
                    minY.append(float(bounds[2]))

                    for avArr in av_styles:
                        if avArr is not None and avArr.name == layer['style']:
                            print(avArr.workspace)
                            work = ''
                            if avArr.workspace == None:
                                work = ''
                            else:
                                work = avArr.workspace

                            avStyles_Arr += '''{
                              "TYPE_NAME": "WMS_1_3_0.Style",
                                  "name": "'''+avArr.name + '''",
                                  "title": "'''+avArr.name + '''",

                              "workspace": {
                                                        "name": "'''+work + '''"
                                                    },
                              "format": "sld",
                                  "languageVersion": {
                                                        "version": "1.0.0"
                                                    },
                              "filename": "'''+avArr.filename+'''"
                                } '''

                        break
                    # print(avStyles_Arr)
                    # avStyles_Arr = avStyles_Arr[:-1]

                    # centerx = (bounds[0]) + (bounds[1])) / 2
                    # centery = ((bounds[2])+(bounds[3]))/2
                    postgis_layers += '''{
                                    "id": "''' + layer['tablename'] + '''",
                                    "format": "image/png",
                                    "search": {
                                    "url": "'''+Config.GEOSERVER_PUBLIC_URL + '''/wfs",
                                    "type": "wfs"
                                  },
                                    "name": "''' + layer['tablename'] + '''",
                                    "description": "''' + layer['tablename'] + '''",
			                              "style": "'''+layer['style'] + '''",
                                    "availableStyles": ['''+avStyles_Arr+'''],
                                    "title": "''' + layer['title'] + '''",
                                    "type": "wms",
                                    "url": "''' + Config.GEOSERVER_PUBLIC_URL + '''/wms",
                                    "bbox": {
                                      "crs": "''' + projection + '''",
                                      "bounds": {
                                        "minx": "''' + str(bounds[0]) + '''",
                                        "miny": "''' + str(bounds[2]) + '''",
                                        "maxx": "''' + str(bounds[1]) + '''",
                                        "maxy": "''' + str(bounds[3]) + '''"
                                      }
                                    },
                                    "visibility": true,
                                    "singleTile": false,
                                    "allowedSRS": {
                                      "''' + projection + '''": true,
                                      "EPSG:3785":true,
                                      "EPSG:3857":true,
                                      "EPSG:4269":true,
                                      "EPSG:4326":true,
                                      "EPSG:102113":true,
                                      "EPSG:900913":true
                                    },

                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "catalogURL": null,
                                    "useForElevation": false,
                                    "hidden": false,
                                    "params": {}
                                  },'''
            postgis_layers = postgis_layers[:-1]  # Remove last comma
            print(maxX)
            maxX_total = maxX[0]
            maxY_total = maxY[0]
            minX_total = minX[0]
            minY_total = minY[0]
            for x in maxX:
                if x > maxX_total:
                    maxX_total = x
            for x in maxY:
                if x > maxY_total:
                    maxY_total = x
            for x in minX:
                if x > minX_total:
                    minX_total = x
            for x in minY:
                if x > minY_total:
                    minY_total = x

            centerx = (maxX_total + minX_total)
            centery = (maxY_total + minY_total)

            divx = centerx / 2
            print(divx)
            divy = centery / 2
            print(divy)
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/xml'
            }
            payload = '''
                  <Resource>
                    <description><![CDATA[''' + mapdescription + ''']]></description>
                    <metadata></metadata>
                    <name><![CDATA[''' + mapname + ''']]></name>
                    <category>
                        <name>MAP</name>
                    </category>
                    <Attributes>
                        <attribute>
                            <name>owner</name>
                            <value>admin</value>
                            <type>STRING</type>
                        </attribute>
                    </Attributes>
                    <store>
                        <data>
                            <![CDATA[{
                              "version": 2,
                              "map": {
                                "center": {
                                   "x": ''' + str(divx)+''',
                                  "y": '''+str(divy) + ''',
                                  "crs": "EPSG:4326"
                                },
                                "maxExtent": [
                                 -20037508.34,
                                  -20037508.34,
                                  20037508.34,
                                  20037508.34
                                ],
                                "projection": "EPSG:900913",
                                "units": "m",
                                "zoom": 11,
                                "mapOptions": {},
                                "layers": [
                                  {
                                    "id": "mapnik__0",
                                    "group": "background",
                                    "source": "osm",
                                    "name": "mapnik",
                                    "title": "Open Street Map",
                                    "type": "osm",
                                    "visibility": true,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "Night2012__1",
                                    "group": "background",
                                    "source": "nasagibs",
                                    "name": "Night2012",
                                    "provider": "NASAGIBS.ViirsEarthAtNight2012",
                                    "title": "NASAGIBS Night 2012",
                                    "type": "tileprovider",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "OpenTopoMap__2",
                                    "group": "background",
                                    "source": "OpenTopoMap",
                                    "name": "OpenTopoMap",
                                    "provider": "OpenTopoMap",
                                    "title": "OpenTopoMap",
                                    "type": "tileprovider",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "s2cloudless:s2cloudless__3",
                                    "format": "image/jpeg",
                                    "group": "background",
                                    "source": "s2cloudless",
                                    "name": "s2cloudless:s2cloudless",
                                    "opacity": 1,
                                    "title": "Sentinel 2 Cloudless",
                                    "type": "wms",
                                    "url": [
                                      "https://1maps.geo-solutions.it/geoserver/wms",
                                      "https://2maps.geo-solutions.it/geoserver/wms",
                                      "https://3maps.geo-solutions.it/geoserver/wms",
                                      "https://4maps.geo-solutions.it/geoserver/wms",
                                      "https://5maps.geo-solutions.it/geoserver/wms",
                                      "https://6maps.geo-solutions.it/geoserver/wms"
                                    ],
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "undefined__4",
                                    "group": "background",
                                    "source": "ol",
                                    "title": "Empty Background",
                                    "type": "empty",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },''' + postgis_layers + '''
                                ],
                                "groups": [
                                  {
                                    "id": "Default",
                                    "title": "Default",
                                    "expanded": true
                                  }
                                ],
                                "backgrounds": []
                              },
                              "catalogServices": {
                                "services": {
                                 "GeoAPI WMS Service": {
                                    "url": "''' + Config.GEOSERVER_PUBLIC_URL + '''/wms",
                                    "type": "wms",
                                    "title": "WMS Service",
                                    "autoload": false,
                                    "showAdvancedSettings": false,
                                    "showTemplate": false,
                                    "hideThumbnail": false,
                                    "metadataTemplate": "<p></p>"
                                  }
                                },
                                "selectedService": "GeoAPI WMS Service"
                              },
                              "widgetsConfig": {
                                "layouts": {
                                  "md": [],
                                  "xxs": []
                                }
                              },
                              "mapInfoConfiguration": {},
                              "dimensionData": {},
                              "timelineData": {}
                           }]]></data>
                    </store>
                </Resource>
                '''

            print(payload)
            response = requests.post(Config.MAPSTORE_URL + "/resources",
                                     headers=headers,
                                     data=payload)
            return response
        except Exception as e:
            return e.args[0]

    def create_mapmultiplebds(self, access_token, mapname, mapdescription, workspaces, catalog_name, catalog_title):
        try:
            catalog_url = Config.GEOSERVER_GC_URL
            geoserver_catalog = GeoserverCatalog()
            av_styles = geoserver_catalog.get_styles()
            avStyles_Arr = ''

            # print(avStyles_Arr)
            maxX = []
            maxY = []
            minX = []
            minY = []
            url_layer = Config.GEOSERVER_GC_URL
            postgis_layers = ''

            for workspace in workspaces:

                for layer in workspace['layers']:

                    ly = geoserver_catalog.getLayer(
                        workspace['name'], layer['tablename'])

                    if ly:
                        layer_data = geoserver_catalog.getLayer(
                            workspace['name'],  layer['tablename'])  # Return Layer data
                        print(layer_data)
                        projection = layer_data.resource.projection
                        bounds = layer_data.resource.latlon_bbox
                        maxX.append(float(bounds[1]))
                        maxY.append(float(bounds[3]))
                        minX.append(float(bounds[0]))
                        minY.append(float(bounds[2]))

                        # centerx = (bounds[0]) + (bounds[1])) / 2
                        # centery = ((bounds[2])+(bounds[3]))/2
                        postgis_layers += '''{
                                    "id": "''' + layer['tablename'] + '''",
                                    "format": "image/png",
                                    "search": {
                                    "url": "'''+Config.GEOSERVER_PUBLIC_URL + '''/wfs",
                                    "type": "wfs"
                                  },
                                    "name": "''' + layer['tablename'] + '''",
                                    "description": "''' + layer['tablename'] + '''",
			                              "style": "'''+layer['style'] + '''",
                                    "availableStyles": ['''+avStyles_Arr+'''],
                                    "title": "''' + layer['title'] + '''",
                                    "type": "wms",
                                    "url": "''' + Config.GEOSERVER_PUBLIC_URL + '''/wms",
                                    "bbox": {
                                      "crs": "''' + projection + '''",
                                      "bounds": {
                                        "minx": "''' + str(bounds[0]) + '''",
                                        "miny": "''' + str(bounds[2]) + '''",
                                        "maxx": "''' + str(bounds[1]) + '''",
                                        "maxy": "''' + str(bounds[3]) + '''"
                                      }
                                    },
                                    "visibility": true,
                                    "singleTile": false,
                                    "allowedSRS": {
                                      "''' + projection + '''": true,
                                      "EPSG:3785":true,
                                      "EPSG:3857":true,
                                      "EPSG:4269":true,
                                      "EPSG:4326":true,
                                      "EPSG:102113":true,
                                      "EPSG:900913":true
                                    },

                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "catalogURL": null,
                                    "useForElevation": false,
                                    "hidden": false,
                                    "params": {}
                                  },'''
            postgis_layers = postgis_layers[:-1]  # Remove last comma
            print(maxX)

            maxX_total = maxX[0]
            maxY_total = maxY[0]
            minX_total = minX[0]
            minY_total = minY[0]
            for x in maxX:
                if x > maxX_total:
                    maxX_total = x
            for x in maxY:
                if x > maxY_total:
                    maxY_total = x
            for x in minX:
                if x > minX_total:
                    minX_total = x
            for x in minY:
                if x > minY_total:
                    minY_total = x

            centerx = (maxX_total + minX_total)
            centery = (maxY_total + minY_total)

            divx = centerx / 2
            print(divx)
            divy = centery / 2
            print(divy)
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/xml'
            }
            payload = '''
                  <Resource>
                    <description><![CDATA[''' + mapdescription + ''']]></description>
                    <metadata></metadata>
                    <name><![CDATA[''' + mapname + ''']]></name>
                    <category>
                        <name>MAP</name>
                    </category>
                    <Attributes>
                        <attribute>
                            <name>owner</name>
                            <value>admin</value>
                            <type>STRING</type>
                        </attribute>
                    </Attributes>
                    <store>
                        <data>
                            <![CDATA[{
                              "version": 2,
                              "map": {
                                "center": {
                                   "x": ''' + str(divx)+''',
                                  "y": '''+str(divy) + ''',
                                  "crs": "EPSG:4326"
                                },
                                "maxExtent": [
                                 -20037508.34,
                                  -20037508.34,
                                  20037508.34,
                                  20037508.34
                                ],
                                "projection": "EPSG:900913",
                                "units": "m",
                                "zoom": 11,
                                "mapOptions": {},
                                "layers": [
                                  {
                                    "id": "mapnik__0",
                                    "group": "background",
                                    "source": "osm",
                                    "name": "mapnik",
                                    "title": "Open Street Map",
                                    "type": "osm",
                                    "visibility": true,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "Night2012__1",
                                    "group": "background",
                                    "source": "nasagibs",
                                    "name": "Night2012",
                                    "provider": "NASAGIBS.ViirsEarthAtNight2012",
                                    "title": "NASAGIBS Night 2012",
                                    "type": "tileprovider",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "OpenTopoMap__2",
                                    "group": "background",
                                    "source": "OpenTopoMap",
                                    "name": "OpenTopoMap",
                                    "provider": "OpenTopoMap",
                                    "title": "OpenTopoMap",
                                    "type": "tileprovider",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "s2cloudless:s2cloudless__3",
                                    "format": "image/jpeg",
                                    "group": "background",
                                    "source": "s2cloudless",
                                    "name": "s2cloudless:s2cloudless",
                                    "opacity": 1,
                                    "title": "Sentinel 2 Cloudless",
                                    "type": "wms",
                                    "url": [
                                      "https://1maps.geo-solutions.it/geoserver/wms",
                                      "https://2maps.geo-solutions.it/geoserver/wms",
                                      "https://3maps.geo-solutions.it/geoserver/wms",
                                      "https://4maps.geo-solutions.it/geoserver/wms",
                                      "https://5maps.geo-solutions.it/geoserver/wms",
                                      "https://6maps.geo-solutions.it/geoserver/wms"
                                    ],
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },
                                  {
                                    "id": "undefined__4",
                                    "group": "background",
                                    "source": "ol",
                                    "title": "Empty Background",
                                    "type": "empty",
                                    "visibility": false,
                                    "singleTile": false,
                                    "dimensions": [],
                                    "hideLoading": false,
                                    "handleClickOnLayer": false,
                                    "useForElevation": false,
                                    "hidden": false
                                  },''' + postgis_layers + '''
                                ],
                                "groups": [
                                  {
                                    "id": "Default",
                                    "title": "Default",
                                    "expanded": true
                                  }
                                ],
                                "backgrounds": []
                              },
                              "catalogServices": {
                                "services": {
                                 "GeoAPI WMS Service": {
                                    "url": "''' + Config.GEOSERVER_PUBLIC_URL + '''/wms",
                                    "type": "wms",
                                    "title": "WMS Service",
                                    "autoload": false,
                                    "showAdvancedSettings": false,
                                    "showTemplate": false,
                                    "hideThumbnail": false,
                                    "metadataTemplate": "<p></p>"
                                  }
                                },
                                "selectedService": "GeoAPI WMS Service"
                              },
                              "widgetsConfig": {
                                "layouts": {
                                  "md": [],
                                  "xxs": []
                                }
                              },
                              "mapInfoConfiguration": {},
                              "dimensionData": {},
                              "timelineData": {}
                           }]]></data>
                    </store>
                </Resource>
                '''

            print(payload)
            response = requests.post(Config.MAPSTORE_URL + "/resources",
                                     headers=headers,
                                     data=payload)
            return response
        except Exception as e:
            return e.args[0]

    def getMapByName(self, name, data):
        if isinstance(data, dict):
            if data['name'] == name:
                url = urlsplit(Config.MAPSTORE_URL)
                map_link = url.scheme + '://' + url.netloc + \
                    '/#/viewer/openlayers/' + str(data['id'])
                data['map_link'] = map_link
                return data

        if isinstance(data, list):
            for map in data:
                if map['name'] == name:
                    url = urlsplit(Config.MAPSTORE_URL)
                    map_link = url.scheme + '://' + url.netloc + \
                        '/#/viewer/openlayers/' + str(map['id'])
                    map['map_link'] = map_link
                    return map
