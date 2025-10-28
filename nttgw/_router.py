from flask import jsonify
from nttgw import (
    nttgw_create_file,
    nttgw_create_file_move_file,
    nttgw_create_file_create_file,
    nttgw_upload_chk,
    nttgw_upload_exe,
    nttgw_update,
    nttgw_bosyu,
    nttgw_kei,
    nttgw_store,
    nttgw_kikan,
    nttgw_teikei,
    nttgw_other,
    nttgw_keijyo,
    nttgw_hojin_kojin,
    nttgw_email,
    nttgw_not_store,
)


def router(app):
    # nttgw
    @app.post("/nttgw/<subpath>")
    def router_nttgw(subpath):
        if subpath == "upload_zip_exe":
            dic = nttgw_create_file.upload_zip_exe()

        if subpath == "create_file_start":
            dic = nttgw_create_file.create_file_start()
        if subpath == "count_file_exe":
            dic = nttgw_create_file.count_file_exe()

        if subpath == "move_file_exe":
            dic = nttgw_create_file.move_file_exe()
        if subpath == "move_file_task":
            dic = nttgw_create_file_move_file.move_file_task()

        if subpath == "create_file_exe":
            dic = nttgw_create_file.create_file_exe()
        if subpath == "create_file_task":
            dic = nttgw_create_file_create_file.create_file_task()

        if subpath == "backup_delete_exe":
            dic = nttgw_create_file.backup_delete_exe()

        if subpath == "empty_trash_exe":
            dic = nttgw_create_file.empty_trash_exe()

        if subpath == "upload_chk":
            dic = nttgw_upload_chk.nttgw_upload_chk()
        if subpath == "upload_chk_exe":
            dic = nttgw_upload_chk.nttgw_upload_chk_exe()

        if subpath == "upload_exe":
            dic = nttgw_upload_exe.nttgw_upload_exe()
        if subpath == "upload_exe_exe":
            dic = nttgw_upload_exe.nttgw_upload_exe_exe()

        if subpath == "update":
            dic = nttgw_update.nttgw_update()
        if subpath == "update_cnt":
            dic = nttgw_update.nttgw_update_cnt()
        if subpath == "update_exe":
            dic = nttgw_update.nttgw_update_exe()
        if subpath == "update_task":
            dic = nttgw_update.nttgw_update_task()

        if subpath == "bosyu":
            dic = nttgw_bosyu.nttgw_bosyu()
        if subpath == "bosyu_list":
            dic = nttgw_bosyu.nttgw_bosyu_list()
        if subpath == "bosyu_update":
            dic = nttgw_bosyu.nttgw_bosyu_update()
        if subpath == "bosyu_update_all":
            dic = nttgw_bosyu.nttgw_bosyu_update_all()

        if subpath == "kei":
            dic = nttgw_kei.nttgw_kei()
        if subpath == "kei_list":
            dic = nttgw_kei.nttgw_kei_list()
        if subpath == "kei_modal_open":
            dic = nttgw_kei.nttgw_kei_modal_open()
        if subpath == "kei_modal_update":
            dic = nttgw_kei.nttgw_kei_modal_update()

        if subpath == "store":
            dic = nttgw_store.nttgw_store()
        if subpath == "store_cnt":
            dic = nttgw_store.nttgw_store_cnt()
        if subpath == "store_exe":
            dic = nttgw_store.nttgw_store_exe()
        if subpath == "store_task":
            dic = nttgw_store.nttgw_store_task()

        if subpath == "kikan":
            dic = nttgw_kikan.nttgw_kikan()
        if subpath == "kikan_list":
            dic = nttgw_kikan.nttgw_kikan_list()
        if subpath == "modal_hoken_kikan_keiyaku_list":
            dic = nttgw_kikan.nttgw_modal_hoken_kikan_keiyaku_list()
        if subpath == "modal_kikan_update":
            dic = nttgw_kikan.nttgw_modal_kikan_update()

        if subpath == "teikei":
            dic = nttgw_teikei.nttgw_teikei()
        if subpath == "teikei_list":
            dic = nttgw_teikei.nttgw_teikei_list()

        if subpath == "other":
            dic = nttgw_other.nttgw_other()
        if subpath == "other_list":
            dic = nttgw_other.nttgw_other_list()
        if subpath == "other_kind_modal_open":
            dic = nttgw_other.nttgw_other_kind_modal_open()
        if subpath == "other_kind_modal_update":
            dic = nttgw_other.nttgw_other_kind_modal_update()

        if subpath == "keijyo":
            dic = nttgw_keijyo.nttgw_keijyo()
        if subpath == "keijyo_list":
            dic = nttgw_keijyo.nttgw_keijyo_list()
        if subpath == "keijyo_update":
            dic = nttgw_keijyo.nttgw_keijyo_update()

        if subpath == "hojin_kojin":
            dic = nttgw_hojin_kojin.nttgw_hojin_kojin()
        if subpath == "hojin_kojin_list":
            dic = nttgw_hojin_kojin.nttgw_hojin_kojin_list()
        if subpath == "hojin_kojin_update":
            dic = nttgw_hojin_kojin.nttgw_hojin_kojin_update()

        if subpath == "email":
            dic = nttgw_email.nttgw_email()
        if subpath == "email_exe":
            dic = nttgw_email.nttgw_email_exe()
        if subpath == "email_task":
            dic = nttgw_email.nttgw_email_task()

        if subpath == "not_store":
            dic = nttgw_not_store.nttgw_not_store()
        if subpath == "not_store_cnt":
            dic = nttgw_not_store.nttgw_not_store_cnt()
        if subpath == "not_store_exe":
            dic = nttgw_not_store.nttgw_not_store_exe()

        return jsonify(dic), 201
