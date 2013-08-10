import psycopg2

db = None


def query(sql, fill_data=tuple()):
    if not db:
        db = psycopg2.connect("dbname=icfp2013_01 user=vbo")
    cur = db.cursor()
    cur.execute(sql, fill_data)
    db.commit()
    return cur


def fetchone(sql, params=None):
    cur = query(sql, params)
    return cur.fetchone()[0]

