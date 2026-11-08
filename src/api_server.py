from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Import your existing RAG logic
from src.rag_chain_utils import ask


app = FastAPI(title="SaySo RAG System API")


# Allow Node.js to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your Node.js domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected req body 
class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"📥 Received query from Node.js: {request.query}")


    try:
        # Call RAG func:
        res = ask(request.query)

        # fastAPI will automatically convert this dic to json
        return {
            "status": "success",
            "answer": res["answer"],
            "sources": res["sources"]
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
    
if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("src.api_server:app", host="0.0.0.0", port=8001, reload=True)