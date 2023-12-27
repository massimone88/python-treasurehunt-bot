FROM docker:stable

RUN apk add --no-cache python3 py3-pip curl bash \
    gcc musl-dev autoconf libffi-dev gmp-dev \
    libxml2 libxslt-dev jpeg-dev zlib-dev \
    build-base python3-dev linux-headers

RUN apk add zbar-dev --update-cache --repository \
    http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted

RUN pip3 install lxml pyzbar pillow
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "./manage.py"]