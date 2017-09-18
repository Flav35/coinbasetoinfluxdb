from ubuntu
RUN apt -y update && apt -y install python3 python3-pip && pip3 install --upgrade pip
WORKDIR /opt
COPY requirements.txt requirements.txt
COPY coinbase_to_influxdb.py coinbase_to_influxdb.py
ENV COINBASE_API_KEY SECRET
ENV COINBASE_API_SECRET_KEY SECRET
ENV INFLUXDB_HOST localhost
RUN pip3 install -r requirements.txt
CMD python3 coinbase_to_influxdb.py
