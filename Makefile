compose:
	docker-compose -f Desafio_Engenharia_Dados/docker-compose.yml up
	
compose_down:
	docker-compose -f Desafio_Engenharia_Dados/docker-compose.yml down
	
build:
	docker build --tag process_conect  banco_processamento/.

insert: container_processamento_run
	docker restart flask

container_processamento_build:
	 docker build -t processamento_conectbd .

container_processamento_run:
	#docker run --link containerbd --net desafio_engenharia_dados_default  processamento_conectbd
	docker run  --link containerbd --net desafio_engenharia_dados_default  -it processamento_conectbd ./process_insert.sh