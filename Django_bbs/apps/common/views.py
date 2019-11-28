from flask import Blueprint,render_template,request
from .forms import SMSCaptcha
from utils.sms_send import send_sms
from utils import restful,bbs_cache
from tasks import send_sms_captcha,send_mail
bp = Blueprint("common",__name__,url_prefix='/common')

@bp.route('/')
def index():
    return render_template('common/index.html')


@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptcha(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = '这里应该重新写个方法生成指定位数的验证码'
        bbs_cache.set(captcha.lower(),captcha.lower())
        send_sms(telephone,captcha)
        return restful.success()
    else:
        return restful.params_error(message='参数有误')
import string
import random
@bp.route('/send_mail/')
def send_mail():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数')
    source = list(string.ascii_letters) #a-z A-Z
    source.extend(map(lambda x:str(x),range(0,10))) #混入0-9
    captcha = "".join(random.sample(source,6))
    send_mail.delay('找回论坛密码的验证码',[email],'您的验证码是:%s' % captcha)
    bbs_cache.set(email,captcha)
    return restful.success()