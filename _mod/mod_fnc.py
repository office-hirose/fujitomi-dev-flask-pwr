import os
import mimetypes
from _mod import mod_datetime


# File Name Converter ファイル名を受取り、ファイル名を現在の東京時刻にして返す. content typeも返す
def mz_fnc(file_name):
    # init
    mimetypes.init()

    # get tokyo time now
    tnow_str = mod_datetime.mz_tnow("for_filename")

    # ファイル名と拡張子
    file_name_tuple = os.path.splitext(file_name)  # 受け取ったファイル名をタプルに入れる
    file_name_root = file_name_tuple[0]  # 元のファイル名のみ
    file_name_ext = file_name_tuple[1].lower()  # 拡張子のみを小文字に
    file_name_new = tnow_str  # 日付時間からファイル名のみを作成

    # content type , mime type 調べる
    # content_type_full = mimetypes.types_map[file_name_ext]  # エラーが出るファイルがある、例、xlsx
    content_type_full = mimetypes.guess_type(file_name)[0]

    fnc_values = {
        # 元のファイル名のみ、拡張子なし
        "file_name_root": file_name_root,
        # 拡張子のみ
        "file_name_ext": file_name_ext,
        # 変換されたファイル名のみ、拡張子なし
        "file_name_new": file_name_new,
        # 変換されたファイル名(日付時間のファイル名) + 拡張子
        "file_name_full_new": file_name_new + file_name_ext,
        # content type
        "content_type_full": content_type_full,
    }
    return fnc_values
