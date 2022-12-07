from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"  # 表名
    # 设置字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 设置主键和自动增长
    email = db.Column(db.String(100), nullable=False, unique=True)  # 不为空，且在数据库中只有一份
    captcha = db.Column(db.String(10), nullable=False)  # 不为空
    creat_time = db.Column(db.DateTime, default=datetime.now)  # 设置数据库创建时间。。若在now后面加（） 则存储的是程序运行的时间


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 设置id 为主键和自动增长
    avatar_url = db.Column(db.String(256))   # 头像
    username = db.Column(db.String(200), nullable=False, unique=True)  # 用户名 不为空，且唯一
    sex = db.Column(db.String(2))  # 性别
    email = db.Column(db.String(100), nullable=False, unique=True)  # 邮箱 不为空，且唯一
    password = db.Column(db.String(200), nullable=False)  # 不为空
    join_time = db.Column(db.DateTime, default=datetime.now)  # db.DateTime 时间类型，并将默认时间设置为当前时间


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 设置主键和自动增长
    title = db.Column(db.String(200), nullable=False)  # 不为空，且在数据库中只有一份
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 创建关联表
    author = db.relationship("UserModel", backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 设置主键和自动增长
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 引用外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 创建关联表
    question = db.relationship('QuestionModel',backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship('UserModel',backref="answers")
