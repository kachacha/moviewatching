FROM registry.zylliondata.local/centos:7-python-3.6

LABEL io.k8s.description="爬虫翻译工具（Translate Tool）" \
    io.k8s.display-name="爬虫翻译工具" \
    io.openshift.expose-services="8000:http" \
    io.openshift.tags="Scoring,idsg,ioData,d4i,flask"

WORKDIR /opt/app
ENV HOME /opt/app
ADD . /opt/app
ADD localtime /etc/localtime
RUN  yum install epel-release   -y \
    && yum install nodejs   -y

RUN yum install cyrus-sasl-* python36u-devel gcc-c++ -y && pip3.6 install -r requirements.txt \
    --upgrade --index-url=https://pypi.tuna.tsinghua.edu.cn/simple \
    && chown -R 1001:0 /opt/app \
    && chmod -R 777 /opt/app


USER 1001
EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["-b 0.0.0.0:5000", "app:app","-k gevent","-w 4"]
