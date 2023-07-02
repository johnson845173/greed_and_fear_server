FROM python:3.10.7-buster

WORKDIR /.

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
RUN echo "deb http://miktex.org/download/debian buster universe" | tee /etc/apt/sources.list.d/miktex.list
RUN apt-get install miktex 
RUN miktexsetup finish
RUN initexmf --set-config-value [MPM]AutoInstall=1
ENTRYPOINT ["python"] 

CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# CMD [ "python", "manage.py", "runserver"]

# RUN python manage.py runserver
