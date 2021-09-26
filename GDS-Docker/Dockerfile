FROM python:3.6-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add gcc && \
    apk add musl-dev && \
    apk add bash && \
    mkdir /usr/local/lib/python3.6/site-packages/eoitek_gds && \
    pip install aiohttp -i https://pypi.doubanio.com/simple && \
    pip install requests -i https://pypi.doubanio.com/simple && \
    pip install faker -i https://pypi.doubanio.com/simple

COPY eoitek_gds /usr/local/lib/python3.6/site-packages/eoitek_gds

WORKDIR /usr/local/lib/python3.6/site-packages/eoitek_gds

CMD [ "python", "GdsAPI.py" ]