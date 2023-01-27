FROM mcr.microsoft.com/azure-cli:latest

WORKDIR /app

RUN python -m venv env \
&& source env/bin/activate \ 
&& pip install azure-cosmos \ 
&& pip install boto3

COPY migrate.py ./
