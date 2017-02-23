# this image already has all the tools this utility uses.
FROM kartoza/qgis-base

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y spatialite-bin

RUN mkdir -p /zipzones/data
WORKDIR /zipzones/data
RUN git clone https://github.com/wboykinm/ophz.git
RUN spatialite_tool -i -shp /zipzones/data/ophz/ophz-c/ophz-c -d /zipzones/data/shapes.sqlite -t zoneshapes -c UTF8

RUN git clone https://gist.github.com/7882666.git zips2latlng
RUN cp "/zipzones/data/zips2latlng/US Zip Codes from 2013 Government Data" /zipzones/data/zips2latlng/zip2latlong.csv

# mount this repo directory to /zipzones/app
RUN mkdir -p /zipzones/app
WORKDIR /zipzones/app
COPY . /zipzones/app

RUN mkdir -p /zipzones/build

CMD ["/zipzones/app/zipzones.py", "/zipzones/data/zips2latlng/zip2latlong.csv"]
