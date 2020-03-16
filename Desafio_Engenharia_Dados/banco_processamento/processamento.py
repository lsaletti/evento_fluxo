import pandas as pd
import re
from pandas import DataFrame
import os
import sys
cont = 0

# ELIMANDO COLUNAS CONCRRENTE
def novo_concorrente(concorrente):
        concorrente_normalizada = concorrente[['codigo','codigo_bairro','nome','categoria','faixa_preco','endereco']]
        concorrente_normalizada.to_csv('Resource/concorrente_normalizada.csv',sep=';',index=False)
        

def novo_bairro(bairro,populacao):
        # MERGE ENTRE A TABELA BAIRRO E POPULACAO    
        bairro_populacao=bairro.merge(populacao,left_on='codigo',right_on='codigo')
        # CALCULANDO DENSIDADE DO BAIRRO
        bairro_populacao['vlm_densidade']=bairro_populacao['populacao']/bairro_populacao['area']
        bairro_populacao.to_csv('Resource/bairro_populacao.csv',sep=';',index=False)
      

# CALCULO DIA DA SEMANA ATRAVÉS DAS DATAS
"""
0 - SABADO

1 - DOMINGO

2 - SEGUNDA

3 - TERÇA

4 - QUARTA

5 - QUINTA

6 - SEXTA
"""


# CALCULANDO DIA DA SEMANA E SEPARANDO HORAS DA DATA


def calculo_dias(eventos_fluxo):
    list_fluxo_de_pessoas_com_dia_horas = []
    for j,(i,row) in  enumerate(eventos_fluxo.iterrows()):
            ##REGEX PARA SEPARAR A DATA DAS HORAS
            data=re.search('\d{4}\-\d{2}\-\d{2}',row['datetime']).group()##ano/mes/dia
            hours = re.search('\d{2}\:\d{2}\:\d{2}',row['datetime']).group()
            row['datetime']=row['datetime'].replace(hours,'')
            row['datetime']=row['datetime'].replace(row['datetime'],data)
            ##QUEBRANDO DATA EM DIA , MES , ANO
            ano=data.split('-')[0]
            mes=data.split('-')[1]
            dia = data.split('-')[2]
            ##CALCULO PARA DESCOBRIR O DIA DA SEMANA 
            dia_semana = int(dia)+(2*int(mes))+(3*(int(mes)+1)/5)+int(ano)+(int(ano)/4)-(int(ano)/100)+(int(ano)/400)+2
            dia_da_semana_numero=int(dia_semana % 7)
            ##ATRIBUINDO DIA DA SEMANA E HORAS AOS SEUS RESPECTIVOS CAMPOS
            row['dias_semana'] = dia_da_semana_numero
            row['horas'] = hours
            ###ADICIONANDO OS DADOS A UMA NOVA LISTA
            list_fluxo_de_pessoas_com_dia_horas.append(row)
            ##CHAMADA DE FUNÇÃO
          
    conta_periodos(list_fluxo_de_pessoas_com_dia_horas)

    # DEFINIDO PERIODOS' 
    # PERIODO   MANHÃ = 1   TARDE =2  NOITE = 3
    #CRIANDO COLUNAS DO DIA SEMANA 
def conta_periodos(list_fluxo_de_pessoas_com_dia_horas):
     ##CRIANDO DATAFRAME FLUXO DE PESSOAS COM DIAS E HORAS
    df_fluxo_de_pessoas_com_dia_horas=pd.DataFrame(list_fluxo_de_pessoas_com_dia_horas)
    df_fluxo_de_pessoas_com_dia_horas['manha']= 0
    df_fluxo_de_pessoas_com_dia_horas['tarde']= 0
    df_fluxo_de_pessoas_com_dia_horas['noite'] = 0
    df_fluxo_de_pessoas_com_dia_horas['periodo'] =0
    #CRIANDO A VARIAVEL LISTA DE FLUXOS DE PESSOAS COM DIAS HORAS E SEMANA 
    lista_fluxo_de_pessoas_com_dia_horas_semana =[]
    for (i,row1) in df_fluxo_de_pessoas_com_dia_horas.iterrows():
            ###VERIFICANO AS HORAS DA SEMANA E ATRIBUINDO 1  A CADA PERIODO ENCONTRADO
            if row1['horas'] > '00:00:00' and row1['horas'] <= '12:00:00' :
                row1['manha'] = row1['manha']+ 1
                row1['periodo'] = 1
            if row1['horas']>'12:00:00' and row1['horas']<= '18:00:00':
                row1['tarde'] = row1['tarde'] + 1
                row1['periodo'] = 2
            if row1['horas'] > '18:00:00' and  row1['horas'] <= '23:00:00':
                row1['noite'] = row1['noite']+1
                row1['periodo'] = 3
            ##AtRIBUINDO O NOVO RESULTADO A LISTA       
            lista_fluxo_de_pessoas_com_dia_horas_semana.append(row1)
            ##CHAMADA DE FUNÇÃO
    calcula_dias(lista_fluxo_de_pessoas_com_dia_horas_semana)

