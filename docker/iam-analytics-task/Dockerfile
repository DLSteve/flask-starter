FROM iamdockerdev.azurecr.io/iam/base/azure-python

COPY ./app /flask-starter/app
COPY ./migrations /flask-starter/migrations
COPY setup.py /flask-starter/setup.py
COPY ./configs/settings.default.cfg /default/flask-starter-default.cfg
COPY ./docker/flask-starter-task/init.sh /usr/local/bin/


RUN adduser celery --system --disabled-password --group --shell /bin/bash
RUN echo celery:celery | chpasswd
RUN passwd -l celery

RUN mkdir -p /mnt
RUN chown celery:celery -R /flask-starter

WORKDIR /flask-starter

RUN su celery -c "pip3 install --user -e ."
RUN chmod u+x /usr/local/bin/init.sh

ENTRYPOINT ["init.sh"]