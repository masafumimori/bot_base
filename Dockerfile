# FROM tensorflow/tensorflow:latest
FROM python:3.8-slim

WORKDIR /projects/bots

RUN pip install --upgrade pip

###################
# TO INSTALL TA-LIB
###################
# RUN apt update
# RUN apt-get install -y wget make build-essential graphviz
# RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
#     tar -xvzf ta-lib-0.4.0-src.tar.gz && \
#     cd ta-lib/ && \
#     ./configure --prefix=/usr && \
#     make && \
#     make install
# RUN pip install TA-Lib
# RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz
###################
# TO INSTALL TA-LIB
###################

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token='sevas'", "--port=8080"]