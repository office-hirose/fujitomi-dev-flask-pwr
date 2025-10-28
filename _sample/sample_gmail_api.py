import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.cloud import storage
from _mod import fs_config, mod_datetime, mod_gmail_api


def sample_gmail_api_exe(subpath):
    # init, firestore
    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        return {}  # 設定がない場合は空の辞書を返す
    send_time = mod_datetime.mz_tnow("for_datetime")

    # get
    sender_email = fs_dic["sender_email"]
    # customer_name = item["customer_name"]
    # customer_email = item["customer_email"]
    # subject = item["subject"]
    # message = item["message"]
    customer_name = "flask flask"
    customer_email = "tomoaki.hirose@gmail.com"
    subject = "これはテストです"
    message = "あいうえお"

    # gmail api
    if subpath == "text":
        mz_text("customer", customer_name, customer_email, subject, message, send_time)
        mz_text("admin", customer_name, sender_email, subject, message, send_time)

    if subpath == "html":
        mz_html("customer", customer_name, customer_email, subject, message, send_time)
        mz_html("admin", customer_name, sender_email, subject, message, send_time)

    if subpath == "attach":
        mz_attach("customer", customer_name, customer_email, subject, message, send_time)
        mz_attach("admin", customer_name, sender_email, subject, message, send_time)

    # dic
    dic = {
        "to_email": customer_email,
        "subpath": subpath,
        "send_time": send_time,
    }
    return dic


def mz_text(cat, customer_name, customer_email, subject, message, send_time):
    # init, firestore
    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        return  # 設定がない場合は処理を中断
    from_email = fs_dic["sender_email"]
    to_email = customer_email

    # headerを空文字列として初期化
    header = ""
    if cat == "customer":
        header = "お問い合わせいただきありがとうございました。"

    if cat == "admin":
        header = "管理者用" + "\n\n" + "お問い合わせいただきありがとうございました。"

    # subject, body
    subject = "お問い合わせ（確認メール）- www.office-hirose.com"
    body = ""
    body += header + "\n\n"
    body += "お客様名　　　　：" + customer_name + "\n"
    body += "お客様メール　　：" + customer_email + "\n"
    body += "タイトル　　　　：" + subject + "\n"
    body += "お問い合わせ内容：" + message + "\n"
    body += "\n\n"
    body += "送信時刻：" + send_time + "\n\n"

    # Gmail APIでメール送信
    service = mod_gmail_api.get_gmail_service()
    if service is None:
        return

    # メールメッセージを作成
    message_obj = MIMEText(body, "plain", "utf-8")
    message_obj["to"] = to_email
    message_obj["from"] = from_email
    message_obj["subject"] = subject

    # Base64エンコード
    raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

    # メール送信
    try:
        result = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"Sample Text メール送信成功: {result}")
    except Exception as e:
        print(f"Sample Text メール送信エラー: {e}")
        import traceback

        print(f"Sample Text 詳細エラー: {traceback.format_exc()}")

    return


def mz_html(cat, customer_name, customer_email, subject, message, send_time):
    # init, firestore
    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        return  # 設定がない場合は処理を中断
    from_email = fs_dic["sender_email"]
    to_email = customer_email

    # headerを空文字列として初期化
    header = ""
    if cat == "customer":
        header = "<h3>お問い合わせいただきありがとうございました。</h3>"

    if cat == "admin":
        header = "<h3>管理者用" + "<br>" + "お問い合わせいただきありがとうございました。</h3>"

    # subject, body
    subject = "お問い合わせ（確認メール）- www.office-hirose.com"
    body = ""
    body += "<html><head></head><body>"
    body += header
    body += "<h2>お客様名：" + customer_name + "</h2>"
    body += "<h3>お客様メール：" + customer_email + "</h3>"
    body += "<h4>タイトル：" + subject + "</h4>"
    body += "<h5>お問い合わせ内容：" + message + "</h5>"
    body += "送信時刻：" + send_time
    body += "</body></html>"

    # Gmail APIでメール送信
    service = mod_gmail_api.get_gmail_service()
    if service is None:
        return

    # メールメッセージを作成
    message_obj = MIMEText(body, "html", "utf-8")
    message_obj["to"] = to_email
    message_obj["from"] = from_email
    message_obj["subject"] = subject

    # Base64エンコード
    raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

    # メール送信
    try:
        result = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"Sample Html メール送信成功: {result}")
    except Exception as e:
        print(f"Sample Html メール送信エラー: {e}")
        import traceback

        print(f"Sample Html 詳細エラー: {traceback.format_exc()}")

    return


def mz_attach(cat, customer_name, customer_email, subject, message, send_time):
    # init, firestore
    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        return  # 設定がない場合は処理を中断
    from_email = fs_dic["sender_email"]
    to_email = customer_email

    # headerを空文字列として初期化
    header = ""
    if cat == "customer":
        header = "お問い合わせいただきありがとうございました。"

    if cat == "admin":
        header = "管理者用" + "\n\n" + "お問い合わせいただきありがとうございました。"

    # subject, body
    subject = "お問い合わせ（確認メール）- www.office-hirose.com"
    body = ""
    body += header + "\n\n"
    body += "お客様名　　　　：" + customer_name + "\n"
    body += "お客様メール　　：" + customer_email + "\n"
    body += "タイトル　　　　：" + subject + "\n"
    body += "お問い合わせ内容：" + message + "\n"
    body += "\n\n"
    body += "送信時刻：" + send_time + "\n\n"

    # Gmail APIでメール送信
    service = mod_gmail_api.get_gmail_service()
    if service is None:
        return

    # マルチパートメッセージを作成
    message_obj = MIMEMultipart()
    message_obj["to"] = to_email
    message_obj["from"] = from_email
    message_obj["subject"] = subject

    # テキスト部分を追加
    text_part = MIMEText(body, "plain", "utf-8")
    message_obj.attach(text_part)

    # init
    project_name = fs_dic["project_name"]
    bucket_name = fs_dic["upload_gcs_bucket"]
    source_file = "sample.pdf"
    send_file_name = "sample.pdf"

    # google cloud storage
    client = storage.Client(project_name)
    bucket = client.get_bucket(bucket_name)
    blob = storage.Blob(source_file, bucket)
    content = blob.download_as_string()

    # 添付ファイルを追加
    attachment = MIMEBase("application", "pdf")
    attachment.set_payload(content)
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename= {send_file_name}")
    message_obj.attach(attachment)

    # Base64エンコード
    raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode("utf-8")

    # メール送信
    try:
        result = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"Sample Attach メール送信成功: {result}")
    except Exception as e:
        print(f"Sample Attach メール送信エラー: {e}")
        import traceback

        print(f"Sample Attach 詳細エラー: {traceback.format_exc()}")

    return
