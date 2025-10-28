from flask import jsonify
from manki import manki_list, chk, chk_list, chk_modal


def router(app):
    # manki
    @app.post("/manki/<subpath>")
    def router_manki(subpath):
        # 満期リスト
        if subpath == "list":
            dic = manki_list.manki_list()
        if subpath == "list_exe":
            dic = manki_list.manki_list_exe()
        if subpath == "list_task":
            dic = manki_list.manki_list_task()

        # 満期チェック
        if subpath == "chk":
            dic = chk.manki()
        if subpath == "chk_list":
            dic = chk_list.manki_list()
        if subpath == "load_comment":
            dic = chk_modal.load_comment()
        if subpath == "add_comment":
            dic = chk_modal.add_comment()

        return jsonify(dic), 201
