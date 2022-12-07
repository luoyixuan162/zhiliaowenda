"""
装饰器
检测用户是否登录
"""


from flask import g,redirect,url_for
from functools import wraps


def login_required(func):
    # 保留func的信息。func就是被监测的函数
    """
    @login_required
    def public_question():    func就是public_question函数
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, "user"):
            return func(*args, **kwargs)

        else:
            return redirect(url_for("user.login"))

    return wrapper
