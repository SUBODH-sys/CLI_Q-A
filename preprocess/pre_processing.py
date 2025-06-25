import json
import re
import random
from pathlib import Path

# Input and output paths
INPUT_FILE = "data/qa_pairs.json"
TRAIN_FILE = "data/train.jsonl"
VAL_FILE = "data/val.jsonl"
VAL_SPLIT = 0.1  # 10% for more training data
RANDOM_SEED = 42  # For reproducibility

# def clean_answer(answer):
#     """Extract primary command, skip non-command answers."""
#     # Remove Unicode characters
#     answer = re.sub(r"\\u[0-9a-fA-F]{4}", "", answer)
#     # Define tools
#     tools = r"^(git|tar|grep|python|bash|ssh|cat|echo|read|find|sed|awk)\b"
#     # Extract commands
#     commands = []
#     # Match $ commands
#     dollar_commands = re.findall(r"^\$\s*(.*?)(?:\n|$)", answer, re.MULTILINE)
#     for cmd in dollar_commands:
#         if re.match(tools, cmd.lower()):
#             commands.append(cmd.lstrip("$ ").strip())
#     # Match code blocks
#     code_blocks = re.findall(r"<code>(.*?)</code>|```(.*?)```", answer, re.DOTALL)
#     for block in code_blocks:
#         block_text = block[0] or block[1]
#         lines = block_text.split("\n")
#         for line in lines:
#             line = line.strip()
#             if re.match(tools, line.lower()):
#                 commands.append(line.lstrip("$ ").strip())
#     # Match inline commands (fallback)
#     inline_commands = re.findall(
#         r"\b(?:git|tar|grep|python|bash|ssh|cat|echo|read|find|sed|awk)\s+[^\s][\w\-\/\.\=\;\|\&\>\<\*\+\[\]\{\}\(\)\s]*(?=\s|$|\n|\.|,|\))",
#         answer,
#         re.IGNORECASE
#     )
#     for cmd in inline_commands:
#         cmd = cmd.strip()
#         if cmd not in commands and len(cmd.split()) > 1:
#             commands.append(cmd)
#     # Return first command or None
#     if commands:
#         return commands[0]
#     return None

def format_prompt(question, answer):
    """Format Q&A pair."""
    return f"Question: {question}\nAnswer: {answer}"

def main():
    # Set random seed
    random.seed(RANDOM_SEED)

    # Load Q&A pairs
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)

    # Validate and format
    formatted_pairs = []
    seen_questions = set()
    for pair in qa_pairs:
        question = pair["question"].strip()
        answer = pair["answer"].strip()
        if not question or not answer:
            continue
        question_key = question.lower().strip("?")
        if question_key in seen_questions:
            continue
        seen_questions.add(question_key)
        # cleaned_answer = clean_answer(answer)
        # if cleaned_answer:
        #     formatted_pairs.append({"text": format_prompt(question, cleaned_answer)})
        formatted_pairs.append({"text": format_prompt(question, answer)})

    print(f"Processed {len(formatted_pairs)} unique Q&A pairs")

    # Shuffle and split
    random.shuffle(formatted_pairs)
    val_size = int(len(formatted_pairs) * VAL_SPLIT)
    train_pairs = formatted_pairs[val_size:]
    val_pairs = formatted_pairs[:val_size]

    # Save train set
    Path(TRAIN_FILE).parent.mkdir(exist_ok=True)
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for pair in train_pairs:
            f.write(json.dumps(pair) + "\n")
    print(f"Saved {len(train_pairs)} pairs to {TRAIN_FILE}")

    # Save validation set
    with open(VAL_FILE, "w", encoding="utf-8") as f:
        for pair in val_pairs:
            f.write(json.dumps(pair) + "\n")
    print(f"Saved {len(val_pairs)} pairs to {VAL_FILE}")

if __name__ == "__main__":
    main()