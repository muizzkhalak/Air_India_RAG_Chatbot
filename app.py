from airindiabot import Chatbot
import streamlit as st
import dotenv
dotenv.load_dotenv()

def main():

    chatbot = Chatbot(
        region_name='eu-north-1', 
        embedding_model_id="amazon.titan-embed-text-v2:0",
        llm_model_id="eu.amazon.nova-pro-v1:0", 
        pdf_directory="./data", 
        collection_name="air_india_docs", 
        persist_directory="./vector_store",
        force_recreate_vector_store=False
    )

    st.set_page_config(page_title="Air India Assistant", layout="wide")

    st.title("✈️ Air India Chat Assistant")
    st.markdown("Ask any question about Air India based on the provided documents.")

    # Input field
    question = st.text_input("Enter your question:")

    # When the user submits a question
    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    result = chatbot.get_response(question)
                    st.markdown("### 📄 Answer")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
