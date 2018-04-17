FROM python:3
ENV PYTHONUNBUFFERED 1

ADD dysms_python /dysms_python

RUN mkdir /backend
ADD t01p3_storage_queue/ /backend/

WORKDIR /backend
RUN pip install -r requirements.txt

CMD ["python", "run.py", "--longpoll"]
