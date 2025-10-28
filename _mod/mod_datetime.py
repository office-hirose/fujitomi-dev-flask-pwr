import datetime
import pytz
from dateutil.relativedelta import relativedelta


def mz_tnow(exe_sta):
    # 日本時間日付時刻
    jst = pytz.timezone("Asia/Tokyo")
    tnow = datetime.datetime.now(jst)
    # ファイル名
    if exe_sta == "for_filename":
        tnow_str = tnow.strftime("%Y-%m-%d-%H-%M-%S-%f")
    # ファイル名 yyyy-mmdd
    if exe_sta == "for_filename_yyyy_mmdd":
        tnow_str = tnow.strftime("%Y-%m%d")
    # ファイル名 yyyy-mmdd-hhmm
    if exe_sta == "for_filename_yyyy_mmdd_hhmm":
        tnow_str = tnow.strftime("%Y-%m%d-%H%M")
    # 現在日付
    if exe_sta == "for_date":
        tnow_str = tnow.strftime("%Y-%m-%d")
    # 現在日付時刻
    if exe_sta == "for_datetime":
        tnow_str = tnow.strftime("%Y-%m-%d %H:%M:%S")
    # 現在日付時刻ハイフンなし
    if exe_sta == "for_datetime_no_hypen":
        tnow_str = tnow.strftime("%Y%m%d%H%M%S")
    # 現在日付時刻アンダーバー区切り
    if exe_sta == "for_datetime_underbar":
        tnow_str = tnow.strftime("%Y_%m_%d_%H_%M_%S")
    # 年のみ
    if exe_sta == "year":
        tnow_str = tnow.strftime("%Y")
    return tnow_str


# 日付を数値に変換 yyyymmdd
def mz_dt2num_yymmdd(datetime_data):
    dt_num = int(datetime_data.strftime("%Y%m%d"))
    return dt_num


# 日付を数値に変換 yyyymmddhhmmss
def mz_dt2num_yymmddhhmmss(datetime_data):
    dt_num = int(datetime_data.strftime("%Y%m%d%H%M%S"))
    return dt_num


# 日付を数値に変換 yyyymmdd JST, GAEはリージョンが日本でも時刻はUTCのため
def mz_dt2num_yymmdd_jst(datetime_data):
    datetime_jst = datetime_data + datetime.timedelta(hours=9)
    dt_num = int(datetime_jst.strftime("%Y%m%d"))
    return dt_num


# 日付を数値に変換 yyyymmddhhmmss JST, GAEはリージョンが日本でも時刻はUTCのため
def mz_dt2num_yymmddhhmmss_jst(datetime_data):
    datetime_jst = datetime_data + datetime.timedelta(hours=9)
    dt_num = int(datetime_jst.strftime("%Y%m%d%H%M%S"))
    return dt_num


# 日付を文字列に変換
def mz_dt2str_yymmdd(datetime_data):
    dt_str = datetime_data.strftime("%Y%m%d")
    return dt_str


# 日付を文字列に変換 スラッシュ区切り
def mz_dt2str_yymmdd_slash(datetime_data):
    dt_str = datetime_data.strftime("%Y/%m/%d")
    return dt_str


# 日付を文字列に変換 ハイフン区切り
def mz_dt2str_yymmdd_hyphen(datetime_data):
    dt_str = datetime_data.strftime("%Y-%m-%d")
    return dt_str


# 日付を文字列に変換 ハイフン区切り jst
def mz_dt2str_yymmdd_hyphen_jst(datetime_data):
    datetime_data = datetime_data + datetime.timedelta(hours=9)
    dt_str = datetime_data.strftime("%Y-%m-%d")
    return dt_str


# 日付時間分を文字列に変換 ハイフン区切り 年 月 日 時 分
def mz_dt2str_yymmddhhmm_hyphen(datetime_data):
    dt_str = datetime_data.strftime("%Y-%m-%d %H:%M")
    return dt_str


# 日付時間分を文字列に変換 ハイフン区切り 年 月 日 時 分 秒
def mz_dt2str_yymmddhhmmss_hyphen(datetime_data):
    dt_str = datetime_data.strftime("%Y-%m-%d %H:%M:%S")
    return dt_str


# 日付時間分を文字列に変換 スラッシュ区切り 年 月 日 時 分 秒
def mz_dt2str_yymmddhhmmss_slash(datetime_data):
    dt_str = datetime_data.strftime("%Y/%m/%d %H:%M:%S")
    return dt_str


# 日付時間分を文字列に変換JST ハイフン区切り 年 月 日 時 分 秒
def mz_dt2str_yymmddhhmmss_jst_hyphen(datetime_data):
    datetime_jst = datetime_data + datetime.timedelta(hours=9)
    dt_str = datetime_jst.strftime("%Y-%m-%d %H:%M:%S")
    return dt_str


