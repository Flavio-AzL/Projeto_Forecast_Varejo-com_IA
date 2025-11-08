# ==============================================================================
# 02_TREINAMENTO_MODELO.PY
# Bloco 08: Preparação para Modelagem e Treinamento do Primeiro Modelo
# ==============================================================================

# 1. Importando as bibliotecas necessárias
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

print("--- Iniciando o script de treinamento de modelo ---")

# 2. Carregando os dados processados
caminho_dados = Path('data/walmart_dados_processados.csv')
if caminho_dados.exists():
    df = pd.read_csv(caminho_dados)
    print("✅ Dados processados carregados com sucesso!")
    print(f"   - Shape do dataframe: {df.shape}")
else:
    print(f"❌ ERRO: O arquivo {caminho_dados} não foi encontrado.")
    print("   - Por favor, execute o script 01_preparacao_dados.py primeiro.")
    exit()

# 3. Separando Features (X) e Target (y)
# Target (y) é a coluna que queremos prever: 'Weekly_Sales'
y = df['Weekly_Sales']

# Features (X) são todas as outras colunas que usaremos para fazer a previsão
# Usamos .drop() para remover a coluna target e criar nosso dataframe de features
X = df.drop('Weekly_Sales', axis=1)

print(f"\n[INFO] Features (X) shape: {X.shape}")
print(f"[INFO] Target (y) shape: {y.shape}")


# 4. Dividindo os dados em conjuntos de Treino e Teste
# 80% dos dados para treino, 20% para teste.
# random_state=42 garante que a divisão seja sempre a mesma, para reprodutibilidade.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n[INFO] Dados divididos em conjuntos de treino e teste:")
print(f"   - X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"   - X_test: {X_test.shape},  y_test: {y_test.shape}")


# 5. Treinando o modelo de Machine Learning (Random Forest)
# ==============================================================================
# Bloco 16: Criando um Modelo Otimizado para Deploy (Balanço de Tamanho/Performance)
# ==============================================================================
print("\n--- Treinando o modelo OTIMIZADO PARA DEPLOY (leve) ---")
modelo = RandomForestRegressor(
    n_estimators=50,     # Metade das árvores padrão
    max_depth=20,        # Limite de profundidade (evita ficheiros gigantes)
    min_samples_leaf=5,  # Ajuda a podar e a generalizar
    n_jobs=-1, 
    random_state=42
)

# O comando .fit() é onde a "mágica" acontece: o modelo aprende com os dados de treino
modelo.fit(X_train, y_train)
print("✅ Modelo treinado com sucesso!")


# 6. Fazendo previsões no conjunto de teste
print("\n--- Fazendo previsões no conjunto de teste ---")
y_pred = modelo.predict(X_test)


# 7. Avaliando a performance do modelo
print("\n--- Avaliação da Performance do Modelo ---")
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
print(f"Mean Squared Error (MSE): ${mse:,.2f}")
print(f"R-squared (R²): {r2:.2%}")

# ==============================================================================
# Bloco 09: Análise de Importância das Features
# ==============================================================================

# Importando a biblioteca para visualização
import matplotlib.pyplot as plt
import seaborn as sns

# Verifica se o modelo foi treinado
if 'modelo' in locals() and 'X_train' in locals():
    print("\n\n--- ANALISANDO A IMPORTÂNCIA DAS FEATURES ---")

    # O modelo Random Forest já calcula a importância de cada feature durante o treino
    importancias = modelo.feature_importances_
    
    # Criando um DataFrame para visualizar melhor
    df_importancias = pd.DataFrame({
        'Feature': X_train.columns,
        'Importancia': importancias
    }).sort_values(by='Importancia', ascending=False) # Ordena da mais importante para a menos

    print("\nTop 10 Features mais importantes para o modelo:")
    print(df_importancias.head(10))

    # Criando um gráfico de barras para visualizar
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importancia', y='Feature', data=df_importancias.head(15), palette='viridis')
    plt.title('Top 15 Features Mais Importantes para a Previsão de Vendas')
    plt.xlabel('Importância Relativa')
    plt.ylabel('Feature')
    plt.tight_layout() # Ajusta o layout para não cortar os nomes
    plt.show()

else:
    print("\n❌ ERRO: O modelo ainda não foi treinado. Execute o Bloco 08 primeiro.")


# ==============================================================================
# Bloco 10: Salvando o Modelo Treinado (Persistência)
# ==============================================================================
import joblib

# Verifica se o modelo foi treinado
if 'modelo' in locals():
    print("\n\n--- SALVANDO O MODELO TREINADO ---")
    
    # Criando a pasta 'models' se ela não existir
    caminho_pasta_modelos = Path('models')
    caminho_pasta_modelos.mkdir(exist_ok=True)
    
    # Definindo o caminho completo para salvar o modelo
    caminho_modelo = caminho_pasta_modelos / 'random_forest_regressor_v1.joblib'
    
    # Usando joblib para salvar o objeto do modelo no arquivo
    joblib.dump(modelo, caminho_modelo)
    
    print(f"✅ Modelo salvo com sucesso em: {caminho_modelo}")

else:
    print("\n❌ ERRO: O modelo ainda não foi treinado.")