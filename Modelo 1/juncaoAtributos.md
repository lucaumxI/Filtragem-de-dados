# Documentação: Pré-Processamento - Etapa 2 agrupamento de atributos

**Arquivo Relacionado:** `juncaoAtributos.py`
**Objetivo:** Reduzir a dimensionalidade do dataset do SINAN, removendo atributos que introduzem ruído, viés ou vazamento de dados no treinamento dos modelos.

## Resumo da Execução
* **Entrada:** Dataset amostrado com 45 atributos e 200.000 instâncias.
* **Saída:** Dataset limpo com 21 atributos e 179.163 instâncias.


#### ANOTAÇÕES DEPOIS REESCREVO

- classi_fin: foram descartadas as instancias onde não há um diagnóstico seja positivo ou negativo. Foi criada uma nova coluna arbovirose onde caso classi_fin = dengue OU chikungunya -> arbovirose = 1, do contrário arbovirose = 0
- dt_sin_pri: vai ser útil para a sazonalidade da doença, pra isso basta extrair os meses da data, e tmabém útil pra evolução da doença, dengue principalmente tem um cronograma bem definido que lá pro dia 5 do começo dos sintomas tem a piora do vomito, por exemplo, para isso precisa fazer dt_notific - dt_sin_pri = dias_ate_a_consulta
- nu_anos: transformou do código bizarro para anos inteiro, util porque diferentes faixas etárias apresentam diferentes sintomas
- cs_sexo: transformou de F e M para 0 e 1. Motivo de manter é o mesmo de cima
- Todos os sintomas foram binarizados para 0 e 1 (usavam 1 e 2 originalmente)

**TODO**
atributos arbovirose e idade_anos estão como float, converter para int 