def classify_content(text):
    work_keywords = ["IDE", "terminal", "debug", "code", "project", "Vscode"]
    entertainment_keywords = ["YouTube", "Netflix", "game", "social"]

    if any(word.lower() in text.lower() for word in work_keywords):
        return "Work-Related"
    elif any(word.lower() in text.lower() for word in entertainment_keywords):
        return "Entertainment"
    else:
        return "Unclassified"
