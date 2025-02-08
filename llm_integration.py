from transformers import pipeline

def parse_user_input(user_input):
    """
    Use a pre-trained model for text classification.
    """
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = ["work-related", "entertainment"]
    result = classifier(user_input, candidate_labels)
    print("\nDetected intent and label scores:", result)
    return result

def analyze_screen_content_with_llm(text, intent):
    """
    Analyze screen content with an LLM to classify as work-related or entertainment.
    """

    trunctated_text = text[:200]
    generator = pipeline("text-generation", model="gpt2")

    prompt = (
        f"The user intends: '{intent}'. "
        f"Detected screen content: '{trunctated_text}'. "
        f"Is this content work-related or entertainment? Please answer clearly."
    )

    print("\nAnalyzing with LLM...")
    result = generator(prompt, max_new_tokens=50, num_return_sequences=1, truncation=True)
    return result[0]['generated_text']
