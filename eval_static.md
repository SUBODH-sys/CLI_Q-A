# Static Evaluation
This evaluation compares the pre-trained TinyLlama-1.1B-Chat-v1.0 model's raw responses to ground truth CLI commands for five test prompts. The fine-tuned model produced empty outputs, so only pre-trained results are shown.

![alt text](image.png)

### Metrics:

Match Rate: 2/5 (40%) prompts contain the ground truth command in the raw response.
### Observations:
The pre-trained model generates verbose explanations or Python scripts, reducing CLI command precision.
Fine-tuning failure (empty outputs) limited evaluation to pre-trained model.