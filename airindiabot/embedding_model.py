import boto3
import json
from langchain.embeddings.base import Embeddings
import tiktoken

class AmazonTitanEmbeddings(Embeddings):

    def __init__(self, region_name='eu-north-1', model_id='amazon.titan-embed-text-v2:0'):
        self.client = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = model_id
        self.max_tokens = 8000
        self.tokenizer = tiktoken.get_encoding('cl100k_base')

    def _safe_truncate(self, text):
        tokens = self.tokenizer.encode(text)
        if len(tokens) > self.max_tokens:
            tokens = tokens[:self.max_tokens]
        return self.tokenizer.decode(tokens)

    def embed_documents(self, texts):
        safe_texts = [self._safe_truncate(text) for text in texts]
        embeddings = []
        
        for text in safe_texts:
            request_body = json.dumps({
                "inputText": text
            })
            
            response = self.client.invoke_model(
                body=request_body,
                modelId=self.model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            embeddings.append(response_body['embedding'])
        
        return embeddings

    def embed_query(self, text):
        safe_text = self._safe_truncate(text)
        
        request_body = json.dumps({
            "inputText": safe_text
        })
        
        response = self.client.invoke_model(
            body=request_body,
            modelId=self.model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['embedding']