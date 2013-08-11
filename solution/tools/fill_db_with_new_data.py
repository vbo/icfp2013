import os.path
from time import sleep
from glob import glob
import hashlib
import tempfile
from .. import db

from .fill_db import dropbox_directory

def ids():
    return db.fetchone("SELECT MAX(id) FROM program"), db.fetchone("SELECT MAX(id) FROM inputs")

if __name__ == '__main__':
    while True:
        mask = os.path.join(dropbox_directory, 'problem.*.sql.part.*')
        tmpdir = tempfile.gettempdir()
        globed = glob(mask)
        tmp = os.path.join(tmpdir, hashlib.md5("_".join(globed)).hexdigest() + ".sql")
        if globed:
            print "Got not empty dropbox dir:", globed
            p_id, i_id = ids()
            print "Current serials:", (p_id, i_id)
            print "Loading %s files to db" % (len(globed))
            cmd = "cat %s > %s && psql -d icfp2013_01 -q -f %s && mv %s /tmp/" % (mask, tmp, tmp, mask)
            print cmd
            os.system(cmd)
            new_p_id, new_i_id = ids()
            print "New serials:", (new_p_id, new_i_id)
            print "Added:", (new_p_id - p_id, new_i_id - i_id)
        sleep(5)


