FROM python:3

WORKDIR /root/yuna-api

COPY . /root/yuna-api
RUN pip install -r requirements.txt

ENV PYTHONPATH /root/yuna-api

EXPOSE 80
CMD [ "python", "main.py" ]
