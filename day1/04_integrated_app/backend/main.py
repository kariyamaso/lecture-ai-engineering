# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import llm
import uvicorn

app = FastAPI(
    title="AI Code Generation API",
    description="API to generate code snippets based on natural language prompts using a Hugging Face model.",
    version="0.1.0"
)

# --- Pydantic Models ---
class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 256 # Default value, can be overridden in request

class CodeResponse(BaseModel):
    generated_code: str

# --- API Endpoints ---
@app.post("/generate", response_model=CodeResponse)
async def generate_code_endpoint(request: PromptRequest):
    """
    Receives a natural language prompt and returns generated code.
    """
    print(f"Received prompt: {request.prompt}")
    try:
        # Simple prompt formatting - might need improvement for code gen
        code_generation_prompt = f"以下の指示に基づいてPythonコードを生成してください:\n\n{request.prompt}\n\n生成されたコードのみを提供してください。説明やコメントは不要です。\n```python"

        generated_text = llm.generate_text(
            prompt=code_generation_prompt,
            max_new_tokens=request.max_new_tokens
        )

        # Clean up the output - remove potential closing backticks if added by the model
        if generated_text.endswith("```"):
            generated_code = generated_text[:-3].strip()
        else:
            generated_code = generated_text.strip()

        print(f"Generated code snippet (first 100 chars): {generated_code[:100]}...")
        return CodeResponse(generated_code=generated_code)

    except Exception as e:
        print(f"Error during code generation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate code: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Code Generation API"}

# --- Model Loading on Startup (Optional but recommended) ---
@app.on_event("startup")
async def startup_event():
    print("Application startup: Loading model...")
    try:
        llm.load_pipeline() # Pre-load the model when the server starts
        print("Model loaded successfully during startup.")
    except Exception as e:
        print(f"ERROR: Failed to load model during startup: {e}")
        # Depending on severity, you might want the app to fail startup
        # raise RuntimeError(f"Failed to load model during startup: {e}")

# --- Run with Uvicorn (for local development) ---
if __name__ == "__main__":
    # Load the model before starting the server if run directly
    # Note: Uvicorn's --reload handles this better in dev
    print("Running script directly: Pre-loading model...")
    try:
        llm.load_pipeline()
    except Exception as e:
        print(f"Failed to pre-load model when running script directly: {e}")
        # Decide if you want to exit or continue without the model
        # exit(1)

    print("Starting Uvicorn server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