# 文字列を日付型でそのまま返す ハイフン区切り
def mz_str2dt_hyphen(str):
    dt_dt = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
    return dt_dt


# 文字列を日付型でそのまま返す スラッシュ区切り
def mz_str2dt_slash(str):
    dt_dt = datetime.datetime.strptime(str, "%Y/%m/%d %H:%M:%S")
    return dt_dt


# 文字列を日付型にして、JST時刻をUTC時刻に変換、日付型でそのまま返す
def mz_str2dt_jst2utc(str):
    dt_dt = datetime.datetime.strptime(str, "%Y/%m/%d %H:%M:%S")
    jst = pytz.timezone("Asia/Tokyo")
    utc = pytz.timezone("UTC")
    dt_dt = dt_dt.replace(tzinfo=jst).astimezone(utc)
    return dt_dt


# num date to yyyy-mm-dd, 20180115 -> 2018-01-15
def mz_num2date_hyphen(num_date):
    if num_date == 0:
        dt_str = "0000-00-00"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "-" + mm + "-" + dd
    return dt_str


# num dateを日付型に変換 20210131 -> 2021-01-31
def mz_mum2date_yymmdd(num_date):
    dt_str = "2000-01-01"
    str_date = str(num_date)
    yy = str_date[0:4]
    mm = str_date[4:6]
    dd = str_date[6:8]
    dt_str = yy + "-" + mm + "-" + dd
    dt_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
    return dt_dt


# num date to yyyy-mm-dd, 20180115 -> 2018-01-15 ゼロの場合ブランク
def mz_num2date_hyphen_zero_blank(num_date):
    if num_date == 0:
        dt_str = ""
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "-" + mm + "-" + dd
    return dt_str


# 日付を文字列に変換 年月日
def mz_dt2str_yymmdd_nen_tuki_hi(datetime_data):
    dt_str = datetime_data.strftime("%Y年%-m月%-d日")
    return dt_str


# 日付を文字列に変換 年月日 前ゼロ
def mz_dt2str_yymmdd_nen_tuki_hi_zero(datetime_data):
    dt_str = datetime_data.strftime("%Y年%m月%d日")
    return dt_str


# num date to yyyy/mm/dd, 20180115 -> 2018/01/15
def mz_num2date_slash(num_date):
    if num_date == 0:
        dt_str = "1900/01/01"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "/" + mm + "/" + dd
    return dt_str


# num dateを文字列に変換 年月日
def mz_mum2str_yymmdd_nen_tuki_hi(num_date):
    if num_date == 0:
        dt_str = "1900-01-01 00:00:00"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "-" + mm + "-" + dd + " 00:00:00"

    dt_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    dt_str = dt_dt.strftime("%Y年%-m月%-d日")
    return dt_str


# num dateを文字列に変換 年月
def mz_mum2str_yymmdd_nen_tuki(num_date):
    if num_date == 0:
        dt_str = "0000年01月"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dt_str = yy + "年" + mm + "月"
    return dt_str


# 日付を年月日のみ
# def mz_datetime_fmt_yymmdd(value, format='%Y/%m/%d'):
#     if value is None:
#         return value
#     else:
#         return value.strftime(format)


# str date to num date, 2018-01-15 -> 20180115
def mz_date2num(str_date):
    if str_date == "0" or str_date == "" or str_date == 0:
        conv_date = 0
    else:
        yy = str_date[0:4]
        mm = str_date[5:7]
        dd = str_date[8:10]
        conv_date = int(yy + mm + dd)
    return conv_date


# str date to num date, 2018-01-15 -> 20180115
def mz_str2num_hyphen_zero_ari(str_date):
    if str_date == "0" or str_date == "":
        num_date = 0
    else:
        yy = str_date[0:4]
        mm = str_date[5:7]
        dd = str_date[8:10]
        num_date = int(yy + mm + dd)
    return num_date


# num date to yyyy mm dd, 20180115 -> 2018 1 15
def mz_num2yy(num_date):
    if num_date == 0:
        conv_date = "1900"
    else:
        str_date = str(num_date)
        conv_date = int(str_date[0:4])
    return conv_date


def mz_num2mm(num_date):
    if num_date == 0:
        conv_date = "1"
    else:
        str_date = str(num_date)
        conv_date = int(str_date[4:6])

    return conv_date


def mz_num2dd(num_date):
    if num_date == 0:
        conv_date = "1"
    else:
        str_date = str(num_date)
        conv_date = int(str_date[6:8])
    return conv_date


