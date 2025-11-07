# ==============================================================================
# Bloco 01: Configuração Inicial e Carregamento dos Dados
# ==============================================================================

# 1. Importando a biblioteca essencial para manipulação de dados
import pandas as pd

print("--- Iniciando o script de análise de vendas ---")

# 2. Definindo os caminhos para os arquivos dentro da pasta 'data'
# Usamos caminhos relativos, que funcionam em qualquer computador
# desde que a estrutura de pastas seja mantida.
caminho_treino = 'data/train.csv'
caminho_lojas = 'data/stores.csv'
caminho_features = 'data/features.csv'

# 3. Carregando os três dataframes em memória
# O bloco try-except é uma boa prática para garantir que os arquivos existem
# antes de tentar lê-los.
try:
    df_train = pd.read_csv(caminho_treino)
    df_stores = pd.read_csv(caminho_lojas)
    df_features = pd.read_csv(caminho_features)

    print("✅ Arquivos carregados com sucesso!")
    print(f"   - df_train: {df_train.shape[0]} linhas, {df_train.shape[1]} colunas")
    print(f"   - df_stores: {df_stores.shape[0]} linhas, {df_stores.shape[1]} colunas")
    print(f"   - df_features: {df_features.shape[0]} linhas, {df_features.shape[1]} colunas")

except FileNotFoundError as e:
    print(f"❌ ERRO: Arquivo não encontrado. Verifique o caminho e a estrutura de pastas.")
    print(f"   Detalhe do erro: {e}")
    # Encerra o script se os arquivos não forem encontrados
    exit()

# 4. Inspeção inicial do dataframe principal (df_train)
# Isso confirma que os dados foram carregados corretamente e nos dá uma visão inicial.
print("\n--- Informações sobre os Dados de Treino (df_train) ---")
df_train.info()

print("\n--- 5 Primeiras Linhas dos Dados de Treino (df_train) ---")
print(df_train.head())


# ==============================================================================
# Bloco 02: Análise Exploratória de Dados (EDA) - Perfil Inicial
# ==============================================================================

# Apenas para garantir que esta seção só rode se o Bloco 1 foi bem-sucedido.
if 'df_train' in locals():
    print("\n\n--- INICIANDO ANÁLISE EXPLORATÓRIA ---")

    # Pergunta 1: Quantas lojas e departamentos únicos existem no conjunto de treino?
    num_lojas = df_train['Store'].nunique()
    num_deptos = df_train['Dept'].nunique()
    print(f"\n[INFO] O dataset de treino contém dados de {num_lojas} lojas e {num_deptos} departamentos distintos.")

    # Pergunta 2: Qual o período que os dados de treino cobrem?
    # Para isso, primeiro garantimos que a coluna 'Date' seja do tipo 'datetime' para podermos
    # fazer cálculos e extrair informações de data facilmente.
    df_train['Date'] = pd.to_datetime(df_train['Date'])
    df_features['Date'] = pd.to_datetime(df_features['Date'])

    data_inicio = df_train['Date'].min()
    data_fim = df_train['Date'].max()
    print(f"[INFO] O período de análise vai de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}.")

    # Pergunta 3: Existem dados faltantes (nulos) em algum dos nossos dataframes?
    # Esta é uma das verificações mais importantes da EDA.
    print("\n--- Verificação de Dados Faltantes (Nulos) ---")
    
    print("\n[ANALYSIS] Dados de Treino (df_train):")
    print(df_train.isnull().sum())
    
    print("\n[ANALYSIS] Dados das Lojas (df_stores):")
    print(df_stores.isnull().sum())

    print("\n[ANALYSIS] Dados de Features Externas (df_features):")
    # Vamos somar os nulos e ver o percentual em relação ao total de linhas
    nulos_features = df_features.isnull().sum()
    percentual_nulos = (nulos_features / len(df_features)) * 100
    print(nulos_features[nulos_features > 0]) # Mostra apenas colunas com dados faltantes
    print("\nPercentual de dados faltantes em df_features:")
    print(percentual_nulos[percentual_nulos > 0].round(2))

else:
    print("\n❌ ERRO: Dataframes não foram carregados. Execute o Bloco 01 primeiro.")


# =============================================================================================
# Bloco 2.5: Investigação Profunda - A Origem dos Nulos em 'MarkDown'
# =============================================================================================

# Para a visualização, vamos precisar da biblioteca matplotlib
import matplotlib.pyplot as plt

