FROM tomcat:9-jdk11-openjdk 
LABEL maintainer="Arturo Aranguren"

# Tomcat specific options
ENV CATALINA_BASE "$CATALINA_HOME"
ENV MAPSTORE_WEBAPP_DST="${CATALINA_BASE}/webapps"
ENV INITIAL_MEMORY="512m"
ENV MAXIMUM_MEMORY="2512m"
ENV JAVA_OPTS="${JAVA_OPTS} -Xms${INITIAL_MEMORY} -Xmx${MAXIMUM_MEMORY} -Djavax.xml.parsers.SAXParserFactory=com.sun.org.apache.xerces.internal.jaxp.SAXParserFactoryImpl"
ENV TERM xterm

COPY ./docker/mapstore.war "${MAPSTORE_WEBAPP_DST}/mapstore.war"



EXPOSE 8080
