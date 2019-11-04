from flask import session, g
import config
from .views import bp
from .models import CMSUser
from .models import CMSPersmission


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor  #上下文处理器, 返回的字典可以在全部模板中使用
def context_processor():
    return {'CMSPersmission':CMSPersmission}
