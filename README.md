# Cloud RUN, build deploy

gcloud config set project oh-prj-xxxxx

gcloud builds submit --tag gcr.io/oh-prj-xxxxx/flask

gcloud run deploy --image gcr.io/oh-prj-xxxxx/flask

To make this the default region, run `gcloud config set run/region us-central1`

# .gitignoreがPushできない場合、このコマンドでPushする

git add -f .gitignore
git commit -m ".gitignoreファイルを追加"
git push

# Gmail API, Google Cloud 設定マニュアル

このマニュアルは、GCPプロジェクトでGmail APIを安全に利用するための設定手順です。
**キーファイルを直接使わず、Secret Managerを利用する**ことで、セキュリティを向上させることを前提としています。

### Step 1: GCP (Google Cloud Platform) での準備

1.  **Gmail APIの有効化**
    -   GCPコンソール (`console.cloud.google.com`) にログインし、対象プロジェクトを選択します。
    -   `APIとサービス` > `ライブラリ` で `Gmail API` を検索し、有効化します。

2.  **サービスアカウントの作成**
    -   `IAMと管理` > `サービスアカウント` に移動します。
    -   `サービスアカウントを作成` をクリックし、名前（例: `gmail-api-service`）を入力して作成します。このとき**ロールは設定せず**に続行します。

3.  **サービスアカウントキーの作成とSecret Managerへの登録**
    -   作成したサービスアカウントの `キー` タブを選択します。
    -   `キーを追加` > `新しい鍵を作成` > `JSON` を選択してキーファイルを**一度だけローカルにダウンロード**します。
    -   GCPコンソールで **Secret Manager** に移動します。
    -   `+ シークレットを作成` をクリックします。
        -   **名前**: `gmail-api-key-json` （コード内でこの名前が直接使用されます）
        -   **シークレットの値**: **ファイルをアップロード**するか、ダウンロードしたキーファイルの中身（`{...}`）を**全文コピーして貼り付け**ます。
    -   シークレットを作成します。
    -   **重要**: 作業完了後、ダウンロードしたキーファイルはローカルPCから完全に削除してください。リポジトリにもコミットしません。

4.  **IAM権限の設定（最小権限の原則）**
    -   `IAMと管理` > `IAM` に移動します。
    -   **Cloud Runが使用するサービスアカウント**（通常は `[プロジェクト番号]-compute@developer.gserviceaccount.com`）を探し、編集ボタン（鉛筆アイコン）をクリックします。
    -   プログラムの実行に必要な、以下のロールが付与されていることを確認、または追加します。
        -   **Secret Manager のシークレット アクセサー**: Secret Managerからキー情報を読み取るため。
        -   **ストレージ オブジェクト閲覧者**: (もしあれば)メール添付のためにCloud Storageからファイルを読み取るため。
    -   `保存` をクリックします。

### Step 2: Google Workspace での権限委任

1.  **サービスアカウント情報の確認**
    -   GCPの `IAMと管理` > `サービスアカウント` で、作成したアカウントをクリックし、「詳細」タブを開きます。
    -   **「一意の ID」**という項目にある**数字の羅列**をコピーします。これがAPIクライアントIDになります。

2.  **ドメイン全体の委任を設定**
    -   **Google Workspace 管理コンソール** (`admin.google.com`) に特権管理者でログインします。
    -   `セキュリティ` > `アクセスとデータ管理` > `API の制御` に移動します。
    -   `ドメイン全体の委任` の項目で `[ドメイン全体の委任を管理]` をクリックします。
    -   `新しく追加` をクリックします。
    -   `クライアントID`: 先ほどコピーした**「一意の ID」（数字）**を貼り付けます。
    -   `OAuthスコープ`: メール送信に必要な以下のスコープを貼り付けます。
        ```
        https://www.googleapis.com/auth/gmail.send
        ```
    -   `承認` をクリックして保存します。

### Step 3: アプリケーション側の設定

1.  **必要なライブラリをインストール**
    -   `requirements.txt` に以下が含まれていることを確認し、なければ追加して `pip install -r requirements.txt` を実行します。
    ```
    google-api-python-client
    google-auth-httplib2
    google-auth-oauthlib
    google-cloud-storage
    google-cloud-secret-manager
    ```

### Step 4: コード実装

-   プログラムは、Secret Managerに保存されたキー情報を直接読み込んで認証情報を生成します。
-   このプロジェクトの `_sample/sample_gmail_api.py` にある `get_gmail_service` 関数が具体的な実装例となります。
-   実装の主なポイント:
    -   Secret Managerを利用した安全なキー管理
    -   サービスアカウント認証を使用
    -   テキスト、HTML、添付ファイル対応
