FROM python:3.8

WORKDIR /opt/great-international-ui
ADD . /opt/great-international-ui/

RUN pip install -U pip
RUN make install_requirements

EXPOSE 8012

ENTRYPOINT ["make", "webserver"]
