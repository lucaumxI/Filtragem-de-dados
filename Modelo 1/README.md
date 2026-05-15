# Modelo 1

## Dataset original
Foi coletado do Sinan os dataset referentes aos anos de 2021-2025, esse intervalo foi escolhido porque em 2021 foi alterado a estruturação do dataset. Ao todo tinhamos 5 arquivos .csv da dengue e 5 da chikungunya, a quantidade de instâncias somadas dos dataset chegava próxima aos 8 milhões, por conta desse alto volume foi realizada uma amostragem aleatória onde de cada tabela escolhiamos 20 mil instâncias, totalizando um datasetAmostrado de 200 mil instâncias.

## Datase Amostrado
Com o datasetAmostrado pronto, realizamos uma análise semântica de cada variável, decidimos se elas eram ou não relevantes para a aplicação e excluímos as colunas irrelevantes para diminuir a dimensionalidade do dataset.

### Como conseguir o dataset pré-processado
1. clone o repositório (git clone https://github.com/lucaumxI/Filtragem-de-dados.git)
2. baixe o arquivo datasetAmostrado.csv ([link](https://drive.google.com/drive/folders/15GGEFAqv14SVNw4XXq_Jpgey_Bje822Q?usp=sharing))
3. execute o script para limpar as colunas irrelevantes (python exclusaoColunas.py)
