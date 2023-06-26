FROM python:3.10-slim as builder

# install package
RUN apt-get update \
    && apt-get -y install gcc libpq-dev \
    && apt-get clean \
    && pip install --upgrade pip \
    && apt-get autoclean \
    && apt-get autoremove --purge  -y \
    && rm -rf /var/lib/apt/lists/*

# setting env
RUN python -m venv /opt/virtual-env
ENV PATH="opt/virtual-env/bin:$PATH"

# install require packages
COPY ./requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install wheel \
    && python3 -m pip install  --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt


FROM python:3.10-slim-buster as final

# enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV APP=/home/app

RUN adduser app

COPY --from=builder /opt/virtual-env /opt/virtual-env
ENV PATH="/opt/virtual-env/bin:$PATH"

WORKDIR $APP

COPY . .

USER app
