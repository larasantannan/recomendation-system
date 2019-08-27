import lucene
import sys

from java.io import StringReader, File
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.pt import PortugueseAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
lucene.initVM()

INDEX_DIR = "/index_test"

# Tokenizer exemplo.
test = "Isso é um teste."
tokenizer = StandardTokenizer()
tokenizer.setReader(StringReader(test))
charTermAttrib = tokenizer.getAttribute(CharTermAttribute.class_)
tokenizer.reset()
tokens = []

while tokenizer.incrementToken():
    tokens.append(charTermAttrib.toString())

print(tokens)

# PortugueseAnalyzer exemplo.
analyzer = PortugueseAnalyzer()
stream = analyzer.tokenStream("", StringReader(test))
stream.reset()
tokens = []

while stream.incrementToken():
    tokens.append(stream.getAttribute(CharTermAttribute.class_).toString())

print(tokens)
