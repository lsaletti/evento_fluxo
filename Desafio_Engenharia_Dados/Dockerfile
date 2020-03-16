FROM postgres



ADD banco_processamento/ /banco_processamento/  
RUN  apt-get update  && apt-get install -y python3 &&  apt install -y python3-pip &&  apt-get install libpq-dev


#RUN chmod 777 /banco_processamento/*.csv


COPY  banco_processamento/dbconcorrente.sql  /docker-entrypoint-initdb.d/

EXPOSE 5432

