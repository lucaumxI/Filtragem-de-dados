import pandas as pd

print("Carregando o dataset...")

df = pd.read_csv('datasetAmostrado.csv', sep=',', encoding='utf-8')
df.columns = df.columns.str.lower().str.strip()

print(f"Tamanho original: {df.shape[0]} linhas e {df.shape[1]} colunas")

# ====================== COLUNAS PARA EXCLUIR MANUALMENTE ======================
colunas_para_excluir = [
    # 1. Burocracia e Identificadores
    'tp_not', 'id_agravo', 'nu_ano', 'ano_nasc', 'cs_raca', 
    'sg_uf', 'id_mn_resi', 'id_rg_resi', 'id_pais', 'id_ocupa_n', 
    'uf', 'municipio', 'tpautocto', 'coufinf', 'copaisinf', 'comuninf',

    # 2. Controle do Sistema
    'dt_invest', 'dt_digita', 'cs_flxret', 'flxrecebi', 'migrado_w', 
    'tp_sistema', 'criterio',

    # 3. Exames Laboratoriais (Data Leakage)
    'dt_chik_s1', 'dt_chik_s2', 'res_chiks1', 'res_chiks2', 
    'dt_prnt', 'resul_prnt', 'dt_soro', 'resul_soro', 'dt_ns1', 
    'resul_ns1', 'dt_viral', 'resul_vi_n', 'dt_pcr', 'resul_pcr_', 
    'sorotipo', 'histopa_n', 'imunoh_n', 'clinc_chik',

    # 4. Desfecho do Paciente
    'hospitaliz', 'dt_interna', 'doenca_tra', 'evolucao', 
    'dt_obito', 'dt_encerra', 'complica',

    # 5. Comorbidades
    'diabetes', 'hematolog', 'hepatopat', 'renal', 'hipertensa', 
    'acido_pept', 'auto_imune',

    # 6. Sinais raros / quase nulos
    'mani_hemor', 'epistaxe', 'gengivo', 'metro', 'petequias', 
    'hematura', 'sangram', 'laco_n', 'plasmatico', 'evidencia', 
    'plaq_menor', 'con_fhd'
]
# =========================================================================

# Lista para registrar todas as colunas excluídas
colunas_excluidas = []

print("\nIniciando limpeza de colunas...")

# 1. Exclusão manual
colunas_faltantes = [col for col in colunas_para_excluir if col not in df.columns]

if colunas_faltantes:
    print(f"⚠️  {len(colunas_faltantes)} colunas da lista manual não foram encontradas.")

df = df.drop(columns=colunas_para_excluir, errors='ignore')

# Registrar as colunas excluídas manualmente
for col in colunas_para_excluir:
    if col in df.columns:   # se ainda estava presente antes do drop
        colunas_excluidas.append((col, "Exclusão manual (irrelevante / leakage / desfecho)"))

print(f"Tamanho após exclusão manual: {df.shape[0]} linhas e {df.shape[1]} colunas")

# 2. Remover colunas constantes (apenas 1 valor único)
print("\n🔍 Verificando colunas constantes (1 único valor)...")

n_unicos = df.nunique()
colunas_constantes = n_unicos[n_unicos == 1].index.tolist()

if colunas_constantes:
    print(f"✅ Encontradas {len(colunas_constantes)} colunas constantes:")
    for col in colunas_constantes:
        valor = df[col].iloc[0]
        print(f" → {col} (valor: {valor})")
        colunas_excluidas.append((col, f"Coluna constante (único valor = {valor})"))
    
    df = df.drop(columns=colunas_constantes)
else:
    print("Nenhuma coluna constante encontrada.")

# ====================== SALVAR LOG DE COLUNAS EXCLUÍDAS ======================
print("\n📝 Salvando log de colunas excluídas...")

with open('colunas_excluidas.txt', 'w', encoding='utf-8') as f:
    f.write("=== COLUNAS EXCLUÍDAS DO DATASET ===\n\n")
    f.write(f"Total de colunas removidas: {len(colunas_excluidas)}\n\n")
    
    for col, motivo in colunas_excluidas:
        f.write(f"{col:40} | {motivo}\n")

print(f"✅ Log salvo em 'colunas_excluidas.txt' ({len(colunas_excluidas)} colunas registradas)")

# =========================================================================

print(f"\nTamanho final do dataset: {df.shape[0]} linhas e {df.shape[1]} colunas")

df.to_csv('dataset_sem_col_irrelevantes.csv', index=False, sep=',', encoding='utf-8')

print("\n🎉 Processo finalizado com sucesso!")