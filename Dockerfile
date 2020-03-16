From python:3.7

RUN  apt-get update && apt-get install -y libpq-dev && pip install --upgrade pip && pip install pandas &&  pip install psycopg2 

ADD  Desafio_Engenharia_Dados/banco_processamento/  /banco_processamento/
RUN chmod 777 /banco_processamento/*.sh


WORKDIR /banco_processamento

#ENTRYPOINT ["process_insert.sh"]


#CMD ["process_insert.sh"]