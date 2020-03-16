-- Database: db_concorrente

--DROP DATABASE db_concorrente;

--CREATE DATABASE IF NOT EXISTS db_concorrente
--  WITH OWNER = postgres
--       ENCODING = 'UTF8'
--       TABLESPACE = pg_default
--       LC_COLLATE = 'pt_BR.UTF-8' 
--       LC_CTYPE = 'pt_BR.UTF-8'
--       CONNECTION LIMIT = -1;

CREATE TABLE public.TBL_DIAS_SEMANA (
                cd_dias_semana NUMERIC NOT NULL,  
                nm_semana VARCHAR NOT NULL,
                CONSTRAINT cd_dia_semana PRIMARY KEY (cd_dias_semana)
);


CREATE TABLE public.TBL_BAIRRO (
                cd_bairro NUMERIC NOT NULL,
                nm_bairro VARCHAR NOT NULL,
                nm_municipio VARCHAR NOT NULL,
                nm_uf VARCHAR NOT NULL,
                tm_area DOUBLE PRECISION NOT NULL,
                qtd_populacao NUMERIC NULL,
                vlm_densidade REAL  NULL,
                CONSTRAINT cd_bairro PRIMARY KEY (cd_bairro)
);


CREATE TABLE public.TBL_CONCORRENTE (
		cd_concorrente NUMERIC NOT NULL,                
		cd_bairro NUMERIC  NULL,
                nome VARCHAR NOT NULL,
                ds_categoria VARCHAR NOT NULL,
                vl_faixa_preco REAL NOT NULL,
                ds_endereco VARCHAR ,
                CONSTRAINT cd_concorrente PRIMARY KEY (cd_concorrente)
);


CREATE TABLE public.TBL_FLUXO_PESSOA (
                --cd_fluxo_pessoa NUMERIC NOT NULL,
                cd_concorrente NUMERIC NOT NULL,
                cd_dias_semana NUMERIC NOT NULL,
                --cd_bairro NUMERIC,
                md_fluxo_manha NUMERIC  NULL,
                md_fluxo_noite NUMERIC  NULL,
                md_fluxo_tarde NUMERIC NULL
                --CONSTRAINT cd_fluxo_pessoa PRIMARY KEY (cd_concorrente)
);



ALTER TABLE public.TBL_CONCORRENTE ADD CONSTRAINT fk_bairro_concorrente
FOREIGN KEY (cd_bairro)
REFERENCES public.TBL_BAIRRO (cd_bairro)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;


CREATE OR REPLACE VIEW public.vw_periodo_concorrente_mdfluxos_noite_bairro_nm_pop_end_vl_prec AS 
 SELECT tbl_fluxo_pessoa.cd_concorrente,
    tbl_fluxo_pessoa.md_fluxo_manha,
    tbl_dias_semana.nm_semana,
    tbl_concorrente.nome,
    tbl_fluxo_pessoa.md_fluxo_tarde,
    tbl_fluxo_pessoa.md_fluxo_noite,
    tbl_bairro.nm_bairro,
    tbl_bairro.qtd_populacao,
    tbl_bairro.vlm_densidade,
    tbl_concorrente.ds_endereco,
    tbl_concorrente.vl_faixa_preco
   FROM tbl_fluxo_pessoa
     JOIN tbl_dias_semana ON tbl_dias_semana.cd_dias_semana = tbl_fluxo_pessoa.cd_dias_semana
     JOIN tbl_concorrente ON tbl_fluxo_pessoa.cd_concorrente = tbl_concorrente.cd_concorrente
     JOIN tbl_bairro ON tbl_concorrente.cd_bairro = tbl_bairro.cd_bairro;

ALTER TABLE public.vw_periodo_concorrente_mdfluxos_noite_bairro_nm_pop_end_vl_prec
  OWNER TO postgres;

