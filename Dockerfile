FROM python:3.11
COPY . /bot_democrat_v1.3
WORKDIR /bot_democrat_v1.3
RUN pip install --no-cache-dir -r requirements.txt
ENV REDIS_URL=${REDIS_URL}
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV LOGS_PATH=${LOGS_PATH}
ENV PATH_TO_DB=${PATH_TO_DB}

CMD [ "python", "bot.py" ]
