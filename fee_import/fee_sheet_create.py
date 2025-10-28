# -------------------------------------------------------------------
#  fee_sheet_create.py - Spread Sheetを作成する
# -------------------------------------------------------------------
import sys
from flask import request
from _mod import mod_base
from fee_import import fee_mod

from fee_import import seiho_DA as SEIHO_DA  # 日本生命
from fee_import import seiho_DQ as SEIHO_DQ  # ジブラルタ生命
from fee_import import seiho_DR as SEIHO_DR  # 明治安田生命
from fee_import import seiho_DU as SEIHO_DU  # ソニー生命
from fee_import import seiho_DW as SEIHO_DW  # SOMPOひまわり生命
from fee_import import seiho_EA as SEIHO_EA  # オリックス生命
from fee_import import seiho_EB as SEIHO_EB  # アクサ生命
from fee_import import seiho_EC as SEIHO_EC  # エヌエヌ生命
from fee_import import seiho_ED as SEIHO_ED  # 三井住友海上あいおい生命
from fee_import import seiho_EJ as SEIHO_EJ  # 東京海上日動あんしん生命
from fee_import import seiho_EN as SEIHO_EN  # FWD生命
from fee_import import seiho_EO as SEIHO_EO  # 東京海上フィナンシャル生命
from fee_import import seiho_EQ as SEIHO_EQ  # マニュライフ生命
from fee_import import seiho_ER as SEIHO_ER  # ネオファースト生命
from fee_import import seiho_FC as SEIHO_FC  # メットライフ生命

from fee_import import sonpo_04 as SONPO_04  # 三井住友海上火災
from fee_import import sonpo_09 as SONPO_09  # 東京海上日動火災
from fee_import import sonpo_11 as SONPO_11  # セコム損保
from fee_import import sonpo_14 as SONPO_14  # 日新火災
from fee_import import sonpo_16 as SONPO_16  # AIG損保
from fee_import import sonpo_17 as SONPO_17  # 損保ジャパン
from fee_import import sonpo_18 as SONPO_18  # 楽天損保
from fee_import import sonpo_23 as SONPO_23  # セゾン自動車火災
from fee_import import sonpo_66 as SONPO_66  # チャブ損保

from fee_import import sonpo_JIBAISEKI as SONPO_JIBAISEKI  # 自賠責
from fee_import import syotan_30038 as SYOTAN_30038  # あんしん少短
from fee_import import syotan_30056 as SYOTAN_30056  # くふう少短


def fee_sheet_create():
    # json
    obj = request.get_json()
    jwtg = obj["jwtg"]

    sheet_url = obj["create_sheet_url"]
    nyu_nendo = obj["nyu_nendo"]
    nyu_date = obj["nyu_date_int"]
    cat_cd = obj["cat_cd"]
    coltd_cd = obj["coltd_cd"]

    # base - level 2
    base_data = mod_base.mz_base(9, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]

    # chk
    if level_error == "error":
        dic = {
            "level_error": level_error,
            "new_sheet_url": "",
            "new_sheet_fee_total": 0,
        }
    else:
        # サービスアカウントのJSONキーをダウンロード
        # json_key = fee_mod.download_keyfile()

        # URLからspreadsheet_idを取得
        spreadsheet_id = fee_mod.get_spreadsheet_id(sheet_url)

        # spreadsheet fileを取得
        spreadsheet_file = fee_mod.get_spreadsheet_file(spreadsheet_id)

        # ステータス、枝番、消費税などを設定
        sheet_dic = {
            "spreadsheet_file": spreadsheet_file,
            "nyu_nendo": nyu_nendo,
            "nyu_date": nyu_date,
            "cat_cd": cat_cd,
            "coltd_cd": coltd_cd,
            "kind_cd": 1,
            "syoken_cd_sub": "0000",
            "fee_withtax": 0,
            "fee_tax_per": 10,
            "fee_tax_num": 0,
        }

        # 会社別にシートを作成
        new_sheet_url = set_coltd_sheet(sheet_dic)

        # 作成したシートの手数料税抜を取得
        new_sheet_fee_total = fee_mod.get_fee_total(new_sheet_url)

        dic = {
            "level_error": level_error,
            "new_sheet_url": new_sheet_url,
            "new_sheet_fee_total": new_sheet_fee_total,
        }
    return dic


# 保険会社別に処理
def set_coltd_sheet(sheet_dic):
    # 保険会社別の処理をマッピングするディスパッチディクショナリ
    company = {
        "DA": SEIHO_DA,
        "DQ": SEIHO_DQ,
        "DR": SEIHO_DR,
        "DU": SEIHO_DU,
        "DW": SEIHO_DW,
        "EA": SEIHO_EA,
        "EB": SEIHO_EB,
        "EC": SEIHO_EC,
        "ED": SEIHO_ED,
        "EJ": SEIHO_EJ,
        "EN": SEIHO_EN,
        "EO": SEIHO_EO,
        "EQ": SEIHO_EQ,
        "ER": SEIHO_ER,
        "FC": SEIHO_FC,
        "04": SONPO_04,
        "09": SONPO_09,
        "11": SONPO_11,
        "14": SONPO_14,
        "16": SONPO_16,
        "17": SONPO_17,
        "18": SONPO_18,
        "23": SONPO_23,
        "66": SONPO_66,
        "JIBAISEKI": SONPO_JIBAISEKI,
        "30038": SYOTAN_30038,
        "30056": SYOTAN_30056,
    }

    # 保険会社コードを取得
    coltd_cd = sheet_dic["coltd_cd"]

    # 保険会社の処理をディスパッチディクショナリから取得し、関数を呼び出す
    if coltd_cd in company:
        new_sheet_url = company[coltd_cd].set_sheet(sheet_dic)
        return new_sheet_url
    else:
        raise ValueError(f"Invalid coltd_cd: {coltd_cd}")
