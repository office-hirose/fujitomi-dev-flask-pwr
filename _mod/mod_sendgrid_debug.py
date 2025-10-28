from _mod import fs_config, mod_datetime
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, To


def mz_send_text(send_text):
    # init, firestore
    fs_dic = fs_config.fs_dic()

    if fs_dic is None or fs_dic.get("sender_email") is None or fs_dic.get("sendgrid_api_key") is None:
        print("Error: Failed to load SendGrid configuration.")  # Log the error
        return  # Exit the function if config is missing

    send_time = mod_datetime.mz_tnow("for_datetime")
    from_email = fs_dic["sender_email"]
    to_email = fs_dic["sender_email"]

    # subject body
    subject_data = "sendgrid debug"
    body_data = ""
    body_data += "\n\n"
    body_data += "send_text：" + "\n\n"
    body_data += send_text + "\n\n"
    body_data += "処理送信時刻：" + send_time + "\n\n"

    # sendgrid define
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject_data
    content = Content("text/plain", body_data)
    mail_con = Mail(from_email, to_email, subject, content)
    sg = sendgrid.SendGridAPIClient(fs_dic["sendgrid_api_key"])
    sg.send(mail_con)

    return
