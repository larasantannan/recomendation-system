# Sistema de Recomendação de Orientação

Utilizar Python3.

As importações necessárias para rodar o programa encontram-se no arquivo "requirements.txt".

Para realizar as importações: pip3 install -r requirements.txt

# Teste lucene

No arquivo lucene_test.py esto localizados os testes referentes à criação de tokens e análise do texto com o Lucene.

# Crawler

No arquivo crawler.py é realizado o crawler das informações do professor e essas são parseadas através do WebDriver.
Após o parser, tais informações em texto são analisadas pelo Lucene, considerando os espaços em branco e em seguida são inseridas no índice de acordo com o tipo de campo a que essas pertencem.

