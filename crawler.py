import sys
import lucene
import os
from lucene import JavaError

from java.io import File
from java.nio.file import Paths

from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search import FuzzyQuery, MultiTermQuery, IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, FieldInfo, IndexOptions,MultiReader, Term
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.search.spans import SpanNearQuery, SpanQuery, SpanTermQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser

# Realização do crawler para buscar as informações do professor.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)

# Por hora, tenho que inserir o link do escavdor de cada professor, mas estou em busca de uma alternativa para isso.
driver.get("https://www.escavador.com/sobre/5906861/frederico-araujo-durao")

#Seleção dos campos que serão parseados.
name = driver.find_element_by_xpath('//*[@id="usuario"]/div[1]/div/header/div/div[1]/h1')
resume = driver.find_element_by_xpath('//*[@id="usuario"]/div[1]/div/header/div/div[2]/p')
academic = driver.find_element_by_xpath('//*[@id="formacao"]/div')
languages = driver.find_element_by_xpath('//*[@id="idiomas"]/div[2]')
phd = driver.find_element_by_xpath('//*[@id="pos-doutorado"]/div[2]')

# Método para realizar a adição 
def addDoc(field_name, text, writer):
        doc = Document()
        doc.add(Field(field_name, text, t2))        
        writer.addDocument(doc)

# Inicialização do Lucene e criação dos índices.
lucene.initVM()
storeDir = os.path.dirname(os.path.abspath("index/"))
store = SimpleFSDirectory(Paths.get(storeDir))

t2 = FieldType()
t2.setStored(False)
t2.setTokenized(True)
t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

# Seleção do tipo de analizador do texto e configuração do IndexWriter. Por enquanto utilizado o WhiteSpace analyzer devido à utilização de palavras em língua inglesa e portuguesa nos textos.
analyzer = WhitespaceAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(store, config)

# Criação de diferentes campos para os diferentes campos parseados e adição desses documentos no index.
addDoc("name", name.text, writer)
addDoc("resume", resume.text, writer)
addDoc("phd", phd.text, writer)
writer.commit()
writer.close()

driver.close()

# Nesse momento é realizada a busca dos termos dentro dos respectivos campos.
searcher=IndexSearcher(DirectoryReader.open(store))

# Query para a realização dos termos buscados. Os termos buscados devem estar em um mesmo campo.
clauses=[1,2]
clauses[0] =  SpanMultiTermQueryWrapper(FuzzyQuery( Term("resume", "Web")))
clauses[1] =  SpanMultiTermQueryWrapper(FuzzyQuery( Term("resume", "WISER")))
query = SpanNearQuery(clauses,50, False)
hits = searcher.search(query, 2).scoreDocs

for hit in hits:
        print (hit.score, hit.doc, hit.toString())
        doc = searcher.doc(hit.doc)
        print (doc.getFields())