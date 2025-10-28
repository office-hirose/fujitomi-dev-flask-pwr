from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import secretmanager
import json
from _mod import fs_config


def get_gmail_service():
    """Gmail APIサービスを取得 (Secret Manager対応)"""

    fs_dic = fs_config.fs_dic()
    if fs_dic is None:
        return None

    try:
        # --- Secret Managerからサービスアカウントキーを取得する処理 ---
        # 1. Secret Managerクライアントを初期化
        client = secretmanager.SecretManagerServiceClient()

        # 2. シークレットのバージョンリソース名を構築
        project_id = fs_dic.get("project_name")
        secret_id = "gmail-api-key-json"  # GCPで作成したシークレット名
        version_id = "latest"  # 最新バージョンを指定
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # 3. シークレットの値にアクセス
        response = client.access_secret_version(request={"name": name})
        secret_payload = response.payload.data.decode("UTF-8")

        # 4. JSON文字列を辞書に変換
        credentials_info = json.loads(secret_payload)

        print(f"Secret Managerからキーを正常に取得しました: {secret_id}")
        # -----------------------------------------------------------

        print(f"送信者メールアドレス: {fs_dic['sender_email']}")

        # 取得したキー情報から認証情報を作成
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/gmail.send"],
        )

        # 委任されたユーザーのメールアドレス
        delegated_credentials = credentials.with_subject(fs_dic["sender_email"])
        print("認証情報の作成が完了しました")

        # Gmail APIサービスを構築
        service = build("gmail", "v1", credentials=delegated_credentials)
        print("Gmail APIサービスの構築が完了しました")
        return service
    except Exception as e:
        print(f"Gmail APIサービスの初期化エラー: {e}")
        import traceback

        print(f"詳細エラー: {traceback.format_exc()}")
        return None
