import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from app import app
from app import db
import config

def query_db(query, args=(), one=False):
    #cur = get_db().execute(query, args)
    #SELECT * FROM my_table WHERE my_column = :val', {'val': 5}
    result = db.session.execute(query, args)
    db.session.commit()

    print(result)

    rv = [dict(r.items()) for r in result]
    print(query)
    print((rv[0] if rv else None) if one else rv)
    return (rv[0] if rv else None) if one else rv


def query_db_list(query, args=()):
    #cur = get_db().execute(query, args)
    #SELECT * FROM my_table WHERE my_column = :val', {'val': 5}
    result = db.session.execute(query, args)
    for r in result:
        print(r)
    result_list = [r for r in result]
    db.session.commit()
    return result_list


