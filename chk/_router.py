from flask import jsonify
from chk import (
    task,
    dup,
    mistake,
    retiree,
    space_order,
    space_fee,
    allocation,
    oyaeda,
    fee_store,
)


def router(app):
    # check, task, dup, mistake
    @app.post("/chk/<subpath>")
    def router_chk(subpath):
        if subpath == "task":
            dic = task.task()
        if subpath == "task_del":
            dic = task.task_del()

        if subpath == "dup":
            dic = dup.dup()
        if subpath == "dup_modal":
            dic = dup.modal_dup_data()
        if subpath == "dup_modal_del":
            dic = dup.modal_dup_data_del()

        if subpath == "mistake":
            dic = mistake.mistake()
        if subpath == "mistake_modal":
            dic = mistake.modal_mistake_data()
        if subpath == "mistake_modal_del":
            dic = mistake.modal_mistake_data_del()

        if subpath == "retiree":
            dic = retiree.retiree()

        if subpath == "space_order":
            dic = space_order.space_order()

        if subpath == "space_fee":
            dic = space_fee.space_fee()

        if subpath == "allocation":
            dic = allocation.allocation()

        if subpath == "oyaeda":
            dic = oyaeda.oyaeda()

        # sql_fee_store 検索
        if subpath == "fee_store_sch":
            dic = fee_store.fee_store_sch()

        if subpath == "fee_store_modal_exe":
            dic = fee_store.fee_store_modal_exe()

        return jsonify(dic), 201
