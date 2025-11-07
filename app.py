# 1. Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ==============================================================================
# Bloco 11: Configuração Inicial
# ==============================================================================

# 2. Configurando o título da página
st.set_page_config(page_title="Forecast de Demanda", layout="wide")

# 3. Adicionando um Título Principal à página
st.title("Projeto Integrador III: Forecast de Demanda com IA")

# 4. Adicionando um subtítulo ou texto de introdução
st.write("""
Esta aplicação apresenta os resultados da análise de dados e o modelo de previsão de vendas 
para as lojas da rede Walmart, desenvolvido como parte do Projeto Integrador.
""")

# ==============================================================================
# Bloco 12: Carregamento de Dados e Modelo (com Cache)
# ==============================================================================

# 4. Criando funções de carregamento com cache
@st.cache_data
def carregar_dados():
    caminho_dados = Path('data/walmart_dados_processados.csv')
    if caminho_dados.exists():
        df = pd.read_csv(caminho_dados)
        return df
    else:
        st.error("Arquivo de dados processados não encontrado. Execute o script 01 primeiro.")
        return None

@st.cache_resource
def carregar_modelo():
    caminho_modelo = Path('models/random_forest_regressor_v1.joblib')
    if caminho_modelo.exists():
        modelo = joblib.load(caminho_modelo)
        return modelo
    else:
        st.error("Arquivo do modelo não encontrado. Execute o script 02 primeiro.")
        return None

# 5. Executando as funções de carregamento
df = carregar_dados()
modelo = carregar_modelo()

# ==============================================================================
# Início da Lógica Principal da Aplicação
# ==============================================================================

# 6. Verificação e exibição de dados
if df is not None and modelo is not None:
    
    # Esta é a parte de exibição do Bloco 12
    st.header("Análise Exploratória dos Dados Processados")
    st.write("Abaixo está uma amostra dos dados que foram usados para treinar o modelo de IA.")
    st.dataframe(df.sample(5)) # Mostra 5 linhas aleatórias
    st.success("Dados e modelo carregados com sucesso! Aplicação pronta.")

    # ==============================================================================
    # Bloco 13: Formulário Interativo para Previsão (Versão Corrigida com 'key')
    # ==============================================================================

    st.sidebar.header("🗓️ Fazer Nova Previsão")

    # Criando os inputs na sidebar
    
    # 1. Input para Loja (Store)
    lojas = sorted(df['Store'].unique())
    loja_selecionada = st.sidebar.selectbox(
        "Selecione a Loja:", 
        lojas, 
        key='input_loja'  # <--- CHAVE ÚNICA
    )

    # 2. Input para Departamento (Dept)
    deptos = sorted(df['Dept'].unique())
    depto_selecionado = st.sidebar.selectbox(
        "Selecione o Departamento:", 
        deptos, 
        key='input_depto' # <--- CHAVE ÚNICA
    )

    # 3. Input para a Data
    data_selecionada = st.sidebar.date_input(
        "Selecione a Data:", 
        key='input_data'  # <--- CHAVE ÚNICA
    )

    # 4. Inputs para dados externos
    temp_selecionada = st.sidebar.number_input(
        "Temperatura Média (em Fahrenheit):", 
        value=70.0, 
        key='input_temp'  # <--- CHAVE ÚNICA
    )
    feriado_selecionado = st.sidebar.selectbox(
        "É feriado?", 
        [False, True], 
        key='input_feriado' # <--- CHAVE ÚNICA
    )

    # 5. Botão para disparar a previsão
    if st.sidebar.button("Gerar Previsão", key='btn_prever'): # <--- CHAVE ÚNICA
        
        # --- PREPARAÇÃO DOS DADOS PARA O MODELO ---
        
        # 1. Extrair features da data selecionada
        ano = data_selecionada.year
        mes = data_selecionada.month
        dia = data_selecionada.day
        semana_do_ano = data_selecionada.isocalendar().week

        # 2. Buscar dados de referência da loja (Size, Type, CPI, etc.)
        dados_loja = df[df['Store'] == loja_selecionada].iloc[-1]
        
        # 3. Criar o DataFrame de 1 linha para o modelo
        features_para_prever = {
            'Store': loja_selecionada,
            'Dept': depto_selecionado,
            'IsHoliday': feriado_selecionado,
            'Temperature': temp_selecionada,
            'Ano': ano,
            'Mes': mes,
            'Dia': dia,
            'Semana_do_Ano': semana_do_ano,
            'Size': dados_loja['Size'],
            'Fuel_Price': dados_loja['Fuel_Price'],
            'MarkDown1': dados_loja['MarkDown1'],
            'MarkDown2': dados_loja['MarkDown2'],
            'MarkDown3': dados_loja['MarkDown3'],
            'MarkDown4': dados_loja['MarkDown4'],
            'MarkDown5': dados_loja['MarkDown5'],
            'CPI': dados_loja['CPI'],
            'Unemployment': dados_loja['Unemployment'],
            'Type_A': dados_loja['Type_A'],
            'Type_B': dados_loja['Type_B'],
            'Type_C': dados_loja['Type_C']
        }
        
        df_previsao = pd.DataFrame([features_para_prever])
        
        # Garantir a ordem exata das colunas (O MODELO EXIGE ISSO)
        colunas_modelo = modelo.feature_names_in_
        df_previsao = df_previsao[colunas_modelo]
        
        # --- Fazer a Previsão ---
        previsao_vendas = modelo.predict(df_previsao)[0]
        
        # --- Exibir o Resultado ---
        st.header(f"📈 Previsão de Vendas")
        st.metric(
            label=f"Vendas Semanais para a Loja {loja_selecionada}, Dept {depto_selecionado}",
            value=f"$ {previsao_vendas:,.2f}"
        )
        
        with st.expander("Ver detalhes da previsão"):
            st.dataframe(df_previsao)

else:
    # Este 'else' garante que o app pare se os arquivos não forem carregados
    st.error("Aplicação não pode ser iniciada. Verifique os arquivos de dados e modelo.")