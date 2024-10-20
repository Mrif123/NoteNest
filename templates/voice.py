import cv2
import numpy as np
import speech_recognition as sr
import pyautogui
import time

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Function to recognize voice commands
def recognize_command():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for commands...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Adjust timeout and phrase limit
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Load a large image for scrolling
image = cv2.imread('picture1.jpg')  # Replace with the path to your large image

# Set initial scroll parameters
scroll_y = 0
scroll_step = 100  # Number of pixels to scroll with each command

# Function to scroll the image up and down
def scroll_image(command):
    global scroll_y

    # Define the window size (what's visible on screen)
    window_height = 500
    img_height = image.shape[0]

    if "scroll up" in command:
        scroll_y = max(0, scroll_y - scroll_step)  # Scroll up, but don't go above the image
    elif "scroll down" in command:
        scroll_y = min(img_height - window_height, scroll_y + scroll_step)  # Scroll down, but don't go past the image

    # Crop the image to the visible window area
    visible_img = image[scroll_y:scroll_y + window_height, :]

    # Display the visible portion of the image
    cv2.imshow("Image Scroll", visible_img)

# Main loop to display the image and listen for voice commands
while True:
    # Initially display the first section of the image
    visible_img = image[scroll_y:scroll_y + 500, :]
    cv2.imshow("Image Scroll", visible_img)

    # Listen for voice commands
    command = recognize_command()
    if command:
        scroll_image(command)
        if "exit" in command:
            print("Exiting...")
            break

    # Wait for 1 millisecond to detect any keypress, and close the window if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release any resources and close OpenCV windows
cv2.destroyAllWindows()