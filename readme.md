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


## 3. Bloco 2: Análise Exploratória de Dados (EDA) - Perfil Inicial

Nesta fase, foi realizada uma análise exploratória para entender as dimensões e características básicas do dataset. O objetivo é traçar um perfil quantitativo dos dados antes de aprofundar nas análises visuais e de pré-processamento.

### 3.1. Principais Descobertas

* **Dimensões:** O conjunto de dados abrange um total de **45 lojas** e **81 departamentos** distintos.

* **Período Temporal:** Os dados de vendas se estendem de **05/02/2010** a **26/10/2012**. Este intervalo de aproximadamente 2 anos e 9 meses é robusto para a captura de padrões de vendas e sazonalidades anuais.

* **Análise de Dados Faltantes:** A verificação de valores nulos (`NaN`) revelou insights cruciais sobre a natureza dos dados:
    * **Dados Internos (`df_train`, `df_stores`):** Os dataframes de vendas e de informações das lojas estão **100% completos**, sem nenhum valor ausente, refletindo a alta qualidade dos dados operacionais internos da empresa.
    * **Dados Externos (`df_features`):** Este dataframe apresentou valores ausentes em diversas colunas:
        * **`CPI` e `Unemployment`:** Apresentam **7.14%** de dados faltantes. Isso é consistente com a natureza de dados macroeconômicos, que podem ter falhas de coleta ou defasagem na divulgação.
        * **`MarkDown1` a `MarkDown5`:** Possuem um alto índice de valores nulos, variando de **50% a 64%**. A principal hipótese é que este sistema de promoções (`MarkDowns`) não existia no início do período analisado e foi implementado pela empresa posteriormente.

Esta análise de dados faltantes é fundamental, pois define a necessidade de uma etapa de **pré-processing e limpeza** para tratar esses valores antes de unificar os dataframes e treinar o modelo de IA.

## 4. Bloco 3: Limpeza e Pré-processamento de Dados

Com base nas descobertas da EDA, esta etapa foca em preparar os dados para a modelagem, começando pelo tratamento dos valores ausentes.

### 4.1. Tratamento de Valores Ausentes (Imputação)

Foi aplicado um tratamento específico para os dados faltantes no dataframe `df_features`:

* **Colunas `MarkDown1` a `MarkDown5`:** Os valores ausentes (`NaN`) foram preenchidos com `0`. A premissa de negócio é que um valor nulo nestas colunas indica a **inexistência** de uma campanha promocional naquela semana, portanto, o valor monetário do desconto é zero.

* **Colunas `CPI` e `Unemployment`:** Para estas features, foi utilizada a técnica de **imputação pela mediana**. Os valores nulos foram preenchidos com a mediana correspondente de cada loja (`Store`). Esta abordagem preserva as características econômicas locais de cada loja e é robusta a outliers.

Após a execução do tratamento, foi verificado que o dataframe resultante (`df_features_tratado`) não contém mais valores ausentes.

### 3.2. Investigação Aprofundada dos Dados de Promoções (MarkDowns)

Durante a análise exploratória, foi identificada uma alta porcentagem de valores nulos (acima de 50%) nas cinco colunas de `MarkDown`. Para justificar a estratégia de tratamento desses dados, foi realizada uma análise temporal focada em determinar a origem desses valores ausentes.

**Metodologia e Evidências:**
A análise consistiu em identificar a primeira data de registro para cada tipo de promoção e visualizar a contagem de registros não nulos ao longo do tempo. As evidências foram conclusivas:

1.  **Data de Início:** Foi verificado que os primeiros registros de `MarkDown` no dataset datam de **Novembro de 2011**, quase dois anos após o início da coleta de dados (Fevereiro de 2010).
2.  **Visualização Temporal:** Um gráfico da contagem de registros de `MarkDown` ao longo do tempo mostrou uma linha nula até Nov/2011, seguida de um aumento súbito e expressivo, confirmando visualmente a data de implementação do sistema.

**Conclusão da Investigação:**
Esta descoberta **valida a hipótese** de que os valores nulos antes de Nov/2011 representam a **inexistência** do sistema de promoções. Portanto, a estratégia de preencher todos os valores nulos (`NaN`) de `MarkDown` com `0` (a ser executada no Bloco 3) é justificada, pois representa corretamente o valor monetário nulo da promoção naquelas semanas, seja pela ausência de uma campanha ou pela ausência do sistema em si.

### 4.2. Unificação dos Dados (Merge)

Após o tratamento de valores ausentes, os três dataframes do projeto (`df_train`, `df_stores`, `df_features_tratado`) foram consolidados em um único dataframe mestre (`df_final`) para facilitar as próximas etapas.

A unificação foi realizada em duas etapas sequenciais, utilizando a função `merge` com uma junção do tipo `inner`:

1.  **Junção de `df_train` com `df_stores`:** Utilizando a coluna `Store` como chave, as informações de tipo (`Type`) e tamanho (`Size`) de cada loja foram adicionadas aos dados de vendas.
2.  **Junção com `df_features_tratado`:** O dataframe resultante da primeira etapa foi unido ao de features, usando as colunas `Store` e `Date` como uma chave composta. Isso garantiu que cada registro de venda semanal fosse enriquecido com os dados contextuais e econômicos correspondentes.

O dataframe `df_final` resultante contém todas as features em uma única tabela, pronto para a etapa de Engenharia de Features e, subsequentemente, a modelagem.