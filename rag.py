!pip install pdf2image pytesseract
!apt-get install poppler-utils
!sudo apt install tesseract-ocr
!pip install pytesseract
!pip install PyMuPDF
!pip install camelot-py
!pip install pinecone-client
!pip install google-generativeai
!pip install sentence-transformers

import os
from pdf2image import convert_from_path
import pytesseract
from google.colab import files
import shutil
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

output_dir = '/content/output_folder'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Output folder created at: {output_dir}")

uploaded = files.upload()
for filename in uploaded.keys():
    shutil.move(filename, output_dir)

print(f"File(s) uploaded and moved to {output_dir}")

def convert_pdf_to_images(pdf_path, output_folder):
    file_name = os.path.basename(pdf_path)
    file_name_no_extension = os.path.splitext(file_name)[0]
    images = convert_from_path(pdf_path, output_folder=output_folder, fmt='png')
    if len(images) == 1:
        image_path = os.path.join(output_folder, f"{file_name_no_extension}_page_1.png")
        images[0].save(image_path, "PNG")
        return [image_path]
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"{file_name_no_extension}_page_{i+1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

def extract_text_from_image(image_path):
    if os.path.exists(image_path):
        return pytesseract.image_to_string(image_path)
    else:
        print(f"Error: File not found at path: {image_path}")
        return ""

pdf_file_name = list(uploaded.keys())[0]
pdf_file_path = os.path.join(output_dir, pdf_file_name)
image_paths = convert_pdf_to_images(pdf_file_path, output_dir)

all_text = ""
for image_path in image_paths:
    text = extract_text_from_image(image_path)
    all_text += text + "\n"

pc = Pinecone(api_key="#api-key")
index_name = "quickstart"

pc.create_index(
    name=index_name,
    dimension=2,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

genai.configure(api_key="#api-key")

def ask_google_ai_question(question, context_text):
    prompt = f"Context: {context_text}\n\nQuestion: {question}\nAnswer:"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def chat():
    print("Welcome to the Chatbot! Type 'exit' to stop chatting.")
    context_text = all_text
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit' or user_message.lower() == 'quit':
            print("Goodbye!")
            break
        if context_text:
            answer = ask_google_ai_question(user_message, context_text)
            print(f"Bot: {answer}")
        else:
            print("No context available to answer your question.")

chat()
