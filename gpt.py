from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

handbook = TextLoader("db/selpa_handbook.txt").load()
text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=0)
documents = text_splitter.split_documents(handbook)
db = Chroma.from_documents(documents, OpenAIEmbeddings())

query = "What accomodations can a student with ADHD access?"
#docs = db.similarity_search(query)
# with open("db/output.txt", "w") as f:
#     for doc in docs:
#         f.write(doc.page_content)
docs = db.similarity_search_with_score(query)