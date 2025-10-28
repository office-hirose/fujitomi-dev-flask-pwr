import datetime
import pytz
from unicodedata import east_asian_width

# 注意、iPhoneのsafariでは、このフィルターはエラーした、2016-0627
# email 13文字 取り出し 現在未使用 email_shortを使用する
# def email_get_13(email):
#     email_slice = email[0:14]+'...'
#     return email_slice


# 改行を<br>に変換
def nl2br(value):
    return value.replace("\n", "<br>\n")


# UTC時刻をJST時刻に変換
def utc2jst(value, format="%Y/%m/%d %H:%M:%S"):
    utc = pytz.timezone("UTC")
    jst = pytz.timezone("Asia/Tokyo")
    value = value.replace(tzinfo=utc).astimezone(jst)
    return value.strftime(format)


# A、本日の年令を計算、わかりやすいソース
def get_age_a(born):
    today = datetime.date.today()
    age = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    return age


# B、本日の年令を計算、シンプルだがifが書いていないのでわかりにくい
def get_age_b(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# 数字を３桁区切りにカンマを入れる
def num_comma(num):
    if num is None:
        num = 0
    num_comma = "{:,}".format(num)
    return num_comma


# 数字を３桁区切りにカンマを入れる2、上記とどちらが正しいのか不明
# def num_comma2(num):
#     num_comma = '{:,d}'.format(num)
#     return num_comma


# 文字を３桁区切りにカンマを入れる
def str_comma(str_value):
    num = int(str_value)
    num_comma = "{:,d}".format(num)
    return num_comma


# link button title slice small
def lb_title_slice_s(title):
    x = 35
    len = 0
    slice = 0
    title_slice = title

    for i in title:
        # ex '１'
        if east_asian_width(i) == "F":
            len += 2

        # ex 'あ'
        if east_asian_width(i) == "W":
            len += 2

        # ex 'ｱ'
        if east_asian_width(i) == "H":
            len += 1

        # ex 'a'
        if east_asian_width(i) == "Na":
            len += 1

        # 文字長さ確認、スライス
        if len > x:
            title_slice = title[0:slice] + "..."
            break

        slice += 1

    return title_slice


# link button title slice large
def lb_title_slice_l(title):
    x = 90
    len = 0
    slice = 0
    title_slice = title

    for i in title:
        # ex '１'
        if east_asian_width(i) == "F":
            len += 2

        # ex 'あ'
        if east_asian_width(i) == "W":
            len += 2

        # ex 'ｱ'
        if east_asian_width(i) == "H":
            len += 1

        # ex 'a'
        if east_asian_width(i) == "Na":
            len += 1

        # 文字長さ確認、スライス
        if len > x:
            title_slice = title[0:slice] + "..."
            break

        slice += 1

    return title_slice


# link button detail slice large
def lb_detail_slice_l(detail):
    x = 90
    len = 0
    slice = 0
    detail_slice = detail

    for i in detail:
        # ex '１'
        if east_asian_width(i) == "F":
            len += 2

        # ex 'あ'
        if east_asian_width(i) == "W":
            len += 2

        # ex 'ｱ'
        if east_asian_width(i) == "H":
            len += 1

        # ex 'a'
        if east_asian_width(i) == "Na":
            len += 1

        # 文字長さ確認、スライス
        if len > x:
            detail_slice = detail[0:slice] + "..."
            break

        slice += 1

    return detail_slice


def mz_zfill2(str_data):
    result_data = ""
    result_data = str_data.zfill(2)
    return result_data


def mz_str2zip(str_zip):
    if len(str_zip) == 0 or len(str_zip) > 7:
        res_zip = "〒000-0000"
    else:
        res_zip = "〒" + str_zip[0:3] + "-" + str_zip[3:7]
    return res_zip
