from flask import (
    render_template,
    request,
    redirect,
    session,
    abort,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.board import Board
from models.user import User
from models.topic import Topic
from models.reply import Reply
import os
import uuid

from routes import current_user
from utils import log

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login u', u)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login', session)
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def user_detail():
    u = current_user()
    ts = topics(u.id)
    tn = topic_count(u.id)
    rs = replies(u.id)
    rn = reply_count(u.id)

    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u, topics=ts, topic_count=tn, Topic=Topic,  replies=rs, reply_count=rn)

def replies(id):
    ms = Reply.all(user_id=id)
    return ms

def reply_count(id):
    count = len(Reply.all(user_id=id))
    return count

def topics(id):
    ms = Topic.all(user_id=id)
    return ms

def topic_count(id):
    count = len(Topic.all(user_id=id))
    return count


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    # file 是一个上传的文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        # filename = secure_filename(file.filename)
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u = current_user()
        log('uuser',u)
        User.update(u.id, dict(
            user_image='/uploads/{}'.format(filename)
        ))

    return redirect(url_for(".profile"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)

@main.route("/setting")
def set_index():
    board_id = request.args.get('board_id', 'all')
    log('bbid:', board_id)
    u = current_user()

    # token = new_csrf_token()

    return render_template("setting.html", u=u, bid=board_id)

@main.route("/user_update", methods=["post"])
def user_update():
    form = request.form
    u = current_user()
    uid = u.id
    User.update(uid, form)
    return render_template("setting.html", u=u)

@main.route("/change_password", methods=["post"])
def change_password():
    form = request.form
    u = current_user()

    if u.password == User.salted_password(form['old_pass']):
        password = User.salted_password(form['new_pass'])
        u.new(dict(
            password=password,
        ))
        return render_template("setting.html", u=u)
    else:
        abort(501)

