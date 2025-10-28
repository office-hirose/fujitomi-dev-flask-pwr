from flask import jsonify, make_response
from mst import mst_coltd, mst_staff, mst_bosyu, mst_gyotei


def router(app):
    # mst
    @app.post("/mst/<subpath>")
    def router_mst(subpath):
        if subpath == "coltd":
            dic = mst_coltd.mst_coltd()
        if subpath == "coltd_modal_exe":
            dic = mst_coltd.mst_coltd_modal_exe()

        if subpath == "staff":
            dic = mst_staff.mst_staff()
        if subpath == "staff_modal_exe":
            dic = mst_staff.mst_staff_modal_exe()

        if subpath == "bosyu":
            dic = mst_bosyu.mst_bosyu()
        if subpath == "bosyu_modal_exe":
            dic = mst_bosyu.mst_bosyu_modal_exe()

        if subpath == "gyotei":
            dic = mst_gyotei.list()
        if subpath == "gyotei_modal_exe":
            dic = mst_gyotei.modal_exe()
        return jsonify(dic), 201

    # mst/file/download
    @app.post("/mst/file/download/<subpath>")
    def router_mst_file_download(subpath):
        if subpath == "gyotei_xlsx":
            create_file, mime_type, file_name = mst_gyotei.xlsx_download()
        response = make_response()
        response.data = create_file
        response.headers["Content-Disposition"] = "attachment; filename=" + file_name
        response.mimetype = mime_type
        return response
