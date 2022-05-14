#
# Install python packages (and build tools)
#

FROM python:3.9 as builder
RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install gcc g++ curl -y \
    && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install --user -r requirements.txt

#
# Copy built python packages to the new image.
#

FROM python:3.9 as app
RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV SLEEP_TIMER="120"
ENV SLEEP_TIMER_MINOR="15"
ENV STORAGE_FOLDER="/storage"
VOLUME /storage

COPY --from=builder /root/.local /root/.local
COPY ./src /app/src
COPY ./bin /app/bin

CMD [ "python3", "-m", "bin.mining.run"]
