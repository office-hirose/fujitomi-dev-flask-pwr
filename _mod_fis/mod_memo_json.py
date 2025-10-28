import json
from _mod import mod_datetime


def mz_memo_json(user_email, moto_memo, moto_memo_json):
    if moto_memo == "":
        res_memo = ""
        res_memo_json = moto_memo_json
    else:
        dic_memo = {
            "text": moto_memo,
            "user_email": user_email,
            "update_time": mod_datetime.mz_tnow("for_datetime"),
        }
        temp_list = []
        temp_list.append(dic_memo)

        # 戦闘に追加する場合
        res_memo = ""
        moto_memo_json = json.loads(moto_memo_json)
        moto_memo_json[0:0] = temp_list
        res_memo_json = json.dumps(moto_memo_json)

        # 後ろに追加する場合
        # res_memo = ""
        # moto_memo_json = json.loads(moto_memo_json)
        # moto_memo_json.append(dic_memo)
        # res_memo_json = json.dumps(moto_memo_json)

    return res_memo, res_memo_json
