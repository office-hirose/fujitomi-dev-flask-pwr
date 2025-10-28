from flask import jsonify, make_response
from fee import (
    fee_stf,
    fee_total,
    fee_cre_month,
    fee_cre_month_keiri,
    fee_gyotei_list,
    fee_gyotei_keiri,
    fee_gyotei_sales,
    fee_nyu_hikaku,
    fee_chk,
    fee_chk_cre,
    fee_future,
    fee_future_cre,
    fee_find,
    fee_find_pdf,
    fee_find_excel,
)


def router(app):
    # fee
    @app.post("/fee/<subpath>")
    def router_fee(subpath):
        #
        if subpath == "stf":
            dic = fee_stf.fee_stf()
        if subpath == "stf_exe":
            dic = fee_stf.fee_stf_exe()
        if subpath == "stf_task":
            dic = fee_stf.fee_stf_task()
        #
        if subpath == "gyotei_list":
            dic = fee_gyotei_list.fee_gyotei_list()
        if subpath == "gyotei_list_exe":
            dic = fee_gyotei_list.fee_gyotei_list_exe()
        if subpath == "gyotei_list_task":
            dic = fee_gyotei_list.fee_gyotei_list_task()
        #
        if subpath == "gyotei_keiri":
            dic = fee_gyotei_keiri.fee_gyotei_keiri()
        if subpath == "gyotei_keiri_exe":
            dic = fee_gyotei_keiri.fee_gyotei_keiri_exe()
        if subpath == "gyotei_keiri_task":
            dic = fee_gyotei_keiri.fee_gyotei_keiri_task()
        #
        if subpath == "gyotei_sales":
            dic = fee_gyotei_sales.fee_gyotei_sales()
        if subpath == "gyotei_sales_exe":
            dic = fee_gyotei_sales.fee_gyotei_sales_exe()
        if subpath == "gyotei_sales_task":
            dic = fee_gyotei_sales.fee_gyotei_sales_task()
        #
        if subpath == "total":
            dic = fee_total.fee_total()
        if subpath == "total_exe":
            dic = fee_total.fee_total_exe()
        if subpath == "total_task":
            dic = fee_total.fee_total_task()
        #
        if subpath == "future":
            dic = fee_future.fee_future()
        if subpath == "future_exe":
            dic = fee_future.fee_future_exe()
        if subpath == "future_task":
            dic = fee_future.fee_future_task()
        #
        if subpath == "cre_month":
            dic = fee_cre_month.fee_cre_month()
        if subpath == "cre_month_exe":
            dic = fee_cre_month.fee_cre_month_exe()
        if subpath == "cre_month_task":
            dic = fee_cre_month.fee_cre_month_task()
        #
        if subpath == "cre_month_keiri":
            dic = fee_cre_month_keiri.fee_cre_month()
        if subpath == "cre_month_keiri_exe":
            dic = fee_cre_month_keiri.fee_cre_month_exe()
        if subpath == "cre_month_keiri_task":
            dic = fee_cre_month_keiri.fee_cre_month_task()
        #
        if subpath == "future_cre":
            dic = fee_future_cre.fee_future_cre()
        if subpath == "future_cre_exe":
            dic = fee_future_cre.fee_future_cre_exe()
        if subpath == "future_cre_task":
            dic = fee_future_cre.fee_future_cre_task()
        #
        if subpath == "nyu_hikaku":
            dic = fee_nyu_hikaku.fee_nyu_hikaku()
        if subpath == "nyu_hikaku_list":
            dic = fee_nyu_hikaku.fee_nyu_hikaku_list()
        if subpath == "nyu_hikaku_sai":
            dic = fee_nyu_hikaku.fee_nyu_hikaku_sai()
        #
        if subpath == "chk":
            dic = fee_chk.fee_chk()
        if subpath == "chk_exe":
            dic = fee_chk.fee_chk_exe()
        if subpath == "chk_task":
            dic = fee_chk.fee_chk_task()
        #
        if subpath == "chk_cre":
            dic = fee_chk_cre.fee_chk_cre()
        if subpath == "chk_cre_exe":
            dic = fee_chk_cre.fee_chk_cre_exe()
        if subpath == "chk_cre_task":
            dic = fee_chk_cre.fee_chk_cre_task()
        #
        if subpath == "find":
            dic = fee_find.fee_find()
        if subpath == "find_list":
            dic = fee_find.fee_find_list()
        if subpath == "find_search":
            dic = fee_find.fee_find_search()

        return jsonify(dic), 201

    # fee find pdf/fee find excel
    @app.post("/fee/find/<subpath>")
    def router_fee_find_download(subpath):
        if subpath == "pdf":
            create_file, mime_type, file_name = fee_find_pdf.fee_pdf()
        if subpath == "excel":
            create_file, mime_type, file_name = fee_find_excel.fee_excel()
        response = make_response()
        response.data = create_file
        response.headers["Content-Disposition"] = "attachment; filename=" + file_name
        response.mimetype = mime_type
        return response
