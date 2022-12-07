# 从flask包导入Flask对象 ，g 是全局变量global
from flask import Flask, session, g
# 引入配置文件
import config
# 导入蓝图 (别名已经在blueprints 文件中初始化)
from blueprints.user import bp as user_bp
from blueprints.qa import bp as qa_bp
# 从拓展文件导入冲突模块
from exts import db, mail
# 导入模型
from models import UserModel
# 导入数据库迁移
from flask_migrate import Migrate

# 使用Flask创建一个app对象，并且传递__name__参数
app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 绑定数据库并初始化
db.init_app(app)
db.app = app
# 邮箱初始实例化对象
mail.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(qa_bp)

# 钩子函数：在程序运行时插入并执行钩子函数。
# before_request/before_first_request/after_request


# 钩子函数
@app.before_request
def before_request():
    user_id = session.get("user_id")  # flask自带解密
    if user_id:
        try:
            # 通过解析session获得的id, 在数据库中查询用户
            user = UserModel.query.get(user_id)
            # 给全局变量g 绑定一个叫做user的变量，他的值就是user的值
            # setattr(g, "user", user)
            g.user = user
        except:
            # setattr(g, "user", None)
            g.user = None


# 接收请求 ->  before_request  ->  视图函数  ->  视图函数中返回模板 -> context_processor

# 上下文处理器
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1033, debug=True)
