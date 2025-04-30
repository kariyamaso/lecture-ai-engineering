# backend/llm.py
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME
from dotenv import load_dotenv
import os

# Load environment variables from .env file located in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env') # Navigate up two levels to day1/
load_dotenv(dotenv_path=dotenv_path)

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# Cache the loaded model and tokenizer
_model = None
_tokenizer = None
_pipe = None

def load_pipeline():
    """Load and return the Hugging Face text generation pipeline."""
    global _model, _tokenizer, _pipe
    if _pipe is None:
        print(f"Loading model: {MODEL_NAME}")
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")

            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=huggingface_token)
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.bfloat16,
                token=huggingface_token,
                device_map="auto", # Automatically select device
            )

            _pipe = pipeline(
                "text-generation",
                model=_model,
                tokenizer=_tokenizer,
                # device=device # device_map="auto" handles this
            )
            print(f"Model '{MODEL_NAME}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model '{MODEL_NAME}': {e}")
            # Consider raising the exception or returning None depending on desired error handling
            raise  # Re-raise the exception for now
    return _pipe

# --- Simple Generation Function (can be expanded) ---
def generate_text(prompt: str, max_new_tokens: int = 256) -> str:
    """Generate text using the loaded pipeline."""
    pipe = load_pipeline()
    if not pipe:
        return "Error: Model pipeline not loaded."

    # Example using a Gemma-specific chat template (adjust if using a different model)
    # Note: You might need a more sophisticated prompt engineering approach for code generation.
    chat = [
        { "role": "user", "content": prompt },
    ]
    formatted_prompt = pipe.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

    outputs = pipe(
        formatted_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )
    generated_text = outputs[0]["generated_text"]

    # Extract the response part after the template
    # This depends heavily on the model and template used
    response_marker = "<start_of_turn>model\n"
    if response_marker in generated_text:
        return generated_text.split(response_marker, 1)[1]
    else:
        # Fallback if marker not found (might return the whole output including prompt)
        # You might need to refine this extraction logic.
        print("Warning: Could not find response marker. Returning full generated text.")
        return generated_text
