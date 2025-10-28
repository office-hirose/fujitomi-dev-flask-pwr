from flask import jsonify
from search import kei_name_sch


def router(app):
    # search
    @app.post("/search/<subpath>")
    def router_search(subpath):
        if subpath == "kei_name_sch":
            dic = kei_name_sch.kei_name_sch()
        if subpath == "kei_name_sch_list":
            dic = kei_name_sch.kei_name_sch_list()
        return jsonify(dic), 201
