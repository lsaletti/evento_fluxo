## *** Evento de Fluxo***
O Projeto tem como objetivo de calcular e disponibilizar o fluxo de pessoas.

----------


#### Inicialização
Comando para realizar o Build das imagens que serão utilizados.

```bash
make compose
```

Comando para rodar os serviços que serão utilizados.

```bash
make container_processamento_build
make insert
```
----------

####  ***API***

Get fluxo por concorrentes.

```bash
http://127.0.0.1:5003/concorrentes
```
ou
```bash
http://127.0.0.1:5003/concorrentes
```
```

----------
