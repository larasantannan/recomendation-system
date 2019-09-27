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

client = MongoClient('127.0.0.1')
db = client['devTest']

# Realização do crawler para buscar as informações do professor.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)

# Por hora, tenho que inserir o link do escavdor de cada professor, mas estou em busca de uma alternativa para isso.
driver.get("https://www.escavador.com/sobre/6109187/mauricio-pamplona-segundo")

#Seleção dos campos que serão parseados.
name = driver.find_element_by_xpath('//*[@id="usuario"]/div[1]/div/header/div/div[1]/h1')
resume = driver.find_element_by_xpath('//*[@id="usuario"]/div[1]/div/header/div/div[2]/p')
academic = driver.find_element_by_xpath('//*[@id="formacao"]/div')
languages = driver.find_element_by_xpath('//*[@id="idiomas"]/div[2]')
production = driver.find_element_by_xpath('//*[@id="producoes"]/ul')
research = driver.find_element_by_xpath('//*[@id="projetos"]/ul')
#development = driver.find_element_by_xpath('//*[@id="projetosDesenvolvimento"]/ul')

#db.professor.remove()
db.professor.insert({"name": name.text, "resume": resume.text, "academic": academic.text, "languages": languages.text, 'research': research.text, 'productions': production.text})

for r in db.professor.find():
        print(r)