if 'df_features' in locals():
    print("\n\n--- INVESTIGAÇÃO: PRIMEIRA APARIÇÃO DOS MARKDOWNS ---")

    # Para cada coluna MarkDown, encontramos a data mínima onde o valor NÃO é nulo
    data_md1 = df_features[df_features['MarkDown1'].notnull()]['Date'].min()
    data_md2 = df_features[df_features['MarkDown2'].notnull()]['Date'].min()
    data_md3 = df_features[df_features['MarkDown3'].notnull()]['Date'].min()
    data_md4 = df_features[df_features['MarkDown4'].notnull()]['Date'].min()
    data_md5 = df_features[df_features['MarkDown5'].notnull()]['Date'].min()

    print(f"\n[EVIDÊNCIA] Primeira data com valor para MarkDown1: {data_md1.strftime('%d/%m/%Y')}")
    print(f"[EVIDÊNCIA] Primeira data com valor para MarkDown2: {data_md2.strftime('%d/%m/%Y')}")
    print(f"[EVIDÊNCIA] Primeira data com valor para MarkDown3: {data_md3.strftime('%d/%m/%Y')}")
    print(f"[EVIDÊNCIA] Primeira data com valor para MarkDown4: {data_md4.strftime('%d/%m/%Y')}")
    print(f"[EVIDÊNCIA] Primeira data com valor para MarkDown5: {data_md5.strftime('%d/%m/%Y')}")

    print("\n--- VISUALIZANDO A INTRODUÇÃO DOS MARKDOWNS AO LONGO DO TEMPO ---")
    
    # Vamos contar, para cada semana, quantas entradas de MarkDown não nulas existem
    df_features_plot = df_features.copy()
    # Cria uma coluna que soma quantos MarkDowns não são nulos naquela linha (pode ir de 0 a 5)
    df_features_plot['Markdown_Count'] = df_features_plot[['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']].notnull().sum(axis=1)
    
    # Agrupa por data e soma a contagem de markdowns disponíveis
    markdown_over_time = df_features_plot.groupby('Date')['Markdown_Count'].sum()
    
    # Plotando o gráfico
    plt.figure(figsize=(15, 6))
    markdown_over_time.plot(kind='line')
    plt.title('Número de Registros de MarkDown Não Nulos ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Contagem de Registros de MarkDown')
    plt.grid(True)
    plt.show()

else:
    print("\n❌ ERRO: Dataframe df_features não foi carregado.")


# ==============================================================================
# Bloco 03: Pré-processamento - Tratamento de Dados Faltantes em df_features
# ==============================================================================

if 'df_features' in locals():
    print("\n\n--- INICIANDO LIMPEZA DE DADOS FALTANTES (df_features) ---")

    # É uma boa prática criar uma cópia para não alterar o dataframe original
    df_features_tratado = df_features.copy()

    # Estratégia 1: Preencher MarkDowns com 0
    colunas_markdown = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    df_features_tratado[colunas_markdown] = df_features_tratado[colunas_markdown].fillna(0)
    print("\n[OK] Dados faltantes de 'MarkDown' preenchidos com 0.")

    # Estratégia 2: Preencher CPI e Unemployment com a mediana da loja
    # Usamos groupby('Store') e transform('median') para calcular a mediana por loja
    # e alinhar os resultados para o preenchimento.
    df_features_tratado['CPI'] = df_features_tratado['CPI'].fillna(
        df_features_tratado.groupby('Store')['CPI'].transform('median')
    )
    df_features_tratado['Unemployment'] = df_features_tratado['Unemployment'].fillna(
        df_features_tratado.groupby('Store')['Unemployment'].transform('median')
    )
    print("[OK] Dados faltantes de 'CPI' e 'Unemployment' preenchidos com a mediana da respectiva loja.")

    # Verificação Final: Checando se ainda existem nulos no dataframe tratado
    print("\n--- Verificação Final de Nulos em df_features_tratado ---")
    nulos_restantes = df_features_tratado.isnull().sum()
    print(nulos_restantes[nulos_restantes > 0])
    
    if nulos_restantes.sum() == 0:
        print("\n✅ Sucesso! Não há mais dados faltantes em df_features_tratado.")
    else:
        print("\n⚠️ Atenção! Ainda restam dados faltantes a serem tratados.")

else:
    print("\n❌ ERRO: Dataframe df_features não foi carregado.")


# ==============================================================================
# Bloco 04: Pré-processamento - Unindo os Dataframes (Merge)
# ==============================================================================

# Verifica se os dataframes necessários existem antes de prosseguir
if 'df_train' in locals() and 'df_stores' in locals() and 'df_features_tratado' in locals():
    print("\n\n--- INICIANDO A UNIÃO DOS DATAFRAMES ---")

    # Etapa 1: Unir df_train com df_stores
    # A chave para a união é a coluna 'Store', presente em ambos.
    # Usamos how='inner' para manter apenas as lojas que existem nos dois dataframes.
    df_merged = pd.merge(df_train, df_stores, on='Store', how='inner')
    print(f"\n[OK] Merge entre df_train e df_stores concluído.")
    print(f"   - Shape antes do merge (df_train): {df_train.shape}")
    print(f"   - Shape após o merge (df_merged):  {df_merged.shape}")


    # Etapa 2: Unir o dataframe recém-criado com o df_features_tratado
    # Agora, a chave da união é composta por 'Store' e 'Date', pois as features
    # são específicas para uma loja em uma determinada semana.
    # Note que IsHoliday existe em ambos os dataframes. O merge inteligentemente
    # cria sufixos (_x, _y) para diferenciá-los. Vamos manter o do df_train.
    df_final = pd.merge(df_merged, df_features_tratado, on=['Store', 'Date'], how='inner')
    print(f"\n[OK] Merge final com df_features_tratado concluído.")
    print(f"   - Shape antes do merge (df_merged):  {df_merged.shape}")
    print(f"   - Shape do dataframe final (df_final): {df_final.shape}")

    # Verificação Final: Vamos olhar como ficou nosso dataframe final
    print("\n\n--- VERIFICAÇÃO DO DATAFRAME FINAL ---")
    df_final.info()
    
    print("\n--- 5 Primeiras Linhas do Dataframe Final ---")
    print(df_final.head())
    
    # A coluna IsHoliday ficou duplicada (IsHoliday_x, IsHoliday_y). Vamos remover a _y e renomear a _x.
    if 'IsHoliday_y' in df_final.columns:
        df_final = df_final.drop(columns=['IsHoliday_y'])
        df_final = df_final.rename(columns={'IsHoliday_x': 'IsHoliday'})
        print("\n[CLEANUP] Coluna 'IsHoliday' duplicada foi tratada.")

