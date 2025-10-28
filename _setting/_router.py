from flask import jsonify
from _setting import (
    lm,
    lb,
    lc,
    al,
    style,
    google_upload,
    google_list,
)


def router(app):
    # setting
    @app.post("/setting/<subpath>")
    def router_setting(subpath):
        # lm
        if subpath == "lm":
            dic = lm.lm()
        if subpath == "lm_modal_exe":
            dic = lm.lm_modal_exe()
        # lc
        if subpath == "lc":
            dic = lc.lc()
        if subpath == "lc_modal_exe":
            dic = lc.lc_modal_exe()
        # lb
        if subpath == "lb":
            dic = lb.lb()
        if subpath == "lb_modal_exe":
            dic = lb.lb_modal_exe()
        # al
        if subpath == "al":
            dic = al.al()
        if subpath == "al_list":
            dic = al.al_list()
        if subpath == "al_del":
            dic = al.al_del()
        if subpath == "al_task":
            dic = al.al_task()
        # style
        if subpath == "style":
            dic = style.style()
        if subpath == "style_modal_exe":
            dic = style.style_modal_exe()
        # google upload/list
        if subpath == "google_upload":
            dic = google_upload.google_upload()
        if subpath == "google_list":
            dic = google_list.google_list()
        return jsonify(dic), 201

    # account file upload
    @app.post("/setting/file/upload/<subpath>")
    def router_setting_file_upload(subpath):
        if subpath == "google_upload_exe":
            dic = google_upload.google_upload_exe()
        return dic
