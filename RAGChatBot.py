import os
from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr
from KnowledgeBase import get_chroma_vector_store
from LoadData import obtener_pedazos
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

def get_llm():   
	open_ai_api_key = os.environ['OPENAI_API_KEY']
  return ChatOpenAI(api_key=SecretStr(open_ai_api_key), model="gpt-3.5-turbo-0125",)

def get_embedding_model():
    open_ai_api_key = os.environ['OPENAI_API_KEY']
    return OpenAIEmbeddings(model="text-embedding-3-small", ​api_key=SecretStr(open_ai_api_key))

def get_prompt():
    template =  """Utilice las siguientes piezas de contexto para responder la pregunta.
                    ​ ​ ​ ​ al final. Si no sabes la respuesta, solo di eso.
                   Si no lo sabes, no intentes inventar una respuesta.
                   Utilice seis oraciones como máximo y mantenga la respuesta concisa.

                    {context}

                    Pregunta: {question}

                    Respuesta:"""
    return PromptTemplate.from_template(template)

def QA(nombrepdf:str):    
	​#aqui imprimimos algunos mensajes para ver en la línea de comando
	​print("Cargando archivo pdf...")    
	​print("Splitting pages into chunks...")
	​#separamos las paginas del archivos y cada pagina la separamos
	​#en pequeños pedazos de contenido llamados chunks
	​chunks = obtener_pedazos(nombrepdf)    
	
	​#aqui creamos los embeddings que utilizaremos más adelante para preparar los
	​#datos que utilizaremos para chatear.​
	​embeds = get_embedding_model()
	​vectorstore = get_chroma_vector_store(chunks, embeds)

  #procedemos a crear el retriever que se encargara de mandar la información
	​#al servicio de inteligencia artificial
	​retriever = vectorstore.as_retriever(search_type="similarity", ​search_kwargs={"k": 6})    
	​llm = get_llm()
	​prompt = get_prompt()
  rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | ​prompt | llm | StrOutputParser())

  while True:        
	​	​message = input("Inserte su pregunta: ")        
	​	​if message == "salir":            
	​	​	​vectorstore.delete_collection()            
	​		​​break        
	​	​else:            
	​	​	​for chunk in rag_chain.stream(message):                
	​	​	​	​print(chunk, end="", flush=True)            
	​	​	​	​print("\n\n")

nombrepdf = "<el nombre de su pdf>"
QA(nombrepdf)
