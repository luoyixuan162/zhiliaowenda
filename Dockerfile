# 使用python3.8
FROM python:3.8
# 设置工作目录
WORKDIR /zhiliaowenda
# 拷贝app.py 到工作目录下
COPY . /zhiliaowenda
COPY requirements.txt requirements.txt
# 安装
RUN ["pip", "install", "-r", "requirements.txt"]
# 使用 python 执行 app.py
CMD ["python","app.py"]
