import time
import pytesseract
from PIL import ImageGrab
from plyer import notification
from content_classifier import classify_content
import csv
import os
import datetime

LOG_FILE = "activity_log.csv"


def log_activity(event_type, content, warning=None):
    """
    Logs user activities, detections, and warnings.
    """
    with open(LOG_FILE, mode="a", newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, event_type, content, warning or "None"])
        print(f"Logged event: {event_type} | Content: {content} | Warning: {warning or 'None'}")

def delete_logs():
    """
    Deletes the log file if it exists.
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("All logs have been deleted.")
    else:
        print("No logs to delete.")

def capture_and_analyze(interval=5):
    """
    Continuously capture and analyze screenshots until interrupted.
    Saves screenshots, handles errors, and provides text extraction.
    """
    screenshot_count = 0
    extracted_texts = []

    try:
        while True:
            print(f"Capturing screenshot {screenshot_count + 1}...")

            # Capture and save the screenshot
            screenshot = ImageGrab.grab()
            image_path = f"screenshot_{screenshot_count}.png"
            screenshot.save(image_path)
            print(f"Screenshot saved as {image_path}.")

            # Text extraction with error handling
            text_detected = pytesseract.image_to_string(screenshot).strip()
            if text_detected:
                extracted_texts.append(text_detected)
                print(f"Detected text in screenshot {screenshot_count}: {text_detected}")
            else:
                print(f"No text detected in screenshot {screenshot_count}.")

            # Example notification logic
            if "restricted" in text_detected.lower():
                send_notification("Alert!", "Detected restricted content!")

            screenshot_count += 1
            time.sleep(interval)  # Wait for the interval

    except KeyboardInterrupt:
        print("\nUser interrupted the process. Exiting...")
    
    return extracted_texts if extracted_texts else ["No content detected"]


def send_notification(title, message):
    """
    Display desktop notifications.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except Exception as e:
        print(f"Notification error: {e}")

def analyze_screenshot(text):
    """Analyze screenshot text and send notifications."""
    category = classify_content(text)

    # Hard-coded detection for specific applications
    if "Chrome" in text or "Browser" in text:
        detected_app = "browser"
    elif "Visual Studio Code" in text or "vscode" in text:
        detected_app = "vscode"
    else:
        detected_app = "unknown"

    # Alert if there's a mismatch
    if detected_app != "vscode":  # Assume user should stay in vscode
        send_notification("App Switch Alert", f"Using '{detected_app}' instead of 'vscode'")
    print(f"Detected Category: {category}")


if __name__ == "__main__":
    print("Starting screen capture. Press Ctrl+C to stop.")
    capture_and_analyze(interval=5)


