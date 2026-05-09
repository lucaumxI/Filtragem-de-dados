import pandas as pd

print("Carregando o dataset...")

df = pd.read_csv('datasetAmostrado.csv', sep=',', encoding='utf-8')
df.columns = df.columns.str.lower().str.strip()

print(f"Tamanho original: {df.shape[0]} linhas e {df.shape[1]} colunas")

# ====================== COLUNAS PARA EXCLUIR MANUALMENTE ======================
colunas_para_excluir = [
    # 1. Burocracia, Identificadores e Overfitting
    'tp_not', 'nu_ano', 'ano_nasc', 'cs_raca', 'cs_escol_n',
    'sg_uf', 'id_mn_resi', 'id_rg_resi', 'id_pais', 'id_ocupa_n', 
    'uf', 'municipio', 'tpautocto', 'coufinf', 'copaisinf', 'comuninf',
    'id_unidade', 'id_regiona', 'cs_gestant', 'id_agravo', 'sem_not', 'sg_uf_not',
    'id_municip', 'sem_pri',

    # 2. Controle do Sistema
    'dt_invest', 'dt_digita', 'cs_flxret', 'flxrecebi', 'migrado_w', 
    'tp_sistema', 'criterio', 'nu_lote_i', 'nduplic_n', 

    # 3. Exames Laboratoriais (Data Leakage)
    'dt_chik_s1', 'dt_chik_s2', 'res_chiks1', 'res_chiks2', 
    'dt_prnt', 'resul_prnt', 'dt_soro', 'resul_soro', 'dt_ns1', 
    'resul_ns1', 'dt_viral', 'resul_vi_n', 'dt_pcr', 'resul_pcr_', 
    'sorotipo', 'histopa_n', 'imunoh_n', 'clinc_chik',

    # 4. Desfecho do Paciente e Evolução (Data Leakage)
    'hospitaliz', 'dt_interna', 'doenca_tra', 'evolucao', 
    'dt_obito', 'dt_encerra', 'complica', 
    'dt_alrm', 'dt_grav', 

    # 5. Comorbidades
    'diabetes', 'hematolog', 'hepatopat', 'renal', 'hipertensa', 
    'acido_pept', 'auto_imune',

    # 6. Sinais raros / Variância Zero
    'mani_hemor', 'epistaxe', 'gengivo', 'metro', 'petequias', 
    'hematura', 'sangram', 'laco_n', 'plasmatico', 'evidencia', 
    'plaq_menor', 'con_fhd'
]
# =========================================================================

print("\nIniciando limpeza de colunas...")

# 1. Exclusão manual
colunas_faltantes = [col for col in colunas_para_excluir if col not in df.columns]

if colunas_faltantes:
    print(f"⚠️  {len(colunas_faltantes)} colunas da lista manual não foram encontradas.")

df = df.drop(columns=colunas_para_excluir, errors='ignore')

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
    
    df = df.drop(columns=colunas_constantes)
else:
    print("Nenhuma coluna constante encontrada.")

# ====================== SALVAR LOG DE COLUNAS REMANESCENTES ======================
print("\n📝 Salvando log das colunas que SOBRARAM...")

colunas_finais = df.columns.tolist()

with open('colunas_remanescentes.txt', 'w', encoding='utf-8') as f:
    f.write("=== COLUNAS QUE CONTINUAM NO DATASET ===\n\n")
    f.write(f"Total de atributos restantes: {len(colunas_finais)}\n\n")
    
    f.write(f"{'NOME DA COLUNA':<25} | {'TIPO DE DADO'}\n")
    f.write("-" * 45 + "\n")
    
    for col in colunas_finais:
        tipo = str(df[col].dtype)
        f.write(f"{col:<25} | {tipo}\n")

print(f"✅ Log salvo em 'colunas_remanescentes.txt' ({len(colunas_finais)} colunas listadas)")

# =========================================================================

print(f"\nTamanho final do dataset: {df.shape[0]} linhas e {df.shape[1]} colunas")

df.to_csv('dataset_sem_col_irrelevantes.csv', index=False, sep=',', encoding='utf-8')

print("\n🎉 Processo finalizado com sucesso!")