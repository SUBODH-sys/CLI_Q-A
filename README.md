# Project Report: CLI Command Generator
### Introduction
This project developed a CLI command generator using TinyLlama-1.1B, leveraging ~90 Q&A pairs to generate commands for tasks like Git branching, file compression, and virtual environment setup. The goal was to automate CLI assistance for developers, supporting queries like “Create a new Git branch and switch to it.”

### Methodology
The dataset (train.jsonl, val.jsonl, ~81/9 split) was curated with pairs in the format Question: <query>\nAnswer: <command/explanation>. Fine-tuning TinyLlama-1.1B was attempted in Colab (1 epoch, FP16, no QLoRA), but the model produced empty outputs, likely due to a small dataset (~90 pairs vs. required ≥150). Instead, agent.py was implemented using the pre-trained TinyLlama, with regex parsing to extract commands from code blocks or command-like lines. The script runs as python agent.py "<query>".

### Evaluation
Five company-provided prompts were tested:

1. Static: Pre-trained model raw responses matched ground truth for 2/5 prompts (40%), e.g., git checkout -b and python -m venv appeared, but others yielded Python scripts or GUI descriptions.

### Limitations stem from the pre-trained model’s verbosity and failed fine-tuning.

### Conclusion
The pre-trained model achieved limited success (2/5 static, 0.2 dynamic), highlighting the need for effective fine-tuning. Future work includes expanding the dataset to ≥150 pairs, using multiple epochs, and exploring QLoRA for efficient fine-tuning to improve CLI command accuracy.