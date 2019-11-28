#https://flask.palletsprojects.com/en/1.0.x/patterns/celery/
#celery 官网
from celery import Celery
from flask_mail import Message
from exts import mail
import config
# from bbs import create_app  为了避免重复导入问题  这里注释掉

# app = create_app()
# mail.init_app(app)
#在task 任务里边 需要导入 app
#app 视图函数中 需要导入 task
from flask import Flask

app = Flask(__name__)
app.config.from_object(config) #导入config 配置文件
mail.init_app(app)
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task()
def send_sms_captcha():
    pass


@celery.task()
def send_mail(subject,recipients,body):
    message = Message(subject=subject,recipients=recipients,body=body)
    mail.send(message)

