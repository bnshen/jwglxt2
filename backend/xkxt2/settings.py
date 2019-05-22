from datetime import timedelta

class config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asajsfa1o3mfp1p3kpwofkwpkfpewkeopskpda'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)  # 配置过期时间
