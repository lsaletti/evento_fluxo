#coding: utf-8
import psycopg2
import pandas as pd
import os


con = psycopg2.connect(host='containerbd',port=5432, database='postgres', user='postgres', password='')
cur = con.cursor()

psql_dele_dias_semana = 'TRUNCATE TABLE tbl_dias_semana;'
con.commit()
cur.execute(psql_dele_dias_semana)

psql_dele_fluxo_pessoa = 'TRUNCATE TABLE tbl_fluxo_pessoa;'
con.commit()
cur.execute(psql_dele_fluxo_pessoa)

psql_dele_concorrente = 'TRUNCATE TABLE tbl_concorrente;'
con.commit()
cur.execute(psql_dele_concorrente)

psql_delete_bairro = 'TRUNCATE TABLE tbl_bairro CASCADE;'
con.commit()
cur.execute(psql_delete_bairro)

psql="copy tbl_bairro from '/banco_processamento/Resource/bairro_populacao.csv' with delimiter ';' csv header encoding 'windows-1251';"

psql2 ="copy tbl_concorrente FROM '/banco_processamento/Resource/concorrente_normalizada.csv' DELIMITER ';' CSV HEADER;"

psql3 = "copy tbl_fluxo_pessoa FROM '/banco_processamento/Resource/fluxo_medio_pessoas.csv' DELIMITER ';' CSV HEADER;"

psql4 = "copy tbl_dias_semana FROM '/banco_processamento/Resource/tbl_dias_semana.csv' DELIMITER ';' CSV HEADER;"

con.commit()
cur.execute(psql)
con.commit()
cur.execute(psql2)
con.commit()
cur.execute(psql3)
con.commit()
cur.execute(psql4)
con.commit()
#os.system("docker restart flask")
