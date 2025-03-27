FROM postgres:15

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15 \
    postgresql-client-15 \
    && rm -rf /var/lib/apt/lists/*


RUN git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && rm -rf /tmp/pgvector


ENV POSTGRES_DB=weather_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password


EXPOSE 5432

