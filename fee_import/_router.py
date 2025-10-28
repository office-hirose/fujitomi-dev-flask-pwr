# from flask import jsonify, make_response
from flask import jsonify

from fee_import import (
    fee_hikaku,
    fee_sheet_create,
    fee_sheet_check,
    fee_sheet_import,
    fee_delete_sql,
    fee_nyukin,
)


def router(app):
    # fee_import
    @app.post("/fee_import/<subpath>")
    def router_fee_import(subpath):
        if subpath == "hikaku":
            dic = fee_hikaku.fee_hikaku()

        if subpath == "hikaku_list":
            dic = fee_hikaku.fee_hikaku_list()

        if subpath == "modal_open":
            dic = fee_hikaku.modal_open()

        if subpath == "modal_update":
            dic = fee_hikaku.modal_update()

        if subpath == "fee_sheet_create":
            dic = fee_sheet_create.fee_sheet_create()

        if subpath == "fee_sheet_check":
            dic = fee_sheet_check.fee_sheet_check()

        if subpath == "fee_sheet_import":
            dic = fee_sheet_import.fee_sheet_import()

        if subpath == "fee_delete_sql_exe":
            dic = fee_delete_sql.fee_delete_sql_exe()

        # 入金金額更新
        if subpath == "modal_nyukin_update":
            dic = fee_nyukin.modal_nyukin_update()

        if subpath == "modal_nyukin_create":
            dic = fee_nyukin.modal_nyukin_create()

        return jsonify(dic), 201

    # fee file
    # @app.post("/fee_import/file/<subpath>")
    # def router_fee_import_file(subpath):
    # if subpath == "hikaku_xlsx":
    # create_file, mime_type, file_name = fee_hikaku.fee_hikaku_xlsx()

    # if subpath == "fee_pdf":
    #     create_file, mime_type, file_name = fee_find_pdf.fee_pdf()
    # if subpath == "fee_excel":
    #     create_file, mime_type, file_name = fee_find_excel.fee_excel()
    # return send_file(
    #     io.BytesIO(create_file), mimetype=mime_type, attachment_filename=file_name
    # )

    # response = make_response()
    # response.data = create_file
    # response.headers["Content-Disposition"] = "attachment; filename=" + file_name
    # response.mimetype = mime_type
    # return response
