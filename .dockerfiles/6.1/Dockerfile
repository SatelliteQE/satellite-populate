FROM python:3
MAINTAINER https://github.com/SatelliteQE

RUN git clone https://github.com/SatelliteQE/satellite-populate.git && \
  cd satellite-populate && python3 setup.py install
RUN pip install -e git+https://github.com/SatelliteQE/nailgun.git@0.28.0#egg=nailgun

ENV HOME /root/satellite-populate
WORKDIR /root/satellite-populate

EXPOSE 22

ENTRYPOINT ["satellite-populate"]
