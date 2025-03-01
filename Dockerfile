FROM python:3.11
COPY . /bot_democrat_v1.3
WORKDIR /bot_democrat_v1.3
RUN pip install --no-cache-dir -r requirements.txt
ENV REDIS_URL=${REDIS_URL}
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV LOGS_PATH=${LOGS_PATH}
ENV PATH_TO_DB=${PATH_TO_DB}

ENV TELEGRAM_LOGS_TOKEN=${TELEGRAM_LOGS_TOKEN}
ENV TG_CHATID_LOGS=${TG_CHATID_LOGS}

ENV AMO_TOKEN_MANAGER=${AMO_TOKEN_MANAGER}
ENV AMO_CLIENT_ID=${AMO_CLIENT_ID}
ENV AMO_CLIENT_SECRET=${AMO_CLIENT_SECRET}
ENV AMO_SUBDOMAIN=${AMO_SUBDOMAIN}
ENV AMO_REDIRECT_URL=${AMO_REDIRECT_URL}
ENV AMO_STORAGE_DIR=${AMO_STORAGE_DIR}

ENV ADMINS_ID=${ADMINS_ID}

CMD [ "python", "bot.py" ]
