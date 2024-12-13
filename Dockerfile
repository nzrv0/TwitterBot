FROM selenium/standalone-chrome
# RUN sudo apt-get update && sudo apt-get install -y ffmpeg

WORKDIR /code

COPY ./requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY ./src ./src

# CMD ["python3", "src/api.py"]
