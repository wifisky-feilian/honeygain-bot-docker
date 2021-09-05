#基于的基础镜像
FROM python:3.8

#代码添加到code文件夹
ADD ./docker_honeygain-bot /honeygain-bot

# 设置code文件夹是工作目录
WORKDIR /honeygain-bot

# 安装支持
RUN pip install -r requirements.txt

CMD ["python", "/honeygain-bot/main.py"]
