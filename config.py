class Config:
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = ""
    DATA_SECRET_KEY = ""  # 공공데이터 API 내에서 '아파트매매 실거래 상세 자료' 항목 발급받은 API SERVICE KEY


class DevelopmentConfig(Config):
    def __init__(self):
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)

        Config.SQLALCHEMY_DATABASE_URI = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
        Config.SQLALCHEMY_ECHO = config['DEFAULT']['SQLALCHEMY_ECHO']
        Config.SQLALCHEMY_TRACK_MODIFICATIONS = config['DEFAULT']['SQLALCHEMY_TRACK_MODIFICATIONS']
        Config.SECRET_KEY = config['DEFAULT']['SECRET_KEY']
        Config.DATA_SECRET_KEY = config['DEFAULT']['DATA_SECRET_KEY']
