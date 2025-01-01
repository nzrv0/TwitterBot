FROM selenium/standalone-chrome

WORKDIR /code

COPY ./requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY ./src ./src