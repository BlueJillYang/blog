FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY ./app /app
COPY ./requirements.txt /app/

RUN mkdir ~/.pip && \
    cd ~/.pip/  && \
    echo "[global] \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf

RUN pip install -r /app/requirements.txt
