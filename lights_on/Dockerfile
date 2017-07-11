FROM python:3.6
WORKDIR /lum
ADD . /lum
RUN pip install -r requirements.txt
EXPOSE 8888
CMD ["jupyter", "notebook", "--no-browser", "--ip=127.0.0.1"]
