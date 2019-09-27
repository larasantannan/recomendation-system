# Sistema de Recomendação de Orientação

Utilizar Python3.

As importações necessárias para rodar o programa encontram-se no arquivo "requirements.txt".

Para realizar as importações: pip3 install -r requirements.txt

# Teste lucene

No arquivo lucene_test.py esto localizados os testes referentes à criação de tokens e análise do texto com o Lucene.

# Crawler

No arquivo crawler.py é realizado o crawler das informações do professor e essas são parseadas através do WebDriver e salva no banco de dados. 
Após o parser, tais informações em texto são analisadas pelo Lucene, considerando os espaços em branco e em seguida são inseridas no índice de acordo com o tipo de campo a que essas pertencem.

# Lucene

  No arquivo lucene.py, a collection referente aos professores e suas informações é lida, analisada e anexada pelo Lucene. Para realizar a análise, foi utilizado o PortugueseAnalizer, levando em consideração que a maior parte dos textos encontra-se em português. A query de busca no lucene também é realizada nesse arquivo. Para isso foi considerado a busca através do FuzzyQuery.
  
  Após a indexação e busca no lucene de acordo com o termo buscado pelo usuário, temos a inicialização da aplicaço web através do Flask. 
  
 # Templates
 
 - Temos o template da home, onde o usuário digitará o termo buscado. (home.html)
 - Template da página de resultados, com a listagem dos professores que esto associados ao termo buscado pelo usuário. (contents.html)
