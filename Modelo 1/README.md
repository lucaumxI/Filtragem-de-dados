# Filtragem-de-dados

Não irei upar o dataset no git porque é muito pesado pro versionamento então esse repositório é APENAS para ir colocando os script de limpeza que fizeram (criem um .py para cada limpeza mesmo, exemplo, fez um script unica e exclusivamente pra transformar o atributo de data para semana epidemiologica, crie um .py e um .md APENAS para isso). O gitignore ta configurado para ignorar tudo que não seja .py e .md. Sempre que fizer qualquer tratamento no dataset POR FAVOR crie um .md detalhando O QUE VOCÊ fez e o PORQUÊ (só abrir qualquer .md que tiver ai que você entende o formato). Futuramente para treinar o modelo você irá baixar o datasetAmostrado.csv (irei por link depois) e executar os scrips na ordem certa e pronto, tem o dataset polido bonitinho.

## Dataset para o modelo de classficação de arbovirose ou não
Aqui vai dados pro modelo apenas dizer se o paciente tem ou não arbovirose, independente de qual seja ela.

### Operações já feitas
- Redução de instâncias através de amostragem aleatória dos datasets de dengue e chikungunya dos anos de 2021-2025 (foram pegos 20.000 casos de cada tabela, totalizando 200.000 instâncias)
- Integração das 10 tabelas em uma única
- Redução de atributos irrelevantes como dados administrativos e atributos referentes a exames (data leak) e prognósticos

### TODO
- Agrupar casos de dengue e chikungunya em um unico atributo "arbovirose"

### Como conseguir o dataset pré-processado
1. clone o repositório (git clone https://github.com/lucaumxI/Filtragem-de-dados.git)
2. baixe o arquivo datasetAmostrado.csv ([link](https://drive.google.com/drive/folders/15GGEFAqv14SVNw4XXq_Jpgey_Bje822Q?usp=sharing))
3. execute o script para limpar as colunas irrelevantes (python exclusaoColunas.py)
