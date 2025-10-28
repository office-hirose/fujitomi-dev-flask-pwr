from flask import jsonify
from keijyo import keijyo_list, keijyo_list_all


def router(app):
    # keijyo
    @app.post("/keijyo/<subpath>")
    def router_keijyo(subpath):
        if subpath == "list":
            dic = keijyo_list.keijyo_list()
        if subpath == "list_exe":
            dic = keijyo_list.keijyo_list_exe()
        if subpath == "list_task":
            dic = keijyo_list.keijyo_list_task()
        if subpath == "list_all":
            dic = keijyo_list_all.keijyo_list_all()
        if subpath == "list_all_exe":
            dic = keijyo_list_all.keijyo_list_all_exe()
        if subpath == "list_all_task":
            dic = keijyo_list_all.keijyo_list_all_task()
        return jsonify(dic), 201
