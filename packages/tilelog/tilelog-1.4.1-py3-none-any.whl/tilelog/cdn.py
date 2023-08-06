# Functions for internal use related to reporting on CDN health
# These are not automatically built on planet.osm.org

import click
import csv
import datetime
import re

import tilelog.constants


def pop_latency_logs(curs, date, dest):
    click.echo("Querying for POP latency")
    query="""
SELECT
datacenter,
CAST(approx_percentile(duration, 0.50) AS decimal(38,3))/1000 AS hit_p50,
CAST(approx_percentile(duration, 0.75) AS decimal(38,3))/1000 AS hit_p75,
CAST(approx_percentile(duration, 0.95) AS decimal(38,3))/1000 AS hit_p95,
CAST(approx_percentile(duration, 0.99) AS decimal(38,3))/1000 AS hit_p99,
CAST(approx_percentile(duration, 0.999) AS decimal(38,3))/1000 AS "hit_p99.9"
FROM {tablename}
WHERE year = %(year)d
    AND month = %(month)d
    AND day = %(day)d
    AND cachehit = 'HIT'
GROUP BY datacenter
ORDER BY datacenter
""".format(tablename=tilelog.constants.FASTLY_PARQET_LOGS)
    curs.execute(query, {"year": date.year, "month": date.month,
                         "day": date.day})
    click.echo("Writing pop latency to file")
    fieldnames=['datacenter', 'p50', 'p75', 'p95', 'p99', 'p99.9']
    csvwriter = csv.writer(dest, dialect=csv.unix_dialect,
                               quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerow(fieldnames)
    csvwriter.writerows(curs)
