import sys
from flask import request
from _mod import mod_base

from .sql2fst import (
    com_al,
    com_config,
    com_device,
    com_lb,
    com_lc,
    com_lm,
    com_lm_level,
    com_lm_section,
    com_onoff,
    com_style,
)


# start
def main():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # dic
    dic = {
        "level_error": level_error,
    }
    return dic


# exe
def exe():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]
    exe = obj["exe"]

    # base - level 9
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # write
    if level_error == "error":
        dic = {
            "level_error": level_error,
        }
    else:
        # sql firestore
        sql_firestore(exe)

        dic = {
            "level_error": level_error,
        }
    return dic


# sql firestore
def sql_firestore(exe):
    # 関数を辞書にマッピング
    function_mapping = {
        # com
        "com_al": com_al.com_al,
        "com_config": com_config.com_config,
        "com_device": com_device.com_device,
        "com_lb": com_lb.com_lb,
        "com_lc": com_lc.com_lc,
        "com_lm": com_lm.com_lm,
        "com_lm_level": com_lm_level.com_lm_level,
        "com_lm_section": com_lm_section.com_lm_section,
        "com_onoff": com_onoff.com_onoff,
        "com_style": com_style.com_style,
    }

    # exeの値に基づいて適切な関数を実行
    if exe in function_mapping:
        function_mapping[exe]()
    return
