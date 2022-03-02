FROM python:alpine3.15
COPY Covid19Data/ /app/Covid19Data/
COPY static/ /app/static/
COPY templates/ /app/templates/
COPY data.py db.sqlite3 manage.py requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
EXPOSE 8000
WORKDIR /app/
ENTRYPOINT ["python3","manage.py","runserver","0.0.0.0:8000"]
#ENTRYPOINT ["/bin/sh"]