else:
    print("\n❌ ERRO: Um ou mais dataframes necessários para o merge não foram encontrados.")

# ==============================================================================
# Bloco 05: Engenharia de Features - Extração de Componentes de Data
# ==============================================================================

# Verifica se o dataframe final existe antes de prosseguir
if 'df_final' in locals():
    print("\n\n--- INICIANDO ENGENHARIA DE FEATURES ---")

    # É uma boa prática criar uma cópia para esta nova fase
    df_eng = df_final.copy()

    # Extraindo componentes da coluna 'Date' para novas colunas
    # O acesso a .dt permite usar propriedades de data/hora
    df_eng['Ano'] = df_eng['Date'].dt.year
    df_eng['Mes'] = df_eng['Date'].dt.month
    df_eng['Dia'] = df_eng['Date'].dt.day
    df_eng['Semana_do_Ano'] = df_eng['Date'].dt.isocalendar().week.astype(int)

    print("[OK] Novas features de data criadas: Ano, Mes, Dia, Semana_do_Ano.")

    # Vamos remover a coluna 'Date' original, pois já extraímos a informação
    # necessária dela. Manter a data original pode confundir alguns modelos.
    df_eng = df_eng.drop(columns=['Date'])
    print("[OK] Coluna 'Date' original removida.")


    # Verificação Final: Vamos olhar as novas colunas
    print("\n\n--- VERIFICAÇÃO DO DATAFRAME APÓS ENGENHARIA DE FEATURES ---")
    print(df_eng[['Ano', 'Mes', 'Dia', 'Semana_do_Ano']].head())
    print(df_eng.head())

else:
    print("\n❌ ERRO: O dataframe df_final não foi encontrado. Execute os blocos anteriores.")

# ================================================================================================
# Bloco 06: Engenharia de Features - Tratamento de Variáveis Categóricas (One-Hot Encoding)
# ================================================================================================

# Verifica se o dataframe df_eng existe
if 'df_eng' in locals():
    print("\n\n--- TRATANDO VARIÁVEIS CATEGÓRICAS ---")

    # A função pd.get_dummies é a forma mais fácil de aplicar One-Hot Encoding.
    # Ela automaticamente identifica colunas de texto (object) e as converte.
    # O argumento 'columns' especifica quais colunas queremos transformar.
    # 'dtype=int' garante que as novas colunas sejam 0s e 1s inteiros.
    df_processed = pd.get_dummies(df_eng, columns=['Type'], dtype=int)

    print("[OK] Coluna 'Type' convertida para formato numérico via One-Hot Encoding.")


    # Verificação Final: Vamos checar a estrutura final do dataframe
    print("\n\n--- VERIFICAÇÃO FINAL DO DATAFRAME PROCESSADO ---")
    df_processed.info()
    
    print("\n--- 5 Primeiras Linhas mostrando as novas colunas ---")
    # Mostrando apenas as colunas relevantes para a verificação
    print(df_processed[['Store', 'Type_A', 'Type_B', 'Type_C']].head())

else:
    print("\n❌ ERRO: O dataframe df_eng não foi encontrado. Execute os blocos anteriores.")

# ==============================================================================
# Bloco 07: Salvando o Dataframe Processado para a Próxima Etapa
# ==============================================================================

# Importando a biblioteca pathlib para lidar com caminhos de forma robusta
from pathlib import Path

# Verifica se o dataframe df_processed existe
if 'df_processed' in locals():
    
    # Define a pasta de saída
    pasta_saida = Path('data')
    
    # Cria a pasta 'data' se ela não existir (boa prática)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    
    # Constrói o caminho completo do arquivo de forma segura
    caminho_arquivo_saida = pasta_saida / 'walmart_dados_processados.csv'
    
    # Salva o dataframe em um arquivo CSV, sem o índice do pandas
    df_processed.to_csv(caminho_arquivo_saida, index=False)
    
    print(f"\n\n--- ETAPA DE PREPARAÇÃO CONCLUÍDA ---")
    print(f"✅ Dataframe final salvo com sucesso em: {caminho_arquivo_saida}")

else:
    print("\n❌ ERRO: O dataframe df_processed não foi encontrado.")