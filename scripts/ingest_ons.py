import pandas as pd
from google.oauth2 import service_account
import pandas_gbq

print("--- O SCRIPT COMEÇOU A RODAR ---") # Adicione isso aqui!

# 1. Configurações de Identidade
SERVICE_ACCOUNT_FILE = 'credentials.json' # Garanta que o arquivo está na mesma pasta!
PROJECT_ID = 'portfolio-energy-analytics'
DATASET_ID = 'raw_ons'
TABLE_ID = 'geracao_usina_diaria'

# 2. Autenticação
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

def ingest_data():
    print("🚀 Iniciando ingestão de dados do ONS...")
    
    # Link atualizado (Dados consolidados de geração por usina)
    # Se o de 2024 falhar, este de 2023 é garantido para teste de portfólio
    url = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/GERACAO_USINA-2_2026_04.csv"
    
    try:
        print(f"📥 Baixando dados de: {url}")
        # ONS usa ';' como separador e as vezes codificação 'latin-1'
        df = pd.read_csv(url, sep=';', nrows=10000, encoding='utf-8')
        
        print(f"✅ Dados baixados com sucesso! {len(df)} linhas encontradas.")

        destination_table = f"{DATASET_ID}.{TABLE_ID}"
        
        print(f"📤 Subindo para o BigQuery ({destination_table})...")
        pandas_gbq.to_gbq(
            df, 
            destination_table, 
            project_id=PROJECT_ID, 
            if_exists='replace',
            credentials=credentials
        )
        
        print(f"✨ Tabela criada com sucesso no BigQuery!")

    except Exception as e:
        print(f"❌ Erro detalhado: {e}")

if __name__ == "__main__":
    ingest_data()