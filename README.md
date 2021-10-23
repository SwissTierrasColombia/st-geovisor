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

6.- Good luck !!

