FROM python:3.9
FROM ubuntu

RUN apt-get update && apt-get install -y python3-pip && apt-get install -y git

RUN python3 -m pip install --user virtualenv

RUN apt install python3.10-venv --assume-yes

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install git+https://github.com/sethengland/TikTokPy.git

RUN pip install playwright

RUN python3 -m playwright install

RUN playwright install-deps

WORKDIR /app

COPY . /app/

CMD ["python3", "main.py"]