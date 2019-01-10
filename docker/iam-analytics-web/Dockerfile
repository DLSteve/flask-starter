FROM iamdockerdev.azurecr.io/iam/base/azure-python

COPY ./app /flask-starter/app
COPY ./migrations /flask-starter/migrations
COPY setup.py /flask-starter/setup.py
COPY ./configs/settings.default.cfg /default/flask-starter-default.cfg
COPY ./configs/version /default/version
COPY ./docker/common/sshd_config /etc/ssh/
COPY ./docker/flask-starter-web/init.sh /usr/local/bin/

WORKDIR /flask-starter

RUN pip3 install -e .

RUN mkdir -p /mnt

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000
ENTRYPOINT ["init.sh"]