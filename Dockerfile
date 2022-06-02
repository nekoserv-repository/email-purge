FROM python:3.10-alpine

# Dokerfile's infos
LABEL maintainer="nekoserv" mail="nekoserv@fai.tld"
LABEL description="Alpine + python3 + email purge service"
LABEL website="https://github.com/nekoserv-repository/email-purge"
LABEL version="1.0"

# init
ARG UID
ARG GID

# install
RUN [[ -z "$UID" ]] && UID=$(( $RANDOM % 9000 + 1000 )) || UID=$UID && \
    [[ -z "$GID" ]] && GID=$(( $RANDOM % 9000 + 1000 )) || GID=$UID && \
    addgroup -g $GID user && \
    adduser -S -u $UID -G user user && \
    apk add --no-cache curl tzdata unzip gcc libxml2-dev libxslt libxslt-dev musl-dev && \
    curl -L https://github.com/nekoserv-repository/email-purge/archive/main.zip -o main.zip && \
    unzip -q main.zip -d /home/user && \
    chown -R user:user /home/user && \
    python -m pip install --upgrade pip && \
    pip install -r /home/user/email-purge-main/requirements.txt && \
    rm main.zip && \
    rm -rf /root/.cache/pip/ && \
    apk del --purge curl unzip gcc libxml2-dev libxslt-dev musl-dev

# drop privileges
USER user

# run!
ENTRYPOINT ["python", "-u", "/home/user/email-purge-main/main.py"]
