from flask import flash, jsonify, Blueprint, render_template, request, redirect, url_for, session, g, current_app
from exts import mail, db, redis_store
from flask_mail import Message  # 导入邮箱信息
from models import EmailCaptchaModel, UserModel
# 导入字符串和随即库用于生成验证码
import string
import random
import datetime

from datetime import datetime
from .forms import RegisterForm, LoginForm, RepasswordForm, MessageForm
from werkzeug.security import generate_password_hash, check_password_hash

# 引入装饰器
from decorators import login_required

bp = Blueprint("user", __name__, url_prefix="/user")  # url_prefix :设置url前缀


#  /user/register  注册
# GET: 客户端从服务器端获取数据
# POST：将客户端数据提交到服务器
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')  # 返回页面
    elif request.method == "POST":
        form = RegisterForm(request.form)  # 将request.form获取的数据给RegisterForm进行格式验证
        if form.validate():  # 如果验证串成功
            email = form.email.data
            username = form.username.data
            sex = request.form["sex"]
            # md5 加密
            password = form.password.data
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password,sex=sex)
            # try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
            # except:
            #     db.session.rollback()
            #     return redirect(url_for('user.register'))
        else:
            return redirect(url_for('user.register'))


# 登录
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            form_check_label = request.form.get("form-check-label")
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("邮箱未注册！")
                return redirect(url_for("user.login"))
            elif user and check_password_hash(user.password, password):
                # 使用session存放用户信息
                session["user_id"] = user.id
                if form_check_label:
                    """
                    permanent是“永久”的意思，
                    如果设置了此项为True，
                    意味着在permanent_session_lifetime过期时间内即使关闭浏览器，再次打开时session还有效
                    如果设置了此项为False，
                    即使在session的有效期内关闭浏览器，也会清空session，从而导致登录失效
                    还有就是，session.permanent只能在视图内设置，不能和过期时间一起设置
                    """
                    session.permanent = True
                    bp.permanent_session_lifetime = datetime.timedelta(days=10)
                # 登录成功，返回首页
                return redirect("/")
            else:
                flash("密码错误")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱格式错误或密码长度少于6")
            return redirect(url_for("user.login"))


# 退出登录
@bp.route("/logout")
def logout():
    # 清除session中的数据
    session.clear()
    return redirect(url_for("user.login"))


# 生成验证码并通过邮箱发送
@bp.route("/captcha", methods=["POST"])
def get_captcha():
    # POST传参  获取用户注册时输入的邮箱
    email = request.form.get('email')
    # 生成验证码
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:  # 如果填入邮箱则进行以下处理
        # 实例化信息
        message = Message(
            subject='知了问答注册',  # 主题
            recipients=[email],  # 收件人,多人用';'间隔
            body=f'【知了问答】您的注册验证码是:{captcha},有效时间为两分钟。请确认该操作是本人执行。',  # 内容
            # html=None,  # 样式
            sender='1902206219@qq.com'  # 发送者
            # cc=None,
            # bcc=None,
            # attachments=None,
            # reply_to=None,
            # date=None,
            # charset=None,
            # extra_headers=None,
            # mail_options=None,
            # rcpt_options=None
        )
        # 发送邮箱
        mail.send(message)
        # 查询数据库是否存在该邮箱和验证码，若存在则更新邮箱对应的验证码
        # 可以使用redis存储验证码
        # captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()  # 通过邮箱查询对应的邮箱验证码
        # captcha_model = redis_store.get("valid_code:{}".format(email))
        # 如果存在验证码
        # if captcha_model:
        #     captcha_model.captcha = captcha
        #     captcha_model.creat_time = datetime.now()
        #     db.session.commit()
        # else:
        #     captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
        # db.session.add(captcha_model)
        # db.session.commit()
        # 将验证码保存到redis中，第一个参数是key(邮箱)，第二个参数是value（验证码），第三个参数表示120秒后过期
        redis_store.set("valid_code:{}".format(email), captcha, 120)
        return jsonify({"code": 200, "message": "验证码发送成功"})
    else:
        # 400 为客户端错误
        return jsonify({"code": 400, "message": "请先传递邮箱"})


# 更改密码
@bp.route("/repassword", methods=["GET", "POST"])
def repassword():
    if request.method == "GET":
        return render_template("repassword.html")

    else:
        form = RepasswordForm(request.form)
        user = g.user
        password0 = request.form.get('password0')
        password1 = form.password1.data
        password2 = request.form.get('password2')
        # 输入的原密码错误
        if not check_password_hash(user.password, password0):
            flash("密码错误")
            return redirect(url_for("user.repassword"))
        # 输入的原密码正确，判断更改后的密码是否符合要求
        else:
            if form.validate():
                if password1 == password2:
                    g.user.password = generate_password_hash(password1)
                    # 清除session中的数据
                    try:
                        session.clear()
                        db.session.commit()
                        return redirect(url_for('user.login'))
                    except:
                        db.session.rollback()
                        return redirect(url_for("user.repassword"))
                else:
                    flash("更改后的两次密码不一致")
                    return redirect(url_for("user.repassword"))
            else:
                flash("密码格式错误：至少6位，最多20位")
                return redirect(url_for("user.repassword"))


# 用户信息视图
@bp.route('/user_message', methods=['GET', 'POST'])
@login_required
def user_message():
    # 获取用户名
    user = g.user
    username = user.username
    # 获取用户对象
    user = UserModel.query.filter_by(username=username).first()
    # # 将用户对象装换成用户字典
    # user_dict = user.to_dict()

    # 根据请求方式不同做出不同的响应
    if request.method == 'GET':
        # return render_template('test/user_message.html', user=user_dict)
        return render_template('user_message.html')
    # 获取用户输入并更新数据库
    else:
        form = MessageForm(request.form)
        username = form.username.data
        sex = request.form.get('sex')
        avatar = request.files.get('avatar')

        # 如果上传了头像才保存和更新数据库的头像信息
        if avatar:
            # 设置头像存储路径
            absolute_avatar_path = current_app.static_folder + '\images\{}.png'.format(username)
            # 保存图片
            with open(absolute_avatar_path, 'wb+') as f:
                f.write(avatar.read())
                f.close()
            user.avatar_url = absolute_avatar_path

        # 更新用户信息
        user.username = username
        user.sex = sex
        try:
            db.session.commit()
        except:
            db.session.rollback()

        # 更新session的name
        session["name"] = username

        # # 将更新后的对象装换成字典
        # user_dict = user.to_dict()
        # 返回更新结果
        return redirect(url_for('user.user_message'))


# 返回用户头像
@bp.route('/user_avatar', methods=["GET"])
def user_avatar():
    username = session.get('name')

    # 获取用户
    user = UserModel.query.filter_by(username=username).first()

    # 获取当前用户的头像
    avatar_url = user.avatar_url
    print(avatar_url)
    # 如果用户头像不存在，则返回默认头像
    # current_app.send_static_file("文件路径") 能返回静态文件夹里面的文件
    if not avatar_url:
        if user.sex == '男':
            print(current_app.send_static_file('static/images/nstx.png'))
            return current_app.send_static_file('static/images/nstx.png')
        if user.sex == '女':
            print(current_app.send_static_file('static/images/vstx.png'))
            return current_app.send_static_file('static/images/vstx.png')
    else:
        # 头像存在，则正常返回
        print(current_app.send_static_file('static/images/{}.png'.format(username)))
        return current_app.send_static_file('static/images/{}.png'.format(username))
