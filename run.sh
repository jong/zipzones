#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker run --env="ZIPZONES_DESTINATION_FILE=/zipzones/build/zipzones.json" -v $DIR:/zipzones/build -it zipzones
