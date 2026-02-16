# Air India RAG Chatbot

A Streamlit-based chatbot for Air India documentation using AWS Bedrock and ChromaDB.

## Prerequisites

- Docker and Docker Compose installed
- AWS account with access to Bedrock services
- AWS credentials configured

## Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

1. **Set up environment variables:**
   Create a `.env` file in the project root with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=eu-north-1
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

### Option 2: Using Docker directly

1. **Build the Docker image:**
   ```bash
   docker build -t air-india-chatbot .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 \
     -e AWS_ACCESS_KEY_ID=your_access_key \
     -e AWS_SECRET_ACCESS_KEY=your_secret_key \
     -e AWS_REGION=eu-north-1 \
     -e AWS_DEFAULT_OUTPUT=json \
     -v $(pwd)/data:/app/data:ro \
     -v $(pwd)/vector_store:/app/vector_store \
     air-india-chatbot
   ```

## Configuration

- **AWS Region:** Set to `eu-north-1` by default (matches your app configuration)
- **Data Directory:** Mount your PDF documents to `/app/data` in the container
- **Vector Store:** ChromaDB data is persisted in the `vector_store` directory
- **Port:** Application runs on port 8501

## Development

To run locally without Docker:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Make sure your AWS credentials have access to Amazon Bedrock services
- The first run may take longer as it processes PDF documents and creates embeddings
- Vector store data is persisted between container restarts