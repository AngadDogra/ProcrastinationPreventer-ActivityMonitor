from transformers import pipeline
from screen_capture import capture_and_analyze, send_notification, analyze_screenshot, delete_logs
from llm_integration import parse_user_input, analyze_screen_content_with_llm
from plyer import notification
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def collect_user_input():
    """
    Collect user input about intended activities.
    """
    print("What are your intended activities?")
    return input("E.g., 'I'll work with my coding editor and browser': ")

def format_extracted_text(text, screenshot_number, label):
    """
    Format and print extracted text for better readability.
    """
    print(f"\n===== Screenshot {screenshot_number + 1} =====")
    print(f"Activity Detected: {label.capitalize()}")
    print("Extracted Text:")
    print("---------------------------")
    print(text.strip() if text else "No text detected")
    print("===========================\n")


def check_and_notify(intent, screen_activity_label):
    """
    Compare intent and detected activity, then notify if there's a mismatch.
    """
    if intent != screen_activity_label:
        warning_message = f"Detected activity '{screen_activity_label}' does not match intended activity '{intent}'!"
        send_notification("Activity Mismatch Warning", warning_message)
        print(warning_message)
    else:
        print("No deviations detected.")


# Main execution
user_input = collect_user_input()
activity_details = parse_user_input(user_input)

# Capture screenshots and analyze
extracted_texts = capture_and_analyze(interval=5)  # Assume it returns list of image paths/text

for i, text in enumerate(extracted_texts):
    label = activity_details['labels'][i] if i < len(activity_details['labels']) else "Unknown"
    format_extracted_text(text, i, label)

    analyze_screenshot(text)

    llm_response = analyze_screen_content_with_llm(text, user_input)
    print(f"LLM Analysis Result: {llm_response}")

    check_and_notify(user_input, label)
