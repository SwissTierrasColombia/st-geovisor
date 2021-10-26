##Pasos para la puesta en marcha

1.- Clone el repositorio

    git clone

    cd st-geovisor

2.- Copie el fichero de variables de entorno 

    cp Env-Sample .env

3.- Edite como minimo los parámetros del 
    GEOSERVER_PUBLIC_URL 
    MAPSTORE_PUBLIC_URL

4.- Revise los puertos definidos para cada servicio    
    GEOSERVER_PORT
    MAPSTORE_PORT
    GEOAPI_PORT

5.- Arranque los contendedores

    docker-compose up --build -d

6.- Si desea actualizar la API

    docker-compose stop geoapi
    docker-compose rm geoapi
    docker-compose build geoapi
    docker-compose up --no-start geoapi
    docker-compose start geoapi
    docker-compose logs geoapi


6.- Good luck !!


## Utilización: ejemplos 


//create fast context with one workspace
```
 curl "http://geoapi.denebinc.com/st_geocreatefastcontext" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{"name_conn": "aac4","store": "aac4","workspace": "Aac4","dbname": "armenia","host":"db","port":"5432","user": "docker","password": "docker", "schema": "integration","layers":[{"tablename": "construccion_insumos","style":"polygon","title":"Perímetros api"},{"tablename": "manzanas","style": "polygon",    "title":"titulo mapa api"},{"tablename": "perimetros","style":"polygon","title":"titulo mapa api"},{"tablename": "predios_integrados","style": "polygon",    "title":"titulo mapa api"},{"tablename": "veredas","style": "polygon","title":"titulo layer api"}]}
EOF
)
```


//create context fast from severals databases and creating one map
```
curl "http://geoapi.denebinc.com/st_geocreatefastcontextfewbds" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{"connections": [{"name_conn": "conexion","catalog_name": "prueba_fas11","catalog_title": "prueba_fast11","store": "geo_fast7","workspace": [{"name": "geo_fast7", "layers":[{"tablename": "construccion_insumos","style": "polygon","title":"Perímetros"},{"tablename": "manzanas","style": "polygon",                    "title":"titulo mapa api"},{"tablename": "perimetros","style": "polygon","title":"titulo mapa api"},{"tablename": "predios_integrados","style": "predio_historico",    "title":"titulo mapa api"},{"tablename":"veredas","style": "polygon","title":"titulo mapa api"}]}],"dbname": "armenia","host": "db","port": "5432","user": "docker",
"password": "docker","schema": "integration"},{"name_conn": "conexion2","catalog_name": "prueba_fast11","catalog_title": "prueba_fast11","store": "geo_fast2", "workspace":[{"name": "geo_fast2","layers":[{"tablename": "construccion_insumos","style": "polygon","title":"titulo mapa api"}]}],"dbname": "armenia","host": "db",
"port": "5432","user": "docker","password": "docker","schema": "integration"}],"map_name":"mapayad9","map_description":"mapa prueba api"

}
EOF
)
```

//create map
```
curl "http://geoapi.denebinc.com/st_geocreatemap" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{"workspace":"geo_fast7","map_name":"testapi3","map_description":"mapa","layers":[{"tablename": "construccion_insumos","style": "construccion_insumo",    "title":"titulo mapa api"},{"tablename":"manzanas","style":"manzana","title":"titulo mapa api"},{"tablename": "perimetros","style": "predio","title":"titulo mapa api"}, {"tablename": "predios_integrados","style": "predio","title":"titulo mapa api"},{"tablename": "veredas","style": "polygon","title":"titulo mapa api"}]}
EOF
)
```

 //create workspace

```
 curl "http://geoapi.denebinc.com/create_workspace" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{
    "name":"geoTestApi"
}
EOF
)
````

//create store

```
 curl "http://geoapi.denebinc.com/st_createstore" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{
"store_name":"geo_testapi",
"workspace":"geo_testapi",
"db_name":"armenia",
"host":"db",
"port":"5432",
"schema":"integration",
"pg_user":"docker",
"pg_password":"docker"
}
EOF
)
````


// publish feature type
```
 curl "http://geoapi.denebinc.com/publish_featuretype" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{
    "store":"geo_testapi",
    "workspace":"geo_testapi",
    "pg_table":"manzanas"
}
EOF
)
```

//create layer
```
 curl "http://geoapi.denebinc.com/st_geocreatelayer" -H "Accept: application/json" -H "Content-Type:application/json" --data @<(cat <<EOF
{
    "name":"layer_testapi",
    "workspace":"geo_testapi",
    "store":"geo_testapi",
    "table":"gc_construccion",
    "style":"construccion_insumos___b4acb9b0-2f3a-11ec-b6ba-f30df7d17559",
    "srs":"EPSG:9377"
}
EOF
)
```