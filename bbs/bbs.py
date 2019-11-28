from flask import Flask
import config
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
# from apps.uedit import bp as ueditor_bp
from exts import db
from exts import mail

from flask_wtf import CSRFProtect #表单提交防止跨站请求伪造

app = Flask(__name__)
app.config.from_object(config)  #引入配置文件

db.init_app(app)
CSRFProtect(app)
mail.init_app(app)




#注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(common_bp)
app.register_blueprint(front_bp)
# app.register_blueprint(ueditor_bp)


if __name__ == '__main__':
    app.run(debug=True)
