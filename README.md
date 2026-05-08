# Filtragem-de-dados

Não irei upar o dataset no git porque é muito pesado pro versionamento então esse repositório é APENAS para ir colocando os script de limpeza que fizeram (criem um .py para cada limpeza mesmo). O gitignore ta configurado para ignorar tudo que não seja .py e .md. Sempre que fizer qualquer tratamento no dataset POR FAVOR crie um .md detalhando O QUE VOCÊ fez e o PORQUÊ (só abrir qualquer .md que tiver ai que você entende o formato). Futuramente para treinar o modelo você irá baixar o datasetAmostrado.csv (irei por link depois) e executar os scrips na ordem certa e pronto, tem o dataset polido bonitinho.

## Dataset para o modelo de classficação de arbovirose ou não

Aqui vai dados pro modelo apenas dizer se o paciente tem ou não arbovirose, independente de qual seja ela. Para limpar o dataset pra treinar esse modelo é só seguir os passos abaixo
1. clone o repositório (git clone https://github.com/lucaumxI/Filtragem-de-dados.git)
2. baixe o arquivo datasetAmostrado.csv (link)
3. execute o script para limpar as colunas irrelevantes (python exclusaoColunas.py)