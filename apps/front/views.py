from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    g
)

from apps.front.decorators import login_required
from .forms import SignUpForm
from .models import FrontUser
from exts import db
from utils import xjson
from utils import safeutils
import config
from .forms import SignInForm
from .forms import AddPostForm
from apps.models import BannerModel, BoardModel, PostModel
from flask_paginate import Pagination, get_page_parameter
from flask import abort

from .forms import AddCommentForm
from apps.models import CommentModel

from apps.models import HighlightPostModel
from sqlalchemy.sql import func

# from .decorators import login_required

bp = Blueprint('front', __name__)

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    boards = BoardModel.query.all()
    # comments = CommentModel.query.all()

    # 当前页面
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 开始位置
    start = (page - 1) * config.PER_PAGE
    # 结束位置
    end = start + config.PER_PAGE

    board_id = request.args.get('bd', type=int, default=None)
    # comment_id = request.args.get('bd', type=int, default=None)
    sort = request.args.get("st", type=int, default=1)
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序,点赞功能没有做，所以这里用时间倒序排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()

    # if comment_id:
    #     query_obj = query_obj.filter(PostModel.comment_id == comment_id)
    #     posts = query_obj.slice(start, end)
    #     total = query_obj.count()
    # else:
    #     posts = query_obj.slice(start, end)
    #     total = query_obj.count()


    pagination = Pagination(bs_version=3,page=page, total=total)
    context = {
        'banners': banners,
        'boards': boards,
        # 'comments':comments,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)



class SignUpViews(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        signup_form = SignUpForm(request.form)
        if signup_form.validate():
            telephone = signup_form.telephone.data
            username = signup_form.username.data
            password = signup_form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return xjson.json_success('恭喜您，注册成功')
        else:
            return xjson.json_params_error(signup_form.get_error())


bp.add_url_rule('/signup/', view_func=SignUpViews.as_view('signup'))


class SignInViews(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        return render_template('front/front_signin.html')


    def post(self):
        signin_form = SignInForm(request.form)
        if signin_form.validate():
            telephone = signin_form.telephone.data
            password = signin_form.password.data
            remember = signin_form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.premanent = True
                return xjson.json_success('登陆成功')
            else:
                return xjson.json_params_error('手机号或密码错误')
        else:
            return xjson.json_params_error(signin_form.get_error())

bp.add_url_rule('/signin/', view_func=SignInViews.as_view('signin'))



@bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        add_post_form = AddPostForm(request.form)
        if add_post_form.validate():
            title = add_post_form.title.data
            content = add_post_form.content.data
            board_id = add_post_form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return xjson.json_param_error(message='没有这个板块')
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_param_error(message=add_post_form.get_error())

@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post)

@bp.route('/comment/',methods=['POST'])
@login_required
def add_comment():
    add_comment_form = AddCommentForm(request.form)
    if add_comment_form.validate():
        content = add_comment_form.content.data
        post_id = add_comment_form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return xjson.json_success()
        else:
            return xjson.json_param_error('没有这篇帖子！')
    else:
        return xjson.json_param_error(add_comment_form.get_error())


