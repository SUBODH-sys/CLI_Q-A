import requests
import json
import time
import html
import re

# Configuration
API_KEY = "rl_AP7n9SvpVrZBHPVGTUdN8HTqS"  # Replace with your Stack Exchange API key
BASE_URL = "https://api.stackexchange.com/2.3"
TAGS = [
    ("git", 40),
    ("bash", 40),
    ("tar", 40),
    ("grep", 40),
    ("python-venv", 40),
    ("venv", 10)  # Lower target for venv
]  # Command-line topics with pair targets
OUTPUT_FILE = "data/qa_pairs.json"

def clean_text(text):
    """Clean HTML tags and decode HTML entities from question/answer text."""
    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = " ".join(text.split())
    return text

def fetch_qa_pairs(tag, pairs_needed):
    """Fetch Q&A pairs for a given tag."""
    qa_pairs = []
    page = 1
    while len(qa_pairs) < pairs_needed:
        params = {
            "site": "stackoverflow",
            "tagged": tag,
            "key": API_KEY,
            "page": page,
            "pagesize": 100,
            "sort": "votes",
            "filter": "withbody"
        }
        try:
            response = requests.get(f"{BASE_URL}/questions", params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching questions for tag {tag}: {e}")
            break

        data = response.json()
        questions = data.get("items", [])
        if not questions:
            print(f"No more questions for tag {tag}")
            break

        for question in questions:
            if "accepted_answer_id" in question and len(qa_pairs) < pairs_needed:
                answer_params = {
                    "site": "stackoverflow",
                    "key": API_KEY,
                    "filter": "withbody"
                }
                try:
                    answer_response = requests.get(
                        f"{BASE_URL}/answers/{question['accepted_answer_id']}",
                        params=answer_params
                    )
                    answer_response.raise_for_status()
                    answer_data = answer_response.json()
                    answer = answer_data.get("items", [{}])[0]
                    if answer:
                        question_text = clean_text(question["title"] + " " + question.get("body", ""))
                        answer_text = clean_text(answer.get("body", ""))
                        qa_pairs.append({
                            "question": question_text,
                            "answer": answer_text
                        })
                except requests.RequestException as e:
                    print(f"Error fetching answer {question['accepted_answer_id']}: {e}")
                    continue

        print(f"Fetched {len(qa_pairs)}/{pairs_needed} pairs for tag {tag}")
        page += 1
        time.sleep(0.2)

        if data.get("quota_remaining", 0) < 100:
            print("Low quota remaining, stopping...")
            break

    return qa_pairs

def main():
    """Fetch Q&A pairs for all tags and save to JSON."""
    all_qa_pairs = []
    for tag, pairs_needed in TAGS:
        print(f"Fetching pairs for tag: {tag}")
        qa_pairs = fetch_qa_pairs(tag, pairs_needed)
        all_qa_pairs.extend(qa_pairs)
        print(f"Total pairs collected: {len(all_qa_pairs)}")

    # Save to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_qa_pairs, f, indent=2)
    print(f"Saved {len(all_qa_pairs)} Q&A pairs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()