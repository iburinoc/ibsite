FROM alpine:3.13

WORKDIR /app

RUN apk --no-cache add bash ruby git python3 py3-flask nginx
RUN apk --no-cache add ruby-dev ruby-etc
RUN gem install bundler
RUN bundle init
RUN apk --no-cache add build-base && \
    bundle add jekyll json bigdecimal && \
    apk --no-cache del build-base

ADD bg/server/bgserver.py bgserver.py
ADD entry.sh /app/

RUN mkdir -p /run/nginx /www
ADD nginx.conf /etc/nginx/http.d/ibsite.conf

# self-documentation
ADD Dockerfile /app/

EXPOSE 8000

CMD ["/bin/bash", "entry.sh"]
