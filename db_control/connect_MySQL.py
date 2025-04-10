
from pathlib import Path

# 環境変数の読み込み
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# .envを読み込む
load_dotenv()

# load_certs = os.environ.get("WEBSITE_LOAD_CERTIFICATES", None)
# ssl_args = {}

# if load_certs :
#     # 複数指定されている場合は先頭のサムプリントを使用
#     thumbprint = load_certs.split(",")[0].strip()
    # Azure App Service の Linux コンテナ内で証明書は /var/ssl/certs/<サムプリント>.pem として配置される
#     cert_file = f"/var/ssl/certs/{thumbprint}.pem"
#     ssl_args["ssl"] = {"ca": cert_file}
# else:
#     ssl_args["ssl"] = {"ca": "/var/ssl/certs/DigiCertGlobalRootCA.crt.pem"}

# データベース接続情報
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

ssl_cert = str('DigiCertGlobalRootCA.crt.pem')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("nakano DATABASE_URL:",DATABASE_URL)

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl":{
            "ssl_ca":ssl_cert
        }
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

