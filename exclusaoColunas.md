# Documentação: Pré-Processamento - Etapa 1 (Limpeza e Exclusão)

**Arquivo Relacionado:** `exclusaoColunas.py`
**Objetivo:** Reduzir a dimensionalidade do dataset do SINAN, removendo atributos que introduzem ruído, viés ou vazamento de dados no treinamento dos modelos.

## Resumo da Execução
* **Entrada:** Dataset amostrado com 121 atributos e 100.000 instâncias.
* **Saída:** Dataset limpo com 55 atributos.
* **Total Excluído:** 66 colunas descartadas por falta de relevância preditiva ou clínica.

---

## Justificativas de Exclusão

Para garantir a capacidade de generalização do algoritmo, os atributos descartados foram agrupados nas seguintes categorias lógicas:

### 1. Prevenção de Vazamento de Dados (*Data Leakage*)
O objetivo do nosso modelo (especialmente o Modelo 1 - Triagem) é prever a doença no momento em que o paciente chega ao posto com sintomas. Portanto, o algoritmo **não pode** ter acesso a informações que só existiriam dias ou semanas após o atendimento inicial.
* **Exames Laboratoriais:** `dt_chik_s1`, `dt_chik_s2`, `res_chiks1`, `res_chiks2`, `dt_prnt`, `resul_prnt`, `dt_soro`, `resul_soro`, `dt_ns1`, `resul_ns1`, `dt_viral`, `resul_vi_n`, `dt_pcr`, `resulpcr`, `sorotipo`, `histopa_n`, `imunoh_n`, `clinc_chik`.
  * *Motivo:* Se o modelo ler um resultado de exame positivo, ele criará uma regra matemática óbvia ("Se Exame=Positivo, então Dengue") e ignorará completamente o quadro clínico (febre, dores, etc.), inutilizando a IA para o cenário de triagem sem exames rápidos.

### 2. Viés de Prognóstico e Desfecho
Nosso problema de negócio é de **Diagnóstico** (descobrir qual é o vírus), não de Prognóstico (descobrir se o paciente vai sobreviver). 
* **Comorbidades Prévias:** `diabetes`, `hematolog`, `hepatopat`, `renal`, `hipertensa`, `acido_pept`, `auto_imune`.
  * *Motivo:* Ter diabetes ou hipertensão agrava a doença, mas não é um sintoma da picada do mosquito. Manter isso faria o modelo associar falsamente o vírus ao histórico de saúde crônico do paciente.
* **Desfecho Hospitalar:** `hospitaliz`, `dt_interna`, `doenca_tra`, `evolucao`, `dt_obito`, `dt_encerra`, `complica`.
  * *Motivo:* O fato de o paciente ter morrido ou sido internado é uma consequência da doença, não um dado de entrada para prevê-la.

### 3. Variância Zero e Matrizes Esparsas Inúteis
Durante a Análise Exploratória de Dados (EDA) na nossa amostra de 100.000 linhas, identificamos atributos com quase 100% de valores nulos (`NaN`).
* **Sintomas Hemorrágicos Raros:** `mani_hemor`, `epistaxe` (sangramento nasal), `gengivo`, `metro` (metrorragia), `petequias`, `hematura` (sangue na urina), `sangram`, `laco_n`, `plasmatico`, `evidencia`, `plaq_menor`, `con_fhd`.
  * *Motivo:* Sendo eventos extremamente raros na amostra base, essas colunas não oferecem Ganho de Informação (*Information Gain*) para a Árvore de Decisão. Mantê-las apenas consumiria processamento e memória à toa. *(Nota: O sangramento uterino e outros sinais de alarme principais foram mantidos ou fundidos na etapa de Engenharia de Atributos, aqui foram excluídos SOMENTE sintomas que na nossa amostragem sequer apareciam).*

### 4. Burocracia, Metadados e Redundâncias
Campos administrativos do sistema governamental que não possuem relação causal com a biologia da infecção viral.
* **Controle do Sistema:** `dt_invest`, `dt_digita`, `cs_flxret`, `flxrecebi`, `migrado_w`, `tp_sistema`, `criterio`.
  * *Motivo:* A data em que o digitador do hospital inseriu a ficha no sistema não altera o diagnóstico clínico. O campo `criterio` foi descartado para evitar viés de seleção entre casos confirmados por laboratório vs. clínica.
* **Localidades Redundantes e Demografia Irrelevante:** `tp_not`, `id_agravo`, `cs_raca`, `sg_uf`, `id_mn_resi`, `id_rg_resi`, `id_pais`, `uf`, `municipio`, `tpautocto`, `coufinf`, `copaisinf`, `comuninf`.
  * *Motivo:* O município de notificação principal já foi mantido em outro atributo. Identificadores estaduais e nacionais repetitivos foram removidos.
* **Idade e Ano de Nascimento:** `ano_nasc`.
  * *Motivo:* Redundante. A coluna de idade primária (`nu_idade_n`) foi mantida para sofrer conversão matemática para anos inteiros na próxima etapa.
* **Ocupação:** `id_ocupa_n`.
  * *Motivo:* O vetor transmissor (mosquito *Aedes aegypti*) não discrimina vítimas com base no regime de contratação trabalhista (CLT). O risco de infecção está ligado à localidade e vulnerabilidade sanitária, não ao código CBO da profissão.
* **O Risco do Ano (`nu_ano`):** * *Motivo:* Excluído para evitar que o algoritmo memorize padrões temporais fixos ("overfitting" no ano da coleta). A verdadeira sazonalidade da doença será extraída dos meses de notificação (período de chuvas).

---
**Próximo Passo:** O dataset resultante (`dataset_sem_col_irrelevantes.csv`) contém os 55 atributos clínicos e temporais estritamente necessários e será submetido a scripts de *Feature Engineering* para imputação de nulos, binarização lógica (0 e 1), agrupamentos de atributos e cálculo de dias de evolução da doença.