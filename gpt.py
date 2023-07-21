from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import SystemMessage, AIMessage

# chat = ChatOpenAI(temperature=0)
# system_prompt = SystemMessagePromptTemplate.from_template("You are a helpful AI assistant.")

# messages = [
#     SystemMessage(content=system_prompt.format_prompt().to_string()),
# ]

# response = chat(messages)
# output = response[0].content
# print(output)


handbook = TextLoader("db/us_code.txt").load()
text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=0)
documents = text_splitter.split_documents(handbook)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

query = "What accomodations can someone who is blind access?"
docs = db.similarity_search(query)
with open("db/output.txt", "w") as f:
    f.write(docs[0].page_content)