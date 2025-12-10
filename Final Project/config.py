import os

# 專案根目錄
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base 設定（所有環境共用）"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # SQLite Database 路徑
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "blog.db")

    # 上傳設定
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """開發環境"""
    DEBUG = True
    SECRET_KEY = "dev-secret-key"  # 本地固定即可


class ProductionConfig(Config):
    """正式環境（例如部署到 Render / Railway）"""
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")  # 必須從環境變數讀取
