import pandas as pd

def gerar_auditoria(nome_arquivo_csv, nome_arquivo_txt):
    print(f"Lendo o arquivo {nome_arquivo_csv} para auditoria...")
    
    try:
        # low_memory=False resolve o DtypeWarning
        df = pd.read_csv(nome_arquivo_csv, sep=',', encoding='utf-8', low_memory=False)
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return

    total_linhas = len(df)
    total_colunas = len(df.columns)

    print("Gerando o relatório de raio-x...")

    with open(nome_arquivo_txt, 'w', encoding='utf-8') as f:
        f.write("=========================================================\n")
        f.write("      🔍 RELATÓRIO DE AUDITORIA DE ATRIBUTOS 🔍\n")
        f.write("=========================================================\n")
        f.write(f"Arquivo analisado: {nome_arquivo_csv}\n")
        f.write(f"Total de Instâncias (Linhas): {total_linhas}\n")
        f.write(f"Total de Atributos (Colunas): {total_colunas}\n")
        f.write("=========================================================\n\n")

        for col in df.columns:
            tipo = df[col].dtype
            nulos_qtd = df[col].isnull().sum()
            nulos_perc = (nulos_qtd / total_linhas) * 100
            unicos_qtd = df[col].nunique(dropna=True)
            
            f.write(f"▶ ATRIBUTO: {col}\n")
            f.write(f"  - Tipo de Dado: {tipo}\n")
            f.write(f"  - Nulos: {nulos_qtd} ({nulos_perc:.2f}%)\n")
            f.write(f"  - Total de Valores Únicos: {unicos_qtd}\n")
            
            if unicos_qtd <= 15:
                valores = df[col].dropna().unique()
                # A CORREÇÃO MÁGICA: Converte tudo pra string antes de tentar organizar
                valores_formatados = sorted([str(x) for x in valores.tolist()])
                f.write(f"  - Valores Encontrados: {valores_formatados}\n")
            else:
                top_5 = df[col].value_counts().head(5).index.tolist()
                # Também converte o top 5 pra string só por segurança
                top_5_str = [str(x) for x in top_5]
                f.write(f"  - Amostra (Top 5 mais frequentes): {top_5_str} ...\n")
                
            f.write("-" * 65 + "\n")

    print(f"✅ Auditoria finalizada! Abra o arquivo '{nome_arquivo_txt}' para conferir.")

# Rode no dataset limpo que acabamos de gerar (ou no amostrado, se quiser ver o estrago original)
gerar_auditoria('dataset_modelo1_triagem.csv', 'datasetFinal.txt')