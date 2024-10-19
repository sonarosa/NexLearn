# Install necessary libraries
!pip install PyMuPDF pytesseract pillow google-generativeai

import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF for PDF handling
import google.generativeai as genai

# Configure API key
GOOGLE_AI_API_KEY = 'API-KEY'  # Replace with your actual Google AI API key
genai.configure(api_key=GOOGLE_AI_API_KEY)

# Dictionary to store extracted text for each user
user_text_data = {}
unclear_topics = []  # List to store topics the user is unclear about

# OCR function using Tesseract
def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Extract text from PDF (PyMuPDF)
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

# Function to call Google Generative AI API to answer questions based on extracted text
def ask_google_ai_question(question, context_text):
    prompt = f"Context: {context_text}\n\nQuestion: {question}\nAnswer:"
    # Create GenerativeModel instance
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to call Google AI to generate a quiz question based on the topic
def ask_quiz_question(topic):
    prompt = f"Generate a quiz question about {topic}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to provide the correct answer and explanation if the user's answer is incorrect
def provide_solution_and_explanation(question):
    correct_answer_prompt = f"What is the correct answer to this question: {question}?"
    explanation_prompt = f"Provide an explanation for this question: {question}"

    model = genai.GenerativeModel('gemini-1.5-flash')

    correct_answer_response = model.generate_content(correct_answer_prompt)
    explanation_response = model.generate_content(explanation_prompt)

    return correct_answer_response.text, explanation_response.text

# Function to upload a file and extract text
def upload_and_extract():
    from google.colab import files
    uploaded = files.upload()  # Allow users to upload files
    for filename in uploaded.keys():
        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(filename)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            extracted_text = extract_text_from_image(filename)
        else:
            extracted_text = "Unsupported file type. Please upload a PDF or an image."

        # Store the extracted text
        if extracted_text:
            user_text_data[0] = extracted_text  # Use a single user ID for simplicity
            print("Text has been extracted from the document.")
        else:
            print("Failed to extract text. Please try again with a different file.")

# Start chatting
def chat():
    print("Welcome to the Chatbot! Type 'exit' to stop chatting.")
    while True:
        if not user_text_data:
            print("Please upload a document or image first to extract text.")
            upload_and_extract()

        user_message = input("You: ")
        if user_message.lower() == 'exit':
            print("Goodbye!")
            break

        context_text = user_text_data.get(0, "")
        if context_text:
            answer = ask_google_ai_question(user_message, context_text)
            print(f"Bot: {answer}")

            # Check if the user is unclear on a particular topic
            if 'unclear' in user_message or 'not sure' in user_message:
                topic = input("Bot: What topic are you unclear about? ")
                unclear_topics.append(topic)
                print(f"Bot: I've noted that you're unclear about {topic}. Let's quiz you on this.")

                # Ask a quiz question based on the unclear topic
                quiz_question = ask_quiz_question(topic)
                print(f"Bot: {quiz_question}")

                user_answer = input("Your answer: ")
                if "correct" in user_answer.lower():  # Placeholder for real validation
                    print("Bot: That's correct! Here's one more question.")
                    second_question = ask_quiz_question(topic)
                    print(f"Bot: {second_question}")
                    user_answer = input("Your answer: ")
                    print("Bot: Great job! We're done for now.")
                else:
                    # If the answer is incorrect, provide the solution and explanation
                    print("Bot: That's not correct. Let me help you with this topic.")
                    correct_answer, explanation = provide_solution_and_explanation(quiz_question)
                    print(f"Bot: The correct answer is: {correct_answer}")
                    print(f"Bot: Here's the explanation: {explanation}")

                    # Ask the user if they understood
                    understood = input("Bot: Did you understand the explanation? (yes/no): ").lower()
                    if understood == 'yes':
                        print("Bot: Great! Feel free to ask more doubts if you have any.")
                    else:
                        # If the user is still unclear, prompt further clarification
                        unclear_prompt = input("Bot: Please type 'not clear on <topic name>' to ask further questions: ")
                        if 'not clear on' in unclear_prompt.lower():
                            topic_name = unclear_prompt.split('on')[1].strip()
                            unclear_topics.append(topic_name)
                            print(f"Bot: Let's go over {topic_name} again.")
                            additional_quiz_question = ask_quiz_question(topic_name)
                            print(f"Bot: {additional_quiz_question}")
                            user_answer = input("Your answer: ")
                            if "correct" in user_answer.lower():
                                print("Bot: Great, you've understood it this time!")
                            else:
                                correct_answer, explanation = provide_solution_and_explanation(additional_quiz_question)
                                print(f"Bot: The correct answer is: {correct_answer}")
                                print(f"Bot: Here's the explanation: {explanation}")
        else:
            print("No context available. Please upload a document or image first.")

# Run the chat function
chat()
