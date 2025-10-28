from flask import jsonify
from sum import sum_stf, sum_total, sum_list, sum_cre


def router(app):
    # sum
    @app.post("/sum/<subpath>")
    def router_sum(subpath):
        if subpath == "stf":
            dic = sum_stf.sum_stf()
        if subpath == "stf_exe":
            dic = sum_stf.sum_stf_exe()
        if subpath == "stf_task":
            dic = sum_stf.sum_stf_task()
        if subpath == "total":
            dic = sum_total.sum_total()
        if subpath == "total_exe":
            dic = sum_total.sum_total_exe()
        if subpath == "total_task":
            dic = sum_total.sum_total_task()
        if subpath == "list":
            dic = sum_list.sum_list()
        if subpath == "list_exe":
            dic = sum_list.sum_list_exe()
        if subpath == "list_task":
            dic = sum_list.sum_list_task()
        if subpath == "cre":
            dic = sum_cre.sum_cre()
        if subpath == "cre_exe":
            dic = sum_cre.sum_cre_exe()
        if subpath == "cre_task":
            dic = sum_cre.sum_cre_task()
        return jsonify(dic), 201
