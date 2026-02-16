import os
from uuid import uuid4
from .embedding_model import AmazonTitanEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


class VectorStore:
    
    def __init__(self, collection_name, embedding_function, directory=None):
        self.collection_name = collection_name
        self.embedding_function = embedding_function
        self.directory = directory
        self.client = Chroma(collection_name=collection_name, 
                             embedding_function=embedding_function, 
                             persist_directory=directory)

    def add_documents(self, documents, ids=None):
        self.client.add_documents(documents, ids=ids)

    def similarity_search(self, query, k=5):
        return self.client.similarity_search(query, k=k)



class DataCollator:

    def _preprocess_documents(self, pdf_directory):
        # Load PDF documents
        loader = PyPDFDirectoryLoader(pdf_directory, glob="**/*.pdf")
        documents = loader.load()

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_documents = text_splitter.split_documents(documents)

        return split_documents
    
    def add_documents_to_vector_store(self, region_name, model_id, pdf_directory, collection_name, persist_directory=None):

        # Preprocess documents
        documents = self._preprocess_documents(pdf_directory)

        # Initialize embedding model and vector store
        embedding_model = AmazonTitanEmbeddings(region_name=region_name, model_id=model_id)
        vector_store = VectorStore(collection_name=collection_name, 
                                   embedding_function=embedding_model, 
                                   directory=persist_directory)

        # Add split documents to vector store
        ids = [str(uuid4()) for _ in documents]
        vector_store.add_documents(documents, ids=ids)

    def load_vector_store(self, region_name, model_id, collection_name, persist_directory=None):
        
        embedding_model = AmazonTitanEmbeddings(region_name=region_name, model_id=model_id)
        vector_store = VectorStore(collection_name=collection_name, 
                                   embedding_function=embedding_model, 
                                   directory=persist_directory)
        return vector_store
    
    def check_vector_store_exists(self, persist_directory):
        
        if os.path.exists(persist_directory):
            return True
        return False