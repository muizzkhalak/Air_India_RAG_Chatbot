import boto3
import json

def prompt(context, input_text):

    llm_prompt= f"""
    You are a helpful assistant. Use the following context to answer the user's question.
    The context is a collection of documents that may contain relevant information about Air India, its operations, policies, and other related topics.
    Context:
    {context}

    User's Question:
    {input_text}
    """

    ige_message_list = [
                {
                    "role": "user",
                    "content": [
                        {"text": llm_prompt}
                    ],
                }
            ]

    ige_inf_params = {"maxTokens": 300, "topP": 0.1, "topK": 20, "temperature": 0}
    ige_native_request = {
                "schemaVersion": "messages-v1",
                "messages": ige_message_list,
                "system": [{
                    "text": "You are a helpful assistant"
                }],
                "inferenceConfig": ige_inf_params,
            }

    return ige_native_request


class LLMClient:

    def __init__(self, region_name, model_id):

        self.client = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = model_id

    def generate_response(self, context, input_text):

        ige_native_request = prompt(context, input_text)
        response = self.client.invoke_model(modelId=self.model_id, body=json.dumps(ige_native_request))
        result = json.loads(response["body"].read())
        return result['output']['message']['content'][0]['text']