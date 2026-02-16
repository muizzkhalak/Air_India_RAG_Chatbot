from .modules import DataCollator, LLMClient
from pathlib import Path
import shutil


class Chatbot:

    def __init__(self, 
                    region_name, 
                    embedding_model_id,
                    llm_model_id,
                    pdf_directory,
                    collection_name,
                    persist_directory,
                    force_recreate_vector_store=False):
        
        self.region_name = region_name
        self.embedding_model_id = embedding_model_id
        self.llm_model_id = llm_model_id
        self.pdf_directory = pdf_directory
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.vector_store = self.get_vector_store(
                                    region_name=region_name,
                                    model_id=embedding_model_id,
                                    pdf_directory=pdf_directory,
                                    collection_name=collection_name,
                                    persist_directory=persist_directory,
                                    force_recreate_vector_store=force_recreate_vector_store
                                )
        
    def get_vector_store(self, region_name, model_id, pdf_directory, collection_name, persist_directory, force_recreate_vector_store):
    
        data_collator = DataCollator()
        
        if force_recreate_vector_store:
            # wipe persisted store so we rebuild from scratch
            p = Path(persist_directory)
            if p.exists():
                shutil.rmtree(p)

        if not data_collator.check_vector_store_exists(persist_directory):
            data_collator.add_documents_to_vector_store(region_name, model_id, pdf_directory, collection_name, persist_directory)

        vector_store = data_collator.load_vector_store(region_name, model_id, collection_name, persist_directory)
        return vector_store

    def get_response(self, input_text):

        docs_from_vector_store = self.vector_store.similarity_search(input_text,k=3)

        llm_client = LLMClient(region_name=self.region_name, model_id=self.llm_model_id)
        response = llm_client.generate_response(docs_from_vector_store, input_text)
        return response

    










    
