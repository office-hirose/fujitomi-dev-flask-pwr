from flask import jsonify
from dwh import valid_conv


def router(app):
    # data ware house
    @app.post("/dwh/<subpath>")
    def router_dwh(subpath):
        if subpath == "valid_conv":
            dic = valid_conv.valid_conv()
        if subpath == "valid_conv_exe":
            dic = valid_conv.valid_conv_exe()
        if subpath == "valid_conv_task":
            dic = valid_conv.valid_conv_task()
        return jsonify(dic), 201
