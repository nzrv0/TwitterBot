FROM selenium/standalone-chrome

RUN sudo apt-get update; sudo apt-get install cron -y

WORKDIR /code

# create crone job script and grant privilege
COPY ./scripts ./scripts
RUN sudo chmod +x ./scripts/*.sh

# create crone and grant privilege
COPY crontab /etc/cron.d/mycron
RUN sudo  chmod 644 /etc/cron.d/mycron

COPY ./requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY ./src ./src

ENTRYPOINT sudo cron -f
