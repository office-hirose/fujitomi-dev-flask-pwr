from flask import jsonify
from _auth import auth


def router(app):
    # top
    @app.route("/")
    def router_top():
        return "run"

    # auth google signin signout
    @app.post("/auth/<subpath>")
    def router_auth(subpath):
        if subpath == "google_signin":
            dic = auth.google_signin()
        if subpath == "google_signout":
            dic = auth.google_signout()
        if subpath == "update_local_storage":
            dic = auth.update_local_storage()
        return jsonify(dic), 201