def calcula_dias(lista_fluxo_de_pessoas_com_dia_horas_semana):
    # codigo responsavel por calcular a quantidadde de dias na semana
    quantidade_dias_por_periodo = pd.DataFrame(lista_fluxo_de_pessoas_com_dia_horas_semana)
    quantidade_dias_por_periodo['manha']= 0
    quantidade_dias_por_periodo['tarde']= 0
    quantidade_dias_por_periodo['noite']= 0
    quantidade_dias_por_periodo2= quantidade_dias_por_periodo[['datetime','codigo_concorrente','dias_semana','manha','tarde','noite','periodo']]
    a=quantidade_dias_por_periodo2.drop_duplicates()
    #a.loc['codigo_concorrente','manha']= ''     
    lista_dias_semana_periodo =[]
    for (i,row2) in a.iterrows():     
            if row2['periodo'] == 1:
                row2['manha'] = row2['manha']+ 1
            if row2['periodo']==2:
                row2['tarde'] = row2['tarde'] + 1
            if row2['periodo'] == 3:
                row2['noite'] = row2['noite']+1
            lista_dias_semana_periodo.append(row2)
    ##CHAMADA DE FUNÇÃO
    agrupa_soma_dias(lista_fluxo_de_pessoas_com_dia_horas_semana,lista_dias_semana_periodo)    
    
def agrupa_soma_dias(lista_fluxo_de_pessoas_com_dia_horas_semana,lista_dias_semana_periodo):
    df_lista_dias_semana_periodo = pd.DataFrame(lista_dias_semana_periodo)
    r=df_lista_dias_semana_periodo[['datetime','codigo_concorrente','dias_semana','manha','tarde','noite']]
    soma_manha=r.groupby(['codigo_concorrente','dias_semana']).manha.sum()
    soma_tarde =r.groupby(['codigo_concorrente','dias_semana']).tarde.sum()
    soma_noite =r.groupby(['codigo_concorrente','dias_semana']).noite.sum()
    df_noite=pd.DataFrame(soma_noite)
    df_tarde=pd.DataFrame(soma_tarde)
    df_manha= pd.DataFrame(soma_manha)
    ###UNINDO TODOS OS FRAMES DE PERIODO
    df_quantidade_de_dias_semana = pd.concat([df_manha, df_tarde,df_noite], axis=1, sort=False)
    ###CHAMADA DE FUNÇÃO
    soma_pessoas(lista_fluxo_de_pessoas_com_dia_horas_semana,df_quantidade_de_dias_semana)



    # codigo responsavel por calcular a quantidade de pessoas em cada periodo
def  soma_pessoas(lista_fluxo_de_pessoas_com_dia_horas_semana,df_quantidade_de_dias_semana):
    ##CRIANDO O DATA FRAME LISTA DE PESSOAS COM DIA E HORAS E SEbanco_processamentoMANA
    df_lista_fluxo_de_pessoas_com_dia_horas_semana=pd.DataFrame(lista_fluxo_de_pessoas_com_dia_horas_semana)
    ##INICIO DA DEFINIÇÃO DA TABELA FLUXO DE PESSSOAS DEFININDO AS COLUNAS QUE SERÃO UTILIZADAS
    v=df_lista_fluxo_de_pessoas_com_dia_horas_semana[['dias_semana','manha','tarde','noite','codigo_concorrente']]
    ##AGRUPANDO QUANTIDADE DE PESSOAS DE MESMO PERIODO E MESMO CODIGO CONCORRENTE
    soma_manha=v.groupby(['codigo_concorrente','dias_semana']).manha.sum()
    soma_tarde =v.groupby(['codigo_concorrente','dias_semana']).tarde.sum()
    soma_noite =v.groupby(['codigo_concorrente','dias_semana']).noite.sum()
    ##CRIANDO UM DATA FRAME PARA CADA PERIODO
    df_noite=pd.DataFrame(soma_noite)
    df_tarde=pd.DataFrame(soma_tarde)
    df_manha= pd.DataFrame(soma_manha)
    ###UNINDO TODOS OS FRAMES DE PERIODO
    df_fluxo_de_pessoas = pd.concat([df_manha, df_tarde,df_noite], axis=1, sort=False)
    ####CHAMADA DE FUNÇÃO
    media_fluxo_pessoas(df_fluxo_de_pessoas,df_quantidade_de_dias_semana)
    
def media_fluxo_pessoas(df_fluxo_de_pessoas,df_quantidade_de_dias_semana):   
    ##CRIANDO O CSV DE FLUXO DE PESSOAS
    df_fluxo_de_pessoas.to_csv('Fluxo de pessoas.csv',sep=';',index=True)
    a=df_fluxo_de_pessoas['manha']/df_quantidade_de_dias_semana['manha']
    b=df_fluxo_de_pessoas['tarde']/df_quantidade_de_dias_semana['tarde']
    c=df_fluxo_de_pessoas['noite']/df_quantidade_de_dias_semana['noite']
    df_fluxo_medio_pessoas = pd.concat([a, b,c], axis=1, sort=False)
    ####CRIAÇÃO DO FLUXXOO
    df_fluxo_medio_pessoas.to_csv('Resource/fluxo_medio_pessoas.csv',sep=';',index=True)






if __name__ == "__main__":
    
    ####CONCORRENTE
    #path_current = os.getcwd()
    #path_complet_with_csv = '/Dados_Cliente/concorrentes.csv'
    df_concorrente = pd.read_csv('Dados_Cliente/concorrentes.csv')
    novo_concorrente(df_concorrente)
    ###BAIRRRO
    #path_complet_with_csv = os.path.join(path_current +'/Dados_Cliente/populacao.json')
    populacao = pd.read_json('Dados_Cliente/populacao.json')
    populacao = pd.DataFrame(data=populacao)

    #path_complet_with_csv = os.path.join(path_current +'/Dados_Cliente/bairros.csv')
    bairro = pd.read_csv('Dados_Cliente/bairros.csv')
    novo_bairro(bairro,populacao)

    ###CHAMANDO EVENTOS
    #path_complet_with_csv = os.path.join(path_current +'/Dados_Cliente/eventos_de_fluxo.csv')
    eventos_fluxo = pd.read_csv('Dados_Cliente/eventos_de_fluxo.csv')
    calculo_dias(eventos_fluxo)
    print('Concluido')




