import logging
import google.cloud.logging
from flask import Flask
import firebase_admin
import config
from _auth import _router as auth
from _setting import _router as setting
from _conv import _router as conv
from _sample import _router as sample

from chk import _router as chk
from dwh import _router as dwh
from fee import _router as fee
from fee_import import _router as fee_import
from keijyo import _router as keijyo
from manki import _router as manki
from mst import _router as mst
from nttgw import _router as nttgw
from reinyu import _router as reinyu
from search import _router as search
from store import _router as store
from sum import _router as sum
from salary import _router as salary

# Logging
client = google.cloud.logging.Client()
handler = client.get_default_handler()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
# app.secret_key = "i_love_run"
# from datetime import timedelta
# app.permanent_session_lifetime = timedelta(days=5)
# app.permanent_session_lifetime = timedelta(minutes=5)
# セッション永続化、ここではデフォルトの場合31日間
# session.permanent = True
config.setup_cors(app)
firestore_app = firebase_admin.initialize_app()

# common
auth.router(app)
setting.router(app)
conv.router(app)
sample.router(app)

# fis
chk.router(app)
dwh.router(app)
fee.router(app)
fee_import.router(app)
keijyo.router(app)
manki.router(app)
mst.router(app)
nttgw.router(app)
reinyu.router(app)
search.router(app)
store.router(app)
sum.router(app)
salary.router(app)

# run
if __name__ == "__main__":
    app.run()
