FROM python:3.10.7-buster

WORKDIR /.

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"] 

CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# CMD [ "python", "manage.py", "runserver"]

# RUN python manage.py runserver
