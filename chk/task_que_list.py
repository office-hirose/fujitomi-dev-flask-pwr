# 現時点ではqueの稼働状況などが取れないので使用していない
# source
# https://cloud.google.com/tasks/docs/samples/cloud-tasks-list-queues?hl=ja#cloud_tasks_list_queues-python

import sys
from flask import request
from _mod import fs_config, mod_base
from google.cloud import tasks_v2


def task_que_list():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "task_que_data": [],
        }
    else:
        # init
        project = fs_dic["project_name"]
        location = fs_dic["que_location"]

        client = tasks_v2.CloudTasksClient()
        parent = "projects/" + project + "/locations/" + location
        response = client.list_queues(request={"parent": parent})

        # set dic
        que_list = []
        for dt in response:
            temp_dic = {}
            temp_dic["name"] = str(dt.name)
            temp_dic["state"] = str(dt.state)
            que_list.append(temp_dic)

        dic = {
            "level_error": level_error,
            "task_que_data": que_list,
        }
    return dic
