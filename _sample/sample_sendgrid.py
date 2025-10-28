from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)
from google.cloud import storage
import base64
from _mod import fs_config, mod_datetime


def sample_sendgrid_exe(subpath):
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

    # sendgrid
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

    # from, to
    mail_con = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body,
    )

    # send
    sg = SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

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

    # from, to
    mail_con = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body,
    )

    # send
    sg = SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

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

    # from, to
    mail_con = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body,
    )

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
    encoded_file = base64.b64encode(content).decode()

    # attach_file
    attach_file = Attachment(
        FileContent(encoded_file),
        FileName(send_file_name),
        FileType("application/pdf"),
        Disposition("attachment"),
        ContentId(send_file_name),
    )
    mail_con.attachment = attach_file

    # send
    sg = SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    return
