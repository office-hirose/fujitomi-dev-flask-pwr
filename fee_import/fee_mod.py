# -------------------------------------------------------------------
#  fee_mod.py - Spread Sheetのモジュール
# -------------------------------------------------------------------
import json
import re
from _mod import fs_config
from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import gspread
import urllib.parse


# GCSからサービスアカウントのJSONキーをダウンロード
def download_keyfile():
    # init, firestore
    fs_dic = fs_config.fs_dic()

    # Google Cloud Storageのバケット名とJSONキーファイル名を設定
    bucket_name = fs_dic["oauth_key_gcs_bucket"]
    keyfile_name = fs_dic["google_drive_oauth_key_json"]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(keyfile_name)
    json_key = json.loads(blob.download_as_text())
    return json_key


# SpreadSheetのURLからSpreadsheetIDを取得する
def get_spreadsheet_id(sheet_url):
    match = re.search(r"spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Spreadsheet URL")


# SpreadSheetIDからfileを取得
def get_spreadsheet_file(spreadsheet_id):
    json_key = download_keyfile()
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_info(json_key, scopes=scopes)
    creds.refresh(Request())
    client = gspread.authorize(creds)
    spreadsheet_file = client.open_by_key(spreadsheet_id)
    return spreadsheet_file


# URLからgidを取得
def get_gid_from_url(sheet_url):
    parsed = urllib.parse.urlparse(sheet_url)
    fragment = urllib.parse.parse_qs(parsed.fragment)
    gid_list = fragment.get("gid")
    if not gid_list:
        raise ValueError("No gid found in the provided URL")
    gid = int(gid_list[0])
    return gid


# gidからシート名を取得
def get_sheet_name_by_gid(spreadsheet, gid):
    all_worksheets = spreadsheet.worksheets()
    for worksheet in all_worksheets:
        if worksheet.id == gid:
            return worksheet.title
    raise ValueError(f"No sheet found with gid {gid}")


def get_sheet_data(sheet_url):
    # サービスアカウントのJSONキーをダウンロード
    # json_key = download_keyfile()

    # URLからspreadsheet_idを取得
    spreadsheet_id = get_spreadsheet_id(sheet_url)

    # URLからgidを取得
    gid = get_gid_from_url(sheet_url)

    # スプレッドシートを取得
    spreadsheet = get_spreadsheet_file(spreadsheet_id)

    # gidからシート名を取得
    sheet_name = get_sheet_name_by_gid(spreadsheet, gid)

    # シートを選択
    sheet = spreadsheet.worksheet(sheet_name)

    # 行数を取得
    num_rows = sheet.row_count

    # A2からMまでのすべてのデータをリストで取得（ヘッダーを省略）
    sheet_data = sheet.get("A2:M{}".format(num_rows))

    return sheet_data


def get_fee_total(sheet_url):
    # get sheet data
    sheet_data = get_sheet_data(sheet_url)

    # init
    fee_notax = 0
    fee_notax_total = 0

    # calc
    for dt in sheet_data:
        try:
            fee_notax = int(dt[8])
            fee_notax_total += fee_notax
        except:  # noqa: E722
            raise ValueError(f"Invalid fee_notax {fee_notax}")

    return fee_notax_total
