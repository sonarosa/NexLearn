import os
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
load_dotenv()
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# In-memory store for current game session data
current_game_data = {}

@app.route("/generate_story", methods=["POST"])
def generate_story():
    # Check if the request contains the required files and JSON data

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    if 'document' not in request.files:
        return jsonify({'error': 'Document file is required'}), 400

    

    # Get the document (PDF file)
    document_file = request.files['document']
    
    # Ensure the file is a PDF
    if document_file.filename == '' or not document_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Only PDF files are accepted.'}), 400
    
    playerName = request.json.get('player_name', 'Unknown')
    playerSpecies = request.json.get('player_species', 'Human')
    playerJob = request.json.get('player_job', 'Warrior')

    # Read the PDF file content
    document_content = document_file.read() 

    input_text = f"""
You are tasked with creating a gamified learning platform inspired by Dungeons and Dragons. Your role is to generate an immersive story, random encounters, and dynamic questlines, along with rewards and penalties to enhance the learning experience. A document will be provided, and the entire story should be based on that. The document covers a subject or a part of it. Make sure the story has flow in it.

Player Information:
- Player Name: {playerName}
- Player Species: {playerSpecies} (e.g., human, elf, dwarf, orc)
- Player Class/Job: {playerJob} (e.g., wizard, warrior, rogue)

Story Requirements, and Make it a key-value pairs:
1. Title: Generate a creative and engaging title for the player’s adventure.
2. Story Overview: Summarize the player’s quest, their objectives, and the world they are exploring.
3. Dialogues: Create conversations between the player and NPCs, presenting choices that can affect the player’s journey.
4. Options for Players: Create various options for players that they can take.
5. Attribute Check: Just like in real DND, there should be events that require certain stats to be higher than a threshold. Successful attribute checks may give additional rewards.

Player Stats:
- Vitality
- Attack
- Resistance
- Mana
- Wisdom
- Agility
- Charisma
- Stealth

Game Mechanics:
1. Random Encounters:
   - Create random encounters with enemies during the player’s journey.
   - Each encounter should include:
     - Enemy Type (species and job)
     - Stats: Vitality, Attack, Resistance, and Agility
     - Level or Difficulty

2. Player Choices:
   - For each situation or encounter, provide options that the player can take as key-value pairs:
   - When the player option is provided, generate the possible result and produce the next story.

Rewards & Penalties:
1. Quest Rewards: Define the rewards (e.g., experience points, skills, items) for completing quests successfully.
2. Failure Penalties: Specify penalties (e.g., losing health, reducing experience points) for failing quests or losing battles.

Document Integration:
- If a document ({document_content}) is provided, integrate its content meaningfully into the story progression or player tasks.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": input_text}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Make the API call
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        story_response = response.json()

        # Extract relevant information from the story_response
        structured_data = extract_story_elements(story_response)

        # Store the structured data in the current game session
        current_game_data[playerName] = structured_data

        return jsonify(structured_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

def extract_story_elements(story_response):
    """
    Extracts title, description, options, and conversations from the story response.
    Adjust this function based on the actual response structure from the API.
    """
    generated_content = story_response.get("generatedContent", "")
    title = extract_title(generated_content)
    description = extract_description(generated_content)
    options = extract_options(generated_content)
    conversations = extract_conversations(generated_content)

    return {
        "title": title,
        "description": description,
        "options": options,
        "conversations": conversations,
    }

def extract_title(generated_content):
    return generated_content.split('\n')[1]  # Placeholder logic

def extract_description(generated_content):
    return generated_content.split('\n')[2:]  # Placeholder logic

def extract_options(generated_content):
    return ["Option 1", "Option 2"]  # Placeholder logic

def extract_conversations(generated_content):
    return ["Conversation 1", "Conversation 2"]  # Placeholder logic

@app.route("/player_input", methods=["POST"])
def player_input():
    player_name = request.json.get('player_name')
    action = request.json.get('action')  # The player's chosen action
    dice_rolls = request.json.get('dice_rolls', {})  # Dice rolls sent by the player

    if player_name not in current_game_data:
        return jsonify({'error': 'Player not found. Please generate a story first.'}), 404

    # Fetch the current game data for the player
    game_data = current_game_data[player_name]

    # Process the player's action and dice rolls (add your game logic here)
    result = process_player_action(game_data, action, dice_rolls)

    # Optionally, update the game state based on the player's action
    update_game_state(player_name, result)

    return jsonify(result)

def process_player_action(game_data, action, dice_rolls):
    # Example game logic to process the player's action
    # This should include your game mechanics for determining the outcome based on the action and dice rolls
    response = {
        "action": action,
        "outcome": "Action processed successfully",  # Placeholder outcome
        "game_data": game_data,  # Return the current game data
        "dice_rolls": dice_rolls  # Echo the received dice rolls
    }
    
    return response

def update_game_state(player_name, result):
    # Update game state based on the result of the player's action
    pass  # Implement your game state management here

if __name__ == "__main__":
    app.run(debug=True)
