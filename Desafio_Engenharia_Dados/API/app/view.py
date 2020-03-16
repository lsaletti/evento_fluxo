import psycopg2
import pandas as pd
import sys

from flask import Flask,jsonify
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def lendo_banco():
     con = psycopg2.connect(host='containerbd',port=5432, database='postgres', user='postgres', password='')
     cur = con.cursor()
     psql="select * from vw_periodo_concorrente_mdfluxos_noite_bairro_nm_pop_end_vl_prec"
     df_query = pd.read_sql_query(psql, con)
     json_api = create_json_api(df_query)
     return json_api

def create_json_api(df_query):
     quantidade_exata_concorrentes = len(set(df_query['cd_concorrente']))
     concorrentes = [{} for c in range(0,quantidade_exata_concorrentes+1)]
     compare = ''
     i=0
     for (j,d) in df_query.iterrows():
          if compare !=d['cd_concorrente']:
               i+=1
               compare = d['cd_concorrente']
               concorrentes[i]['Codigo Concorrente']=d['cd_concorrente']
               concorrentes[i]['Nome concorrente']=d['nome']
               concorrentes[i]['Endereco'] = d['ds_endereco']
               concorrentes[i]['Preco praticado'] = d['vl_faixa_preco']
               concorrentes[i]['Bairro'] = d['nm_bairro']
               concorrentes[i]['Populacao'] = d['qtd_populacao']
               concorrentes[i]['Densidade'] = d['vlm_densidade']
          if compare == d['cd_concorrente']:
               if d['nm_semana'] == 'Sabado':
                    concorrentes[i]['Fluxo Medio Sabado'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Sabado']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Sabado']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Sabado']['Noite']= d['md_fluxo_noite']      
               if d['nm_semana'] == 'Segunda':
                    concorrentes[i]['Fluxo Medio Segunda'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Segunda']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Segunda']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Segunda']['Noite']= d['md_fluxo_noite']
               if d['nm_semana'] == 'Terça':
                    concorrentes[i]['Fluxo Medio Terca'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Terca']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Terca']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Terca']['Noite']= d['md_fluxo_noite']    
               if d['nm_semana'] == 'Quarta':
                    concorrentes[i]['Fluxo Medio Quarta'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Quarta']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Quarta']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Quarta']['Noite']= d['md_fluxo_noite']  
               if d['nm_semana'] == 'Quinta':
                    concorrentes[i]['Fluxo Medio Quinta'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Quinta']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Quinta']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Quinta']['Noite']= d['md_fluxo_noite']  
               if d['nm_semana'] == 'Sexta':
                    concorrentes[i]['Fluxo Medio Sexta'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Sexta']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Sexta']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Sexta']['Noite']= d['md_fluxo_noite']  
               if d['nm_semana'] == 'Domingo':
                    concorrentes[i]['Fluxo Medio Domingo'] = {'Manha':'','Tarde':'','Noite': ''}
                    concorrentes[i]['Fluxo Medio Domingo']['Manha']=d['md_fluxo_manha']
                    concorrentes[i]['Fluxo Medio Domingo']['Tarde']= d['md_fluxo_tarde']        
                    concorrentes[i]['Fluxo Medio Domingo']['Noite']= d['md_fluxo_noite']  

     return concorrentes

json_concorrentes = lendo_banco()

@app.route('/',methods=['GET'])
def home():
    lendo_banco()
    return "HELLOW API DESENVOLVIDA",200


@app.route('/concorrentes',methods=['GET'])
def principal():   
    return jsonify(json_concorrentes),200


@app.route('/concorrentes/<int:lang>',methods=['GET'])
def concorrente_especifico(lang):
     for c in lendo_banco():
          if c.get("Codigo Concorrente") == lang:
          #if c["Codigo Concorrente"] == lang:
               return jsonify(c),200

if __name__ == '__main__':
     lendo_banco()     
     app.run(host='flask', port='5003', debug=True)

