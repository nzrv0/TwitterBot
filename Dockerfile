FROM selenium/standalone-chrome

USER root

RUN sudo apt-get update; sudo apt-get install cron -y

WORKDIR /code

# create crone job script and grant privilege
COPY ./scripts ./scripts
RUN sudo chmod +x ./scripts/*.sh

# create crone and grant privilege
COPY crontab /etc/cron.d/mycron
RUN sudo chmod 644 /etc/cron.d/mycron

COPY ./requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY /src /code/src
COPY /logs /code/logs

RUN sudo chmod +x ./src/*.py

RUN crontab /etc/cron.d/mycron

ENTRYPOINT sudo cron -f

CMD [ "flask", "run" ]