def mz_num2date_yyyymm(num_date):
    if num_date == 0:
        dt_str = "0"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dt_str = yy + "-" + mm
    return dt_str


# num date to str date, 20180115 -> 2018-01-15, 0の場合そのまま
def mz_num2date_hyphen_zero_ari(num_date):
    if num_date == 0:
        dt_str = "0"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        dt_str = yy + "-" + mm + "-" + dd
    return dt_str


# num date to yyyy mm dd, 20180115 -> 2018 01 15
def mz_num2yy_maezero(num_date):
    if num_date == 0:
        conv_date = "1900"
    else:
        str_date = str(num_date)
        conv_date = str_date[0:4]
    return conv_date


def mz_num2mm_maezero(num_date):
    if num_date == 0:
        conv_date = "01"
    else:
        str_date = str(num_date)
        conv_date = str_date[4:6]
    return conv_date


def mz_num2dd_maezero(num_date):
    if num_date == 0:
        conv_date = "01"
    else:
        str_date = str(num_date)
        conv_date = str_date[6:8]
    return conv_date


def mz_num2yymmdd_maezero(num_date):
    if num_date == 0:
        yy = "1900"
        mm = "01"
        dd = "01"
    else:
        str_date = str(num_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
    return yy, mm, dd


# 現在の日付時刻, 文字型 yyyy-mm-dd, int型 yyyymmdd, int型 yyyy
def mz_now_date():
    now_date = mz_dt2str_yymmdd_hyphen(datetime.datetime.now())
    return now_date


def mz_now_datetime():
    now_datetime = mz_dt2str_yymmddhhmm_hyphen(datetime.datetime.now())
    return now_datetime


def mz_now_datetime_ss():
    now_datetime = mz_dt2str_yymmddhhmmss_hyphen(datetime.datetime.now())
    return now_datetime


def mz_now_date_num():
    datetime_jst = datetime.datetime.now() + datetime.timedelta(hours=9)
    now_date_num = mz_dt2num_yymmdd(datetime_jst)
    return now_date_num


def mz_now_year_num():
    datetime_jst = datetime.datetime.now() + datetime.timedelta(hours=9)
    now_year_str = mz_dt2str_yymmdd(datetime_jst)
    now_year_num = int(now_year_str[0:4])
    return now_year_num


# ２つの日付の経過数
# 日付
def mz_num2keika_day(start_num, end_num):
    if start_num == 0 or end_num == 0:
        dd = 0
    else:
        start_str = str(start_num)
        end_str = str(end_num)

        start_yy = int((start_str)[0:4])
        start_mm = int((start_str)[4:6])
        start_dd = int((start_str)[6:8])

        end_yy = int((end_str)[0:4])
        end_mm = int((end_str)[4:6])
        end_dd = int((end_str)[6:8])

        s = datetime.date(start_yy, start_mm, start_dd)
        e = datetime.date(end_yy, end_mm, end_dd)
        dd = (e - s).days
        # dd += 1  # 該当する最初の日を含める場合
    return dd


# 月数
def mz_num2keika_month(start_num, end_num):
    if start_num == 0 or end_num == 0:
        mm = 0
    else:
        start_str = str(start_num)
        end_str = str(end_num)

        start_yy = int((start_str)[0:4])
        start_mm = int((start_str)[4:6])
        start_dd = int((start_str)[6:8])

        end_yy = int((end_str)[0:4])
        end_mm = int((end_str)[4:6])
        end_dd = int((end_str)[6:8])

        s = datetime.date(start_yy, start_mm, start_dd)
        e = datetime.date(end_yy, end_mm, end_dd)
        mm = (e.year - s.year) * 12 + e.month - s.month

        # 同じ年月の場合のみ+1
        # if start_yy == end_yy and start_mm == end_mm:
        # mm += 1  # 該当する最初の月を含める場合
    return mm


# num_dateから年/月/日 加算する、まだ確認中 2019−0905
def mz_num2add_year_kasan(num_date, num_date_another, add_yy):
    num_date = num_date_another
    if num_date != 0 and add_yy != 0:
        add_mm = add_yy * 12
        str_date = str(num_date)
        num_yy = int((str_date)[0:4])
        num_mm = int((str_date)[4:6])
        num_dd = int((str_date)[6:8])

        datetime_data = datetime.datetime(num_yy, num_mm, num_dd) + relativedelta(months=add_mm)
        num_date = mz_dt2num_yymmdd(datetime_data)
    return num_date


# 日本時間を取得
def mz_japan_time():
    jst = pytz.timezone("Asia/Tokyo")
    japan_time = datetime.datetime.now(jst)
    return japan_time
