from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import WebBaseLoader

# Create a FastAPI instance
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the application to be accessed from a different origin (e.g., a React.js app)
origins = [
    "http://localhost:5173",  # Replace with the URL of your React.js app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the chat request
class ChatRequest(BaseModel):
    query: str

# Initialize the RAG (Retrieval Augmented Generation) components
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
loader = WebBaseLoader("https://fr.wikipedia.org/wiki/XAI_(entreprise)")
documents = loader.load()
embeddings = OllamaEmbeddings(model="mistral")
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()
llm = Ollama(
    model="mistral", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)
rag_chain = RetrievalQA.from_llm(llm=llm, retriever=retriever)

# Define a FastAPI endpoint for the chat functionality
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Handle chat requests and return the response.

    Args:
        request (ChatRequest): A Pydantic model containing the user's query.

    Returns:
        dict: A dictionary containing the response.

    Raises:
        HTTPException: If an exception occurs during the chat process.
    """
    try:
        response = rag_chain.run(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define a FastAPI endpoint for handling OPTIONS requests to the /chat endpoint
@app.options("/chat")
async def options_chat():
    """
    Handle OPTIONS requests to the /chat endpoint.

    This is required for CORS (Cross-Origin Resource Sharing) compliance.

    Returns:
        dict: An empty dictionary.
    """
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)