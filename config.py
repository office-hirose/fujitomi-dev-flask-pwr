# import os
from flask_cors import CORS


# cors
def setup_cors(app):
    CORS(
        app,
        supports_credentials=True,  # Cookieとクレデンシャルをドメイン間で送信できる
        origins=[
            "https://dev.fujitomi.jp",
            "http://localhost",
            "http://localhost:3000",
        ],
    )
