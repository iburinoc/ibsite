FROM alpine:edge

WORKDIR /app

RUN apk --no-cache add bash ruby git python3 py3-flask
RUN apk --no-cache add ruby-dev
RUN gem install bundler
RUN bundle init
RUN apk --no-cache add build-base && \
    bundle add jekyll json bigdecimal && \
    apk --no-cache del build-base

ADD bg/server/bgserver.py bgserver.py
ADD ibsite_nginx.conf /app/
ADD entry.sh /app/

# self-documentation
ADD Dockerfile /app/

EXPOSE 64156

CMD ["/bin/bash", "entry.sh"]
