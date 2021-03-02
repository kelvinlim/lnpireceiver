FROM python:3.8
WORKDIR /project
ADD . /project

RUN pip install -r requirements.txt
CMD ["python","receiverlnpi.py"]
