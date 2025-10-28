from flask import jsonify
from _conv import (
    fst2sql_main,
    sql2fst_main,
)


def router(app):
    # convert firestore to sql
    @app.post("/conv/fst2sql/<subpath>")
    def router_conv_fst2sql(subpath):
        # main
        if subpath == "main":
            dic = fst2sql_main.main()
        # exe
        if subpath == "exe":
            dic = fst2sql_main.exe()
        return jsonify(dic), 201

    # convert sql to firestore
    @app.post("/conv/sql2fst/<subpath>")
    def router_conv_sql2fst(subpath):
        # main
        if subpath == "main":
            dic = sql2fst_main.main()
        # exe
        if subpath == "exe":
            dic = sql2fst_main.exe()
        return jsonify(dic), 201
