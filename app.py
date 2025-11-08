# ==============================================================================
# app.py
# Versão 3.1: Dashboard Completo com 3 Abas (Lendo online_retail_II.csv)
# ==============================================================================

# 1. Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
# import openpyxl # Não é mais necessário para ler .csv

# ==============================================================================
# Bloco 11: Configuração Inicial
# ==============================================================================
st.set_page_config(page_title="Forecast de Demanda", layout="wide")
st.title("Projeto Integrador III: Forecast de Demanda com IA")
st.write("""
Esta aplicação apresenta os resultados da análise de dados e o modelo de previsão de vendas 
para as lojas da rede Walmart, desenvolvido como parte do Projeto Integrador.
""")

# ==============================================================================
# Bloco 12: Carregamento de Dados e Modelo (com Cache)
# ==============================================================================

@st.cache_data
def carregar_dados_walmart():
    """Carrega os dados processados do Walmart."""
    caminho_dados = Path('data/walmart_dados_processados.csv')
    if caminho_dados.exists():
        df = pd.read_csv(caminho_dados)
        # Adiciona a coluna 'Type_Label' para os gráficos
        def get_type(row):
            if row['Type_A'] == 1: return 'Tipo A'
            if row['Type_B'] == 1: return 'Tipo B'
            if row['Type_C'] == 1: return 'Tipo C'
        df['Type_Label'] = df.apply(get_type, axis=1)
        return df
    else:
        st.error("Arquivo 'walmart_dados_processados.csv' não encontrado na pasta 'data'. Execute o script 01 primeiro.")
        return None

@st.cache_resource
def carregar_modelo_walmart():
    """Carrega o modelo de IA treinado."""
    caminho_modelo = Path('models/random_forest_regressor_v1.joblib')
    if caminho_modelo.exists():
        modelo = joblib.load(caminho_modelo)
        return modelo
    else:
        st.error("Arquivo 'random_forest_regressor_v1.joblib' não encontrado na pasta 'models'. Execute o script 02 primeiro.")
        return None

@st.cache_data
def carregar_dados_uk():
    """Carrega os dados brutos do E-commerce UK a partir do CSV."""
    caminho_dados_uk = Path('data/online_retail_II.csv') # <-- MODIFICADO
    if caminho_dados_uk.exists():
        try:
            # Tenta a leitura com encoding 'latin1', que é comum para este dataset
            df_uk = pd.read_csv(caminho_dados_uk, encoding='latin1') # <-- MODIFICADO
        except Exception as e:
            st.error(f"Erro ao ler 'online_retail_II.csv': {e}")
            return None
        return df_uk
    else:
        st.error("Arquivo 'online_retail_II.csv' não encontrado na pasta 'data'.")
        return None

# --- Executando as funções de carregamento ---
df_walmart = carregar_dados_walmart()
modelo_walmart = carregar_modelo_walmart()
df_uk = carregar_dados_uk()

# ==============================================================================
# Bloco 13: Formulário Interativo (Sidebar)
# ==============================================================================

if df_walmart is not None and modelo_walmart is not None:
    st.sidebar.header("🗓️ Fazer Nova Previsão (Walmart)")

    lojas = sorted(df_walmart['Store'].unique())
    loja_selecionada = st.sidebar.selectbox(
        "Selecione a Loja:", lojas, key='input_loja'
    )

    deptos = sorted(df_walmart['Dept'].unique())
    depto_selecionado = st.sidebar.selectbox(
        "Selecione o Departamento:", deptos, key='input_depto'
    )

    data_selecionada = st.sidebar.date_input(
        "Selecione a Data:", key='input_data'
    )

    temp_selecionada = st.sidebar.number_input(
        "Temperatura Média (em Fahrenheit):", value=70.0, key='input_temp'
    )
    feriado_selecionado = st.sidebar.selectbox(
        "É feriado?", [False, True], key='input_feriado'
    )
    
    botao_prever = st.sidebar.button("Gerar Previsão", key='btn_prever')

# ==============================================================================
# Bloco 14 & 15: Conteúdo Principal com 3 Abas
# ==============================================================================

