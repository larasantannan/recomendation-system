import sys
import lucene
import os
from lucene import JavaError
from pymongo import MongoClient

from java.io import File
from java.nio.file import Paths

from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from org.apache.lucene.document import Document, Field

from org.apache.lucene.analysis.pt import PortugueseAnalyzer
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
from org.apache.lucene.util import Version


# Inicialização do banco
client = MongoClient('127.0.0.1')
db = client['devTest']

professorList = []

# Inicialização do Lucene e criação dos índices.
lucene.initVM()
storeDir = os.path.dirname(os.path.abspath("index/"))
store = SimpleFSDirectory(Paths.get(storeDir))

doc = Document()

for r in db.professor.find():
    #print(r['research'])

    # Método para realizar a adição 
    def addDoc(field_name, text, writer):
        doc.add(Field(field_name, text, field))        
        writer.addDocument(doc)

    # Seleção do tipo de analizador do texto e configuração do IndexWriter.
    analyzer = PortugueseAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    #print(writer.numDocs())

    field = FieldType()
    field.setStored(True)
    field.setTokenized(True)
    field.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # Criação de diferentes campos para os diferentes campos parseados e adição desses documentos no index.
    addDoc("name", r['name'], writer)
    addDoc("research", r['research'], writer)
    writer.commit()
    writer.close()

# Nesse momento é realizada a busca dos termos dentro do índice.
searcher=IndexSearcher(DirectoryReader.open(store))
query = FuzzyQuery( Term("research", "programaçao"))

MAX = 1000
hits = searcher.search(query, MAX)

for hit in hits.scoreDocs:
    doc = searcher.doc(hit.doc)
    professorList.append(doc.get("name"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contents', methods=['POST'])
def contents():
    term = request.form['content']

    return render_template('contents.html',
    term=term,
    professors=professorList)


###### INÍCIO DA APLICAÇÃO ######

if __name__ == "__main__":
    app.run(debug=True)