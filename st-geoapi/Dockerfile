FROM python:3.7.1
WORKDIR /app
ADD . /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update -y
RUN apt install -y gdal-bin python3-gdal libgdal-dev python3-pycurl
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}') --global-option=build_ext --global-option="-I/usr/include/gdal"
RUN pip install -r requirements.txt
CMD ["python","app.py"]
#CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "app:app"]
EXPOSE 5000
