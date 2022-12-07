from flask import flash, Blueprint, redirect, url_for, render_template, request, g
from decorators import login_required
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from sqlalchemy import or_

bp = Blueprint("qa", __name__, url_prefix="/")


# 问答页就是首页
@bp.route("/")
def index():
    # questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


# 发布问答
@bp.route("/question/public", methods=["GET", "POST"])
# 判断用户是否登录，如果没有登录则无法进入问答页面。并提醒用户登录
@login_required  # 将以下函数当作一个参数，传给修饰器。在修饰器中闭包的进行判断
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


# 发布评论
# @bp.post("/answer/<int:question_id>")
@bp.route("/answer/<int:question_id>", methods=["GET","POST"])
# 判断用户是否登录，如果没有登录则无法进入问答页面。并提醒用户登录
@login_required
def answer(question_id):
    if not g.user:
        return redirect(url_for("user.login"))

    else:

        form = AnswerForm(request.form)
        if form.validate():
            content = form.content.data
            answer_model = AnswerModel(content=content, author=g.user, question_id=question_id)
            db.session.add(answer_model)
            db.session.commit()
            return redirect(url_for("qa.question_detail", question_id=question_id))
        else:
            flash("请输入评论后发布")
            return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    # url显示 /search？key=xxx
    key = request.args.get("key")  # 获取用户传输的参数,"key"为前端定义的搜索框的名称
    # filter_by 直接使用字段的名称
    # filter 使用模型.字段名称
    questions = QuestionModel.query.filter(
        # QuestionModel.title.contains(key) 标题包含关键字（key接收关键字）
        # 使用Model.Column.Contains(keyword)与filter结合来筛选指定的Column字段包含keyword的内容，由于我们的逻辑是或的关系，所以使用了一个从sqlalchemy中导出的or_函数。
        # or_(QuestionModel.title.contains(key), QuestionModel.content.contains(key))).order_by(db.text("-create_time"))
        or_(QuestionModel.title.contains(key), QuestionModel.content.contains(key))).order_by(QuestionModel.create_time.desc()).all()
    if questions:
        return render_template("index.html", questions=questions)
    else:
        return render_template("warn.html")
