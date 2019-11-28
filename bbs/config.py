#encoding:utf-8
import os
from datetime import datetime,timedelta
SECRET_KEY = os.urandom(24)
#设置session的有效期为2天，若开启了session.permanet后不设置该参数，则默认为31天
PERMANENT_SESSION_LIFETIME= timedelta(days=7)

DEBUG = True

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = '1902bbs'
USERNAME = 'root'
PASSWORD = '123456'

DB_UI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset-utf8'.format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)


SQLALCHEMY_DATABASE_URI = DB_UI
SQLALCHEMY_TRACK_MODIFICATIONS= False

CMS_USER_ID = 'HEBOANHEHE'

#mail
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True #使用SSL，端口号为465或587
MAIL_USERNAME = '2241818298@qq.com'
MAIL_PASSWORD = 'pogvyhrgfincebfi'   #注意，这里的密码不是邮箱密码，而是授权码
MAIL_DEFAULT_SENDER = '22418182998@qq.com'  #默认发送者

FRONT_USER_ID = 'WFQQ132FEVFW'

#上传到本地
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')

#上传到七牛
UEDITOR_UPLOAD_TO_QINIU = True  #如果上传到七牛这里设置为True，上传到本地则为False
UEDITOR_QINIU_ACCESS_KEY = "4pMtV3F2eWZWv0TSD3DXjhcmlmVpxOCLvIdM8aF7"
UEDITOR_QINIU_SECRET_KEY = "GsmHmllZkpxOh5VAkzGrSSjCL7MQGZraQhtYmE-O"
UEDITOR_QINIU_BUCKET_NAME = "flask-1903bbs"
UEDITOR_QINIU_DOMAIN = "http://pydx8cw54.bkt.clouddn.com/"

#flask-paginate的相关配置
PER_PAGE = 6   #每页显示6篇帖子