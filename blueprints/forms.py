"""
Form 表单用于验证前端提交的数据是否符合要求
"""

import wtforms
from wtforms.validators import length, Email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel
from exts import db, redis_store


class RegisterForm(wtforms.Form):
    # validators 验证器
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])  # 判断是否为 email 格式数据
    captcha = wtforms.StringField(validators=[length(min=4, max=4, message="验证码格式错误")])
    username = wtforms.StringField(
        validators=[length(min=2, max=20, message="用户名格式错误：最短2位，最长20位")])  # 用户名长度
    password = wtforms.StringField(validators=[length(min=6, max=12, message="密码格式错误：最短6位，最长12位")])  # 密码长度
    # EqualTo("password") EqualTo 验证器，判断password_confirm 是否于password相等
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证：邮箱是否被注册、验证码是否正确

    # 判断邮箱是否被注册
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("该邮箱已被注册！")

    # 判断用户名是否已被注册
    def validate_username(self, field):
        username = field.data
        user_model = UserModel.query.filter_by(username=username).first()
        if user_model:
            raise wtforms.ValidationError("该用户名已被注册！")

    # 判断验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        captcha_model = redis_store.get("valid_code:{}".format(email))
        if captcha != captcha_model:
            # 抛出异常
            raise wtforms.ValidationError("验证码错误")
        elif not captcha_model:
            raise wtforms.ValidationError("验证码已过期")
        # else:
        #     # 登录后删除验证码 。。 增加了查询时间，降低了访问效率
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])  # 判断是否为 email 格式数据
    password = wtforms.StringField(validators=[length(min=6, max=20, message="密码格式错误")])  # 密码长度


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=1)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
    # question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题的id")])


class RepasswordForm(wtforms.Form):
    password1 = wtforms.StringField(validators=[length(min=6, max=20, message="密码格式错误")])  # 密码长度

    # # 验证密码是否正确
    # def validate_password(self, field):
    #     password = field.data
    #     email = self.email.data
    #     password_model = UserModel.query.filter_by(email=email, password=password).first()
    #     if not password_model:
    #         # 抛出异常
    #         raise wtforms.ValidationError("密码错误！")


class MessageForm(wtforms.Form):
    username = wtforms.StringField(
        validators=[length(min=2, max=20, message="用户名格式错误：最短2位，最长20位")])  # 用户名长度

    # 判断用户名是否已被注册
    def validate_username(self, field):
        username = field.data
        user_model = UserModel.query.filter_by(username=username).first()
        if user_model:
            raise wtforms.ValidationError("该用户名已被注册！")
