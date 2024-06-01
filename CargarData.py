import bs4
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extraer_paginas(nombrepdf):
	try:
	  loader = PyPDFLoader(nombrepdf)
          pages = loader.load_and_split()
          print(f"Se cargaron {len(pages)} paginas del pdf {nombrepdf}")
          return pages    
        except Exception as e:
          print(f"Error error cargando PDF, razon: {e}"​)

def separar_paginas(paginas, dimension):​
	​try:
	    text_splitter = RecursiveCharacterTextSplitter(chunk_size=dimension, ​chunk_overlap=200, add_start_index=True)
	    chunks = text_splitter.split_documents(paginas)
	    print(f"Se separaron {len(paginas)} paginas en {len(chunks)} pedazos")
            return chunks
        except Exception as e:
            print(f"Error separando pedazos, razon: {e}")

​def obtener_pedazos(nombre_pdf):
        docs = extraer_paginas(nombre_pdf)
        chunks = separar_paginas(docs, 500)
	​return chunks
