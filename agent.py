import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import sys
import re

# Model and tokenizer paths
MODEL_PATH = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

def generate_command(question):
    print(f"Processing question: {question}")
    prompt = f"Question: {question}\nAnswer: "
    #print(f"Prompt: {prompt}")
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=256,
        truncation=True,
        padding=True,
        return_attention_mask=True
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    #print(f"Input IDs shape: {inputs['input_ids'].shape}")

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=100,
            num_return_sequences=1,
            do_sample=True,
            temperature=1.0,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            logits_processor=[
                lambda input_ids, scores: torch.clamp(scores, min=-1e10, max=1e10)
            ]
        )
    #print(f"Output IDs shape: {outputs.shape}")

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"{response}")
    
    # Extract command
    answer = response.split("Answer: ")[-1].strip()
    # Look for first code block
    code_block = re.search(r"```(?:bash)?\n(.*?)\n```", answer, re.DOTALL)
    if code_block:
        command = code_block.group(1).strip()
    else:
        # Fall back to first non-empty line that looks like a command
        lines = [line.strip() for line in answer.split("\n") if line.strip()]
        command = next((line for line in lines if not line.startswith("Note:") and not line.isalpha()), lines[0] if lines else "")
    #print(f"Extracted command: {command}")
    return command

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python agent.py \"<question>\"")
        sys.exit(1)
    question = sys.argv[1]
    command = generate_command(question)