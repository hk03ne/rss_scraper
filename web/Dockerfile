FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ADD . /usr/src/app/
ADD app.py ./usr/src/app/
# CMD ["python", "app.py"]
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--config", "conf.py"]

