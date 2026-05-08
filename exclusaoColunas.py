import pandas as pd


print("Carregando o dataset...")

df = pd.read_csv('datasetAmostrado.csv', sep=',', encoding='utf-8')
df.columns = df.columns.str.lower().str.strip()

print(f"Tamanho original: {df.shape[0]} linhas e {df.shape[1]} colunas")

colunas_para_excluir = [
    # 1. Burocracia, Identificadores e Localidades Redundantes
    'tp_not', 'id_agravo', 'nu_ano', 'ano_nasc', 'cs_raca', 
    'sg_uf', 'id_mn_resi', 'id_rg_resi', 'id_pais', 'id_ocupa_n', 
    'uf', 'municipio', 'tpautocto', 'coufinf', 'copaisinf', 'comuninf',

    # 2. Controle do Sistema (Não agregam valor clínico)
    'dt_invest', 'dt_digita', 'cs_flxret', 'flxrecebi', 'migrado_w', 
    'tp_sistema', 'criterio',

    # 3. Exames Laboratoriais (Risco de Data Leakage)
    'dt_chik_s1', 'dt_chik_s2', 'res_chiks1', 'res_chiks2', 
    'dt_prnt', 'resul_prnt', 'dt_soro', 'resul_soro', 'dt_ns1', 
    'resul_ns1', 'dt_viral', 'resul_vi_n', 'dt_pcr', 'resul_pcr_', 
    'sorotipo', 'histopa_n', 'imunoh_n', 'clinc_chik',

    # 4. Desfecho do Paciente (Ocorre depois do diagnóstico)
    'hospitaliz', 'dt_interna', 'doenca_tra', 'evolucao', 
    'dt_obito', 'dt_encerra', 'complica',

    # 5. Comorbidades Pré-existentes (Prognóstico, não Diagnóstico)
    'diabetes', 'hematolog', 'hepatopat', 'renal', 'hipertensa', 
    'acido_pept', 'auto_imune',

    # 6. Hemorragias e Sinais Raros (Variância Zero / 100% Nulos)
    'mani_hemor', 'epistaxe', 'gengivo', 'metro', 'petequias', 
    'hematura', 'sangram', 'laco_n', 'plasmatico', 'evidencia', 
    'plaq_menor', 'con_fhd'
]

print("\nLimpando colunas irrelevantes...")

# --- MÓDULO DE DETETIVE ---
# Verifica quais colunas da sua lista não existem no dataset
colunas_faltantes = [coluna for coluna in colunas_para_excluir if coluna not in df.columns]

if len(colunas_faltantes) > 0:
    print(f"\n⚠️ ALERTA: {len(colunas_faltantes)} colunas da sua lista não existem neste CSV:")
    for col in colunas_faltantes:
        print(f" -> {col}")
    print("O script vai ignorá-las e continuar...\n")
else:
    print("\n✅ Sucesso: Todas as colunas da sua lista negra foram encontradas no dataset!\n")
# -------------------------

# Aqui vem o drop que já estava no seu código
df = df.drop(columns=colunas_para_excluir, errors='ignore')

# Se existirem colunas na lista que por acaso não estão no CSV (para evitar erro no código), 
# você pode usar esse parâmetro de segurança:
# df = df.drop(columns=colunas_para_excluir, errors='ignore')

print(f"Tamanho após limpeza: {df.shape[0]} linhas e {df.shape[1]} colunas")

# Salva o resultado em um novo arquivo
# index=False evita que o Pandas crie uma coluna extra com os números das linhas
df.to_csv('dataset_sem_col_irrelevantes.csv', index=False, sep=',', encoding='utf-8')

print("Dataset salvo com sucesso como 'dataset_processado_v1.csv'")