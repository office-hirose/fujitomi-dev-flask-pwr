from unicodedata import east_asian_width
from _mod import mod_datetime


def mz_ido_kai_date_conv(ido_kai_date):
    ido_kai_date_conv = 0
    if ido_kai_date == "":
        ido_kai_date_conv = 0
    else:
        ido_kai_date_conv = int(ido_kai_date.replace("/", ""))
    return ido_kai_date_conv


def mz_siki_date_conv(siki_date):
    siki_date_conv = 0
    if siki_date == "":
        siki_date_conv = 0
    else:
        siki_date_conv = int(siki_date.replace("/", ""))
    return siki_date_conv


def mz_manki_date_conv(manki_date):
    manki_date_conv = 0
    if manki_date == "":
        manki_date_conv = 0
    else:
        manki_date_conv = int(manki_date.replace("/", ""))
    return manki_date_conv


# 契約者名
def mz_kei_name_conv(temp):
    temp = temp.strip()  # 前後のスペースと改行を取り除く
    temp = temp.replace(" ", "　")  # 半角スペースを全角スペースに置換
    temp = temp.replace("-", "−")  # 半角ハイフンを全角ハイフン
    return temp


def mz_search_text_conv(syoken_cd, old_syoken_cd, kei_name, kei_name_hira):
    search_text = ""
    sp = " "

    kei_name_nospace = mz_kei_name_nospace_conv(kei_name)
    kei_name_hira_nospace = mz_kei_name_nospace_conv(kei_name_hira)

    search_text = syoken_cd + sp + old_syoken_cd + sp + kei_name_nospace + sp + kei_name_hira_nospace
    return search_text


# 契約者名ノースペース
def mz_kei_name_nospace_conv(kei_name):
    kei_name_nospace = ""
    kei_name = kei_name.replace("　", "")  # 契約者名、全角スペース除去
    kei_name_nospace = kei_name.replace(" ", "")  # 契約者名、半角スペース除去
    return kei_name_nospace


def mz_exe_sta_result(exe_sta):
    exe_sta_result = ""
    if exe_sta == "tnet":
        exe_sta_result = "Tnet取込"
    if exe_sta == "hand":
        exe_sta_result = "手動入力"
    if exe_sta == "nttgw":
        exe_sta_result = "NTTGW取込"
    return exe_sta_result


# kei_name slice 20文字
def mz_kei_name_slice20(kei_name):
    kei_name_slice = kei_name[0:20]
    return kei_name_slice


# kei_name slice 30文字
def mz_kei_name_slice30(kei_name):
    kei_name_slice = kei_name[0:30]
    return kei_name_slice


# memo slice
def mz_memo_slice(memo):
    x = 60
    len = 0
    slice = 0
    memo_slice = memo

    for i in memo:
        # example '１'
        if east_asian_width(i) == "F":
            len += 2

        # example 'あ'
        if east_asian_width(i) == "W":
            len += 2

        # example 'ｱ'
        if east_asian_width(i) == "H":
            len += 1

        # example 'a'
        if east_asian_width(i) == "Na":
            len += 1

        # 文字長さ確認、スライス
        if len > x:
            memo_slice = memo[0:slice] + "..."
            break

        slice += 1

    return memo_slice


def mz_keijyo_date_str(keijyo_date):
    keijyo_date_str = ""
    if keijyo_date == 0:
        keijyo_date_str = "9999年99月"
    else:
        str_date = str(keijyo_date)
        yyyy = str_date[0:4]

        str_date = str(keijyo_date)
        mm = str_date[4:6]

        keijyo_date_str = yyyy + "年" + mm + "月"
    return keijyo_date_str


# num date to yyyy/mm/dd, 20180115 -> 2018/01/15、終身の場合があるのでmod_datetimeからコピーして編集
def mz_num2date_slash(num_date):
    if num_date == 0:
        dt_str = "終身"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "/" + mm + "/" + dd
    return dt_str


# num date to yyyy/mm/dd, 20180115 -> 2018/01/15, 0の場合はブランクをセット
def mz_num2date_slash_normal(num_date):
    if num_date == 0:
        dt_str = ""
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "/" + mm + "/" + dd
    return dt_str


# 生保損保で種目種類名の表示を変える
def mz_kind_name_main_sub(cat_cd, kind_name_main, kind_name_sub):
    res_kind_name = ""
    if cat_cd == "1":
        res_kind_name = kind_name_sub
    if cat_cd != "1":
        res_kind_name = kind_name_main
    return res_kind_name


def mz_datetime_view(value_datetime):
    if value_datetime == "empty" or value_datetime is None:
        return_datetime = "0000-00-00 00:00:00"
    else:
        return_datetime = str(mod_datetime.mz_dt2str_yymmddhhmmss_hyphen(value_datetime))
    return return_datetime
