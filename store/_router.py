from flask import jsonify, make_response
from store import (
    store,
    store_pdf,
    store_excel,
    store_modal_select,
    store_modal_insert,
    store_modal_update,
    gyotei,
)


def router(app):
    # store 生保/損保/少短
    @app.post("/store/normal/<subpath>")
    def router_store_normal(subpath):
        if subpath == "store":
            dic = store.store()
        if subpath == "list":
            dic = store.store_list()
        if subpath == "search":
            dic = store.store_search()
        return jsonify(dic), 201

    # store 業務提携
    @app.post("/store/gyotei/<subpath>")
    def router_store_gyotei(subpath):
        if subpath == "store":
            dic = gyotei.store()
        if subpath == "list":
            dic = gyotei.store_list()
        return jsonify(dic), 201

    # store file download pdf/excel
    @app.post("/store/file/download/<subpath>")
    def router_store_file_download(subpath):
        if subpath == "pdf":
            create_file, mime_type, file_name = store_pdf.store_pdf()
        if subpath == "excel":
            create_file, mime_type, file_name = store_excel.store_excel()
        response = make_response()
        response.data = create_file
        response.headers["Content-Disposition"] = "attachment; filename=" + file_name
        response.mimetype = mime_type
        return response

    # store normal modal
    @app.post("/store/normal/modal/<subpath>")
    def router_store_modal(subpath):
        if subpath == "select":
            dic = store_modal_select.store_modal_select()
        if subpath == "meisai":
            dic = store_modal_select.store_modal_meisai()
        if subpath == "nttgw":
            dic = store_modal_select.store_modal_nttgw()
        if subpath == "nttgw_import":
            dic = store_modal_select.store_modal_nttgw_import()
        if subpath == "insert":
            dic = store_modal_insert.store_modal_insert()
        if subpath == "update":
            dic = store_modal_update.store_modal_update()
        return jsonify(dic), 201
