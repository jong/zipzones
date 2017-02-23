#!/usr/bin/env python

import os
import sys
import pyspatialite.dbapi2 as db
import csv
import logging
import json

log = logging.getLogger('zipones')


def _get_rows(csv_filename):
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def _init_sqlite():
    conn = db.connect("/zipzones/data/shapes.sqlite")
    cursor = conn.execute('SELECT sqlite_version(), spatialite_version()')
    results = cursor.fetchall()
    assert results
    log.debug(results)
    return conn


def _get_zone(conn, row):
    log.debug('CSV Row: %s' % row)
    lat = float(row['LAT'].strip())
    lng = float(row['LNG'].strip())
    query = """
        SELECT z.zone, z.temp
        FROM zoneshapes z
        WHERE ST_Contains(z.Geometry, ST_Point({lng},{lat}))
        LIMIT 1
    """.format(
        lat=lat,
        lng=lng,
    )
    cursor = conn.execute(query)
    results = cursor.fetchall()
    item = dict(
        zip=row['ZIP'],
        latitude=lat,
        longitude=lng,
    )
    if results:
        zone, temp = results[0]
        item['zone'] = zone
        item['temp'] = temp
    else:
        item['zone'] = 'NO DATA'
        item['temp'] = 'NO DATA'
    return item


def main(csv_filename, destination_file):
    conn = _init_sqlite()

    # just empty out the file, surprise!
    with open(destination_file, 'w') as f:
        pass

    for row in _get_rows(csv_filename):
        try:
            item = _get_zone(conn, row)
        except KeyboardInterrupt:
            break
        except:
            log.exception('Problem getting zone for row, skipping.')
            continue
        with open(destination_file, 'a') as f:
            log.info('Zip: %s = %s' % (item['zip'], item['zone']))
            f.write(json.dumps(item, f))
            f.write("\n")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    csv_filename = sys.argv[1]

    destination_file = os.getenv('ZIPZONES_DESTINATION_FILE')
    main(csv_filename, destination_file)
