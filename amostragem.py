import pandas as pd
import glob

print("Iniciando a extração da super-amostra aleatória (2021 a 2025)...")

lista_amostras = []
arquivos = glob.glob(r'archive\DENGBR*.csv')
arquivos_filtrados = [f for f in arquivos if any(ano in f for ano in ['21', '22', '23', '24', '25'])]

for arquivo in arquivos_filtrados:
    print(f"Processando: {arquivo}")
    
    # Lista temporária para guardar os pedaços sorteados deste ano específico
    amostras_do_arquivo = []
    
    # Abre o arquivo gigante em pedaços de 100 mil linhas para poupar a RAM
    iterador_lotes = pd.read_csv(arquivo, sep=',', encoding='latin-1', low_memory=False, chunksize=100000)
    
    for lote in iterador_lotes:
        # Pega aleatoriamente 2% das linhas de cada lote (random_state garante reprodutibilidade)
        lote_amostrado = lote.sample(frac=0.1, random_state=42)
        amostras_do_arquivo.append(lote_amostrado)
    
    # Junta todos os pedaços sorteados do ano
    df_ano = pd.concat(amostras_do_arquivo, ignore_index=True)
    
    # Garante que teremos EXATAMENTE 10.000 linhas completamente aleatórias deste ano
    if len(df_ano) > 20000:
        df_ano = df_ano.sample(n=20000, random_state=42)
        
    lista_amostras.append(df_ano)
    print(f"-> Coletadas {len(df_ano)} linhas espalhadas aleatoriamente pelo ano.")

print("\nConcatenando todos os anos...")
df_super = pd.concat(lista_amostras, ignore_index=True)

print("\nSalvando o dataset da super-amostra no disco...")
df_super.to_csv('dataset_amostra_100k.csv', index=False)

print(f"Super-amostra criada! Tamanho total: {df_super.shape[0]} linhas e {df_super.shape[1]} colunas.\n")

print("Gerando os relatórios para o Brainstorm...")

# --- 1. RELATÓRIO DE COLUNAS ---
df_colunas = pd.DataFrame({
    'Porcentagem_Nulos': (df_super.isnull().sum() / len(df_super)) * 100,
    'Valores_Unicos': df_super.nunique(),
    'Tipo_de_Dado': df_super.dtypes
}).reset_index()

df_colunas.rename(columns={'index': 'Nome_da_Coluna'}, inplace=True)
df_colunas.to_csv('Brainstorm_Analise_Colunas.csv', index=False)

# --- 2. RELATÓRIO ESTATÍSTICO ---
with open('Brainstorm_Analise_Estatistica.txt', 'w', encoding='utf-8') as f:
    f.write("========== RELATÓRIO UNIFICADO (AMOSTRA ALEATÓRIA 2021 a 2025) ==========\n")
    f.write(f"Tamanho da Amostra Analisada: {df_super.shape[0]} casos.\n\n")
    
    f.write("========== DISTRIBUIÇÃO DA CLASSIFICAÇÃO FINAL ==========\n")
    coluna_target = 'CLASSI_FIN' if 'CLASSI_FIN' in df_super.columns else 'classi_fin'
    if coluna_target in df_super.columns:
        f.write(df_super[coluna_target].value_counts(dropna=False).to_string())
        
    f.write("\n\n========== RESUMO ESTATÍSTICO ==========\n")
    f.write(df_super.describe().to_string())

print("Pronto! Estatística preservada, RAM salva e arquivos gerados.")