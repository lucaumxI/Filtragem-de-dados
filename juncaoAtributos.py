import pandas as pd

print("Carregando o dataset...")

df = pd.read_csv('dataset_sem_col_irrelevantes.csv', sep=',', encoding='utf-8')
df.columns = df.columns.str.lower().str.strip()

# 1. Removendo os nulos totais da coluna alvo (os em branco '')
df = df.dropna(subset=['classi_fin'])

# 2. Convertendo a coluna para número (caso o Pandas tenha lido como texto por causa dos espaços)
# errors='coerce' transforma qualquer lixo irrecuperável em NaN para podermos limpar depois
df['classi_fin'] = pd.to_numeric(df['classi_fin'], errors='coerce')

# 3. A Peneira da Certeza: Mantendo apenas Confirmados e Descartados
# NOTA: Adapte os números abaixo para bater com o DICIONÁRIO EXATO que você está usando
# Pelo seu print atual: 1 = Confirmado, 2 = Descartado
valores_aceitos = [1, 2] 
df = df[df['classi_fin'].isin(valores_aceitos)]

# 4. Transformando pro Modelo 1 (Binário clássico: 0 e 1)
# Onde era 2 (Descartado), vira 0. Onde era 1 (Confirmado), continua 1.
df['target_modelo_1'] = df['classi_fin'].replace(2, 0)

print("\n--- CONTAGEM DE CLASSES NO ALVO (classi_fin) ---")
# Mostra quantos pacientes sobraram em cada categoria
print(df['classi_fin'].value_counts(dropna=False))

print(f"\nTotal de linhas sobreviventes: {df.shape[0]}")