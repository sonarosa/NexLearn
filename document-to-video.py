from google.colab import drive
drive.mount('/content/drive')
!pip install PyMuPDF pytesseract pillow google-generativeai
!pip install gTTS gtts
from gtts import gTTS
import gtts
import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDF handling
import google.generativeai as genai

GOOGLE_AI_API_KEY = # Replace with your actual Google AI API key
genai.configure(api_key=GOOGLE_AI_API_KEY)
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"
# Function to call Google Generative AI API to generate a script
def ask_google_ai_for_script(context_text, video_duration):
    question = f"Create a speech for a teacher based on the following content for a video that is {video_duration} seconds long without any images or visuals just by word explanation."
    prompt = f"Context: {context_text}\n\nQuestion: {question}\nAnswer:"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
def convert_text_to_speech(script_text, output_audio_path):
    try:
        # Convert text to speech
        tts = gtts.gTTS(script_text)
        
        # Save the audio file
        tts.save(output_audio_path)
        print(f"Audio saved at {output_audio_path}")
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
def main(pdf_path, output_audio_path):
    # Step 1: Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    if "Error" in extracted_text:
        print(extracted_text)
        return
    
    # Step 2: Ask the user for the video duration
    video_duration = input("How long should the video be (in seconds)? ")
    
    # Step 3: Generate the script using Google Generative AI
    script = ask_google_ai_for_script(extracted_text, video_duration)
    print("Generated script:\n", script)
    
    # Step 4: Convert the generated script into speech (audio)
    convert_text_to_speech(script, output_audio_path)
    
    print("Process completed!")
pdf_path = "/content/Photosynthesis.pdf"
output_audio_path = "generated_video_audio.mp3"

# Call the main function
main(pdf_path, output_audio_path)
import requests

video_url = "https://drive.google.com/uc?export=download&id=1Qu7Scy7x3KvwVjOD5oZ9efUfE0l7uJGI"
audio_url = "https://drive.google.com/uc?export=download&id=1byJuBJaThz8z9I89Vd_KkZHNfPOJHG3y"

url = "https://api.sync.so/v2/generate"

payload = {
    "model": "lipsync-1.7.1",
    "input": [
        {
            "type": "video",
            "url": video_url
        },
        {
            "type": "audio",
            "url": audio_url
        }
    ],
    "options": {"output_format": "mp4"},
    "webhookUrl": "https://your-server.com/webhook"
}

headers = {
    "x-api-key": "key",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)
import time
import requests

# Job ID from the initial response
job_id = "id"

# Endpoint to check the status
url = f"https://api.sync.so/v2/generate/{job_id}"

# API headers
headers = {
    "x-api-key": "key",
    "Content-Type": "application/json"
}

# Function to poll and check the job status
def check_job_status():
    while True:
        response = requests.get(url, headers=headers)
        result = response.json()

        status = result.get("status")
        if status == "COMPLETED":
            print(f"Job completed! You can download the video here: {result.get('outputUrl')}")
            break
        elif status == "FAILED":
            print(f"Job failed with error: {result.get('error')}")
            break
        else:
            print(f"Job status: {status}. Retrying in 10 seconds...")

        time.sleep(10)  # Wait for 10 seconds before checking again

# Call the function to start polling
check_job_status()
