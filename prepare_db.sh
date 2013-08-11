#!/bin/sh
set -o history -o histexpand

function pause() {
   read -p "$* [enter]"
}

pause 'collect sql from dropbox to the single file (/tmp/prepare.sql)'
gzcat ~/Dropbox/Icfp2013/problems_index/problem.*.sql.gz > /tmp/prepare.sql;

pause 'truncate db'
psql -d icfp2013_01 -qc 'truncate table program; truncate table inputs;'

pause 'insert data'
psql -d icfp2013_01 -q -f /tmp/prepare.sql

pause 'cleanup'
rm /tmp/prepare.sql

