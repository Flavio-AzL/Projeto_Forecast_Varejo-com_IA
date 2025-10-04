Projeto Integrador: Forecast de Demanda com IA no Varejo

Versão: 1.0

Data: 04 de Outubro de 2025

Autores: \[Seu Nome e dos Colegas]



1\. Objetivo do Projeto

Este projeto tem como objetivo principal o desenvolvimento de um modelo de Inteligência Artificial para realizar a previsão (forecast) de vendas semanais da rede de varejo Walmart. O modelo será treinado com dados históricos de vendas, características das lojas e fatores macroeconômicos.



Como objetivo secundário, será realizada uma análise comparativa dos padrões de venda do varejo físico (Walmart) com dados de um e-commerce do Reino Unido, buscando extrair insights sobre os diferentes comportamentos de consumo.



A aplicação final será um dashboard interativo desenvolvido com a biblioteca Streamlit.



2\. Bloco 1: Estruturação, Coleta e Carregamento dos Dados

Esta seção documenta a fase inicial do projeto, focada em definir o escopo, identificar a fonte de dados correta e realizar o carregamento inicial para análise.



2.1. Significado das Etapas Realizadas

Definição do Escopo e Fonte de Dados:



Significado: Nesta etapa crucial, foi decidido utilizar o dataset "Walmart Stores Sales Forecasting" como base principal para a construção do modelo de IA. A decisão foi tomada pela riqueza de informações, contendo dados de vendas, características de lojas e indicadores econômicos, permitindo uma modelagem mais robusta.



Identificação e Validação dos Arquivos:



Significado: O processo envolveu a pesquisa e validação da fonte de dados mais adequada e publicamente acessível no Kaggle. Foi selecionado o dataset hospedado pelo usuário "Aslan Ahmedov", garantindo que todo o time trabalhe com uma base de dados consistente e completa para os objetivos do projeto. Foram identificados três arquivos essenciais para a análise.



Carregamento dos Dados:



Significado: Utilizando a biblioteca pandas do Python, os três arquivos .csv foram carregados na memória do ambiente de desenvolvimento. Cada arquivo foi armazenado em uma estrutura de dados chamada DataFrame, que é otimizada para manipulação e análise. Esta etapa transforma os dados brutos (arquivos) em objetos com os quais podemos trabalhar programaticamente.



Inspeção Inicial:



Significado: Após o carregamento, foi realizada uma verificação preliminar nos dados. Comandos como .info() e .head() foram utilizados para:



Confirmar que os arquivos foram lidos corretamente.



Visualizar as primeiras linhas e entender a estrutura de cada tabela.



Analisar as colunas existentes, a quantidade de registros (linhas) e os tipos de dados (números, datas, texto). Este passo é fundamental para garantir a integridade dos dados antes de iniciar a análise exploratória.



2.2. Dicionário dos Arquivos Carregados

train.csv (DataFrame: df\_train)



Descrição: O coração do projeto. Contém os dados históricos de vendas. Cada linha representa as vendas (Weekly\_Sales) de um Departamento (Dept) específico, em uma Loja (Store) específica, em uma Data (Date) específica. É a partir daqui que nosso modelo aprenderá os padrões de venda.



stores.csv (DataFrame: df\_stores)



Descrição: Arquivo de metadados das lojas. Descreve cada loja, informando seu Tipo (Type) (A, B, ou C) e seu Tamanho (Size). Esta informação contextual é vital para o modelo entender se lojas maiores ou de um certo tipo vendem mais.



features.csv (DataFrame: df\_features)



Descrição: Arquivo de dados externos ou contextuais. Para cada loja e data, fornece informações como Temperatura (Temperature), Preço do Combustível (Fuel\_Price), Índice de Preços ao Consumidor (CPI) e Taxa de Desemprego (Unemployment). Estes fatores externos ajudam a explicar variações nas vendas que não são devidas apenas ao histórico.

