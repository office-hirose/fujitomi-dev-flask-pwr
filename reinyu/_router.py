from flask import jsonify
from reinyu import reinyu_find


def router(app):
    # reinyu
    @app.post("/reinyu/<subpath>")
    def router_reinyu(subpath):
        if subpath == "find":
            dic = reinyu_find.reinyu_find()
        if subpath == "list":
            dic = reinyu_find.reinyu_find_list()
        if subpath == "search":
            dic = reinyu_find.reinyu_find_search()

        return jsonify(dic), 201
