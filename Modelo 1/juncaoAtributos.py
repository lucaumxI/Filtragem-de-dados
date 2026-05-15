import pandas as pd
import numpy as np

# =====================================================================
# FUNÇÕES AUXILIARES
# =====================================================================
def converter_idade_sinan(codigo):  # A idade vem no formato num formato de 4 digitos, sendo o primeiro referente a unidade de medida (dias, meses ou anos) e o restante a quantidade em si
    """Converte o código composto de idade do SINAN para anos inteiros."""
    codigo_str = str(codigo).split('.')[0]  # Caso o numero inteiro tenha vindo como decimal, o .split corta o ponto tornando inteiro
    
    if len(codigo_str) < 4 or codigo_str == 'nan':  # Se tiver menos de 4 digitos ou fou um NaN retorna NaN
        return np.nan
        
    unidade = codigo_str[0]     # Salva a unidade
    valor = int(codigo_str[1:]) # Pega o restante para ser o valor
    
    if unidade == '4':          # Código 4 = anos
        return valor            # Retorna o próprio valor
    elif unidade in ['1', '2', '3']:
        return 0                # Horas, Dias ou Meses viram 0 anos
    elif unidade == '5':        # Código 5 a pessoa tem mais de 100 anos e a idade real é valor + 100
        return valor + 100
    else:
        return np.nan

# =====================================================================
# FASE 1: CARREGAMENTO E PADRONIZAÇÃO BÁSICA
# =====================================================================
print("Carregando o dataset...")
df = pd.read_csv('dataset_sem_col_irrelevantes.csv', sep=',', encoding='utf-8') 
df.columns = df.columns.str.lower().str.strip()

print(f"Tamanho inicial: {df.shape[0]} linhas e {df.shape[1]} colunas")

# =====================================================================
# FASE 2: DEFINIÇÃO DO ALVO (TARGET) DO MODELO 1 CORRIGIDA
# =====================================================================
print("\nProcessando a variável alvo...")

# Força conversão para número
df['classi_fin'] = pd.to_numeric(df['classi_fin'], errors='coerce') # classi_fin (classe alvo) é forçada a ser um número

# Mantém apenas as linhas que são Confirmadas (10 a 13) ou Descartadas (5)
codigos_validos = [10, 11, 12, 13, 5]   # Códigos 10, 11, 12, 13 e 5 são os códigos válidos
df = df[df['classi_fin'].isin(codigos_validos)].copy()  # .isin verifica se os valores de codigos_validos estão em (is in). O termo dentro do colchetes cria uma máscara booleana usando o .isin

# Cria o alvo binário: 
# Transforma o 5 (Descartado) em 0
df['arbovirose'] = df['classi_fin'].replace(5, 0)

# Transforma todos os outros códigos válidos (10, 11, 12, 13) em 1 (Tem Arbovirose)
df['arbovirose'] = df['arbovirose'].replace([10, 11, 12, 13], 1)

# Joga a coluna antiga fora
df = df.drop(columns=['classi_fin'])

print("--- DISTRIBUIÇÃO DA COLUNA ARBOVIROSE (ALVO) ---")
print(df['arbovirose'].value_counts(dropna=False))
# =====================================================================
# FASE 3: ENGENHARIA DE ATRIBUTOS - DEMOGRAFIA
# =====================================================================
print("\nProcessando demografia (Idade e Gênero)...")

# Idade
df['idade_anos'] = df['nu_idade_n'].apply(converter_idade_sinan)
df = df.dropna(subset=['idade_anos'])
df = df.drop(columns=['nu_idade_n'])

# Gênero (1 = Feminino, 0 = Masculino)
df['cs_sexo'] = df['cs_sexo'].astype(str).str.upper().str.strip()
df = df[df['cs_sexo'].isin(['F', 'M'])]
df['is_feminino'] = df['cs_sexo'].map({'F': 1, 'M': 0})
df = df.drop(columns=['cs_sexo'])

# =====================================================================
# FASE 4: ENGENHARIA DE ATRIBUTOS - TEMPORAL (SAZONALIDADE E EVOLUÇÃO)
# =====================================================================
print("\nProcessando atributos temporais...")

# Converte texto para data
df['dt_sin_pri'] = pd.to_datetime(df['dt_sin_pri'], errors='coerce')
df['dt_notific'] = pd.to_datetime(df['dt_notific'], errors='coerce')
df = df.dropna(subset=['dt_sin_pri', 'dt_notific'])

# Cria features matemáticas
df['mes_sintomas'] = df['dt_sin_pri'].dt.month
df['dias_para_notificacao'] = (df['dt_notific'] - df['dt_sin_pri']).dt.days

# Filtro de sanidade e limpeza
df = df[df['dias_para_notificacao'] >= 0]
df = df.drop(columns=['dt_sin_pri', 'dt_notific', 'sem_not', 'sem_pri'], errors='ignore')

# =====================================================================
# FASE 5: ENGENHARIA DE ATRIBUTOS - QUADRO CLÍNICO
# =====================================================================
print("\nBinarizando sintomas clínicos base...")

sintomas = [
    'febre', 'mialgia', 'cefaleia', 'exantema', 'vomito', 'nausea', 
    'dor_costas', 'conjuntvit', 'artrite', 'artralgia', 'petequia_n', 
    'leucopenia', 'laco', 'dor_retro'
]

# Binarização: 1 = Sim, 0 = Não (Ignorados e nulos assumidos como 0)
for col in sintomas:
    if col in df.columns:
        df[col] = df[col].replace([2, 3, 8, 9], 0)
        df[col] = df[col].fillna(0).astype(int)

# =====================================================================
# FASE 6: ENGENHARIA DE ATRIBUTOS - SINAIS DE ALARME E GRAVIDADE
# =====================================================================
print("Consolidando Sinais de Alarme e Gravidade...")

colunas_alarme = [
    'alrm_hipot', 'alrm_plaq', 'alrm_vom', 'alrm_sang', 'alrm_hemat', 
    'alrm_abdom', 'alrm_letar', 'alrm_hepat', 'alrm_liq'
]

colunas_gravidade = [
    'grav_pulso', 'grav_conv', 'grav_ench', 'grav_insuf', 'grav_taqui', 
    'grav_extre', 'grav_hipot', 'grav_hemat', 'grav_melen', 'grav_metro', 
    'grav_sang', 'grav_ast', 'grav_mioc', 'grav_consc', 'grav_orgao'
]

colunas_alarme = [col for col in colunas_alarme if col in df.columns]
colunas_gravidade = [col for col in colunas_gravidade if col in df.columns]

# Limpa valores antes da soma
for col in colunas_alarme + colunas_gravidade:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df[col] = df[col].replace([2, 3, 8, 9], 0)

# Fusão: Se a soma for > 0, teve pelo menos um sinal
df['teve_sinal_alarme'] = (df[colunas_alarme].sum(axis=1) > 0).astype(int)
df['teve_sinal_gravidade'] = (df[colunas_gravidade].sum(axis=1) > 0).astype(int)

# Remove as 24 colunas originais
df = df.drop(columns=colunas_alarme + colunas_gravidade)

# =====================================================================
# FASE 7: EXPORTAÇÃO
# =====================================================================
print("\n=========================================================")
print(f"Processamento concluído. Tamanho final: {df.shape[0]} linhas e {df.shape[1]} colunas.")
print("=========================================================\n")

df.to_csv('dataset_modelo1_triagem.csv', index=False, sep=',', encoding='utf-8')
print("Dataset do Modelo 1 salvo como 'dataset_modelo1_triagem.csv'.")