if df_walmart is not None and modelo_walmart is not None:
    
    tab1, tab2, tab3 = st.tabs([
        "📊 Análise Walmart", 
        "🤖 Simulador de Previsão", 
        "🌍 Comparativo E-commerce"
    ])

    # 2. Conteúdo da Aba 1: Análise Walmart
    with tab1:
        st.header("Visão Geral dos Dados Históricos (Walmart)")
        st.write("Abaixo está uma amostra dos dados que foram usados para treinar o modelo de IA.")
        st.dataframe(df_walmart.sample(10))
        st.success("Dados do Walmart e modelo carregados com sucesso!")
        st.divider()

        st.header("Análise de Vendas (Walmart)")
        
        st.subheader("Vendas Totais por Mês")
        vendas_por_mes_wm = df_walmart.groupby('Mes')['Weekly_Sales'].sum()
        st.line_chart(vendas_por_mes_wm)
        st.write("Podemos observar claramente a sazonalidade das vendas, com picos no final do ano (Novembro e Dezembro).")

        st.subheader("Vendas Totais por Tipo de Loja")
        vendas_por_tipo_wm = df_walmart.groupby('Type_Label')['Weekly_Sales'].sum()
        st.bar_chart(vendas_por_tipo_wm)
        st.write("As lojas do 'Tipo A' (supercentros) dominam vastamente o volume de vendas.")

    # 3. Conteúdo da Aba 2: Simulador de Previsão
    with tab2:
        st.header("Resultado da Previsão")
        st.write("Utilize o formulário na barra lateral esquerda para gerar uma nova previsão de vendas.")
        
        if botao_prever:
            ano = data_selecionada.year
            mes = data_selecionada.month
            dia = data_selecionada.day
            semana_do_ano = data_selecionada.isocalendar().week

            dados_loja = df_walmart[df_walmart['Store'] == loja_selecionada].iloc[-1]
            
            features_para_prever = {
                'Store': loja_selecionada, 'Dept': depto_selecionado, 'IsHoliday': feriado_selecionado,
                'Temperature': temp_selecionada, 'Ano': ano, 'Mes': mes, 'Dia': dia,
                'Semana_do_Ano': semana_do_ano, 'Size': dados_loja['Size'], 'Fuel_Price': dados_loja['Fuel_Price'],
                'MarkDown1': dados_loja['MarkDown1'], 'MarkDown2': dados_loja['MarkDown2'],
                'MarkDown3': dados_loja['MarkDown3'], 'MarkDown4': dados_loja['MarkDown4'],
                'MarkDown5': dados_loja['MarkDown5'], 'CPI': dados_loja['CPI'],
                'Unemployment': dados_loja['Unemployment'], 'Type_A': dados_loja['Type_A'],
                'Type_B': dados_loja['Type_B'], 'Type_C': dados_loja['Type_C']
            }
            
            df_previsao = pd.DataFrame([features_para_prever])
            colunas_modelo = modelo_walmart.feature_names_in_
            df_previsao = df_previsao[colunas_modelo]
            
            previsao_vendas = modelo_walmart.predict(df_previsao)[0]
            
            st.metric(
                label=f"Vendas Semanais para a Loja {loja_selecionada}, Dept {depto_selecionado}",
                value=f"$ {previsao_vendas:,.2f}"
            )
            
            with st.expander("Ver detalhes dos dados usados na previsão"):
                st.dataframe(df_previsao)
        else:
            st.info("Por favor, preencha os dados na barra lateral e clique em 'Gerar Previsão'.")

    # 4. Conteúdo da Aba 3: Comparativo E-commerce
    with tab3:
        st.header("Análise Comparativa: Varejo Físico vs. E-commerce (UK)")
        
        if df_uk is not None:
            st.write("Amostra dos dados brutos do E-commerce UK:")
            st.dataframe(df_uk.sample(10))
            
            # --- Limpeza e Preparação dos dados UK (on-the-fly) ---
            df_uk_limpo = df_uk.copy()
            df_uk_limpo['InvoiceDate'] = pd.to_datetime(df_uk_limpo['InvoiceDate'], errors='coerce')
            df_uk_limpo = df_uk_limpo.dropna(subset=['InvoiceDate'])
            
            # Filtra transações inválidas
            df_uk_limpo = df_uk_limpo[df_uk_limpo['Quantity'] > 0]
            df_uk_limpo = df_uk_limpo[df_uk_limpo['Price'] > 0] # <-- MODIFICADO
            
            # Cria novas colunas
            df_uk_limpo['TotalPrice'] = df_uk_limpo['Quantity'] * df_uk_limpo['Price'] # <-- MODIFICADO
            df_uk_limpo['Mes'] = df_uk_limpo['InvoiceDate'].dt.month
            
            st.divider()
            st.header("Análises Comparativas")

            st.subheader("Vendas Totais por Mês (E-commerce UK)")
            vendas_mes_uk = df_uk_limpo.groupby('Mes')['TotalPrice'].sum()
            st.line_chart(vendas_mes_uk)
            st.write("""
            **Observação Comparativa:** Assim como no Walmart, o E-commerce apresenta um pico 
            massivo de vendas no final do ano (Novembro e Dezembro), preparando-se para o Natal. 
            A queda em Janeiro também é muito acentuada.
            """)

            st.subheader("Top 10 Países por Volume de Vendas (E-commerce UK)")
            vendas_pais_uk = df_uk_limpo.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)
            st.bar_chart(vendas_pais_uk.head(10))
            st.write("Como esperado, o Reino Unido ('United Kingdom') domina as vendas, mas há uma presença significativa de outros países europeus.")
            
        else:
            st.error("Não foi possível carregar os dados do E-commerce. Verifique o arquivo 'data/online_retail_II.csv'.") # <-- MODIFICADO

else:
    st.error("Aplicação não pode ser iniciada. Verifique os arquivos de dados e modelo do Walmart.")