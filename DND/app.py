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
playerName = None
playerSpecies = None
playerJob = None

@app.route("/generate_story", methods=["POST"])
def generate_story():
    # Check if the request contains the required files and JSON data
    """
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
    document_content = document_file.read() """

    document = "The first clear expression of nationalism came withthe French Revolution in 1789. France, as youwould remember, was a full-fledged territorial statein 1789 under the rule of an absolute monarch.The political and constitutional changes that camein the wake of the French Revolution led to thetransfer of sovereignty from the monarchy to abody of French citizens. The revolution proclaimedthat it was the people who would henceforthconstitute the nation and shape its destiny.From the very beginning, the French revolutionariesintroduced various measures and practices thatcould create a sense of collective identity amongstthe French people. The ideas of la patrie (thefatherland) and le citoyen (the citizen) emphasisedthe notion of a united community enjoying equal rights under aconstitution. A new French flag, the tricolour, was chosen to replacethe former royal standard. The Estates General was elected by thebody of active citizens and renamed the National Assembly. Newhymns were composed, oaths taken and martyrs commemorated,all in the name of the nation. A centralised administrative systemwas put in place and it formulated uniform laws for all citizenswithin its territory. Internal customs duties and dues were abolishedand a uniform system of weights and measures was adopted.Regional dialects were discouraged and French, as it was spokenand written in Paris, became the common language of the nation.The revolutionaries further declared that it was the mission and thedestiny of the French nation to liberate the peoples of Europefrom despotism, in other words to help other peoples of Europeto become nations.When the news of the events in France reached the different citiesof Europe, students and other members of educated middle classesbegan setting up Jacobin clubs. Their activities and campaignsprepared the way for the French armies which moved into Holland,Belgium, Switzerland and much of Italy in the 1790s. With theoutbreak of the revolutionary wars, the French armies began tocarry the idea of nationalism abroad."
    playerName = 'William'
    playerSpecies = 'human male'
    playerJob = 'gun man'
    gamePrompt = f"""
You are tasked with creating a gamified learning platform inspired by Dungeons and Dragons. Unlike D&D it doesn;t have to be always medievel themed. Your role is to generate an immersive story, random encounters, and dynamic questlines, along with rewards and penalties to enhance the learning experience. A document will be provided, and the entire story should be based on that. The document covers a subject or a part of it. Make sure the story has flow in it.

Player Information:
- Player Name: {playerName}
- Player Species: {playerSpecies} (e.g., human, elf, dwarf, orc)
- Player Class/Job: {playerJob} (e.g., wizard, warrior, rogue)

Story Requirements, use these exact key words and no additional information and Make it a key-value pairs:
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
- If a document ({document}) is provided, integrate its content meaningfully into the story progression or player tasks.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": gamePrompt}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        storyResponse = response.json()
        # return storyResponse
        storyElements = extractStoryElements(storyResponse)
        return jsonify(storyElements)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def extractStoryElements(storyResponse):
    """ Extracts title, description, options, and conversations from the story response. """
    content     = storyResponse["candidates"][0]["content"]["parts"][0]["text"]
    
    title       = extractTitle(content)
    description = extractDescription(content)
    dialogues   = extractConversations(content)
    options     = extractOptions(content)

    return {
        "title": title,
        "description": description,
        "dialogues": dialogues,
        "options": options,
    }


def extractTitle(content):
    start   = content.find("**Title:**") + len("**Title:**")
    end     = content.find("\n2", start)
    Title   = content[start:end].strip()
    return Title

def extractDescription(content):
    start       = content.find("**Story Overview:**") + len("**Story Overview:**")
    end         = content.find("\n3.", start)
    description =  content[start:end].strip()
    return description

def extractConversations(content):
    dialogues = content.find("**Dialogues:**") + len("**Dialogues:**")
    end = content.find("\n4.", dialogues)
    dialoguesSections = content[dialogues:end].strip()
    dialogues = [dia.strip() for dia in dialoguesSections.split("\\n") if dia]
    return dialogues

def extractOptions(content):
    start = content.find("**Options for Players:**") + len("**Options for Players:**")
    end = content.find("\n5.", start)
    optionsSections = content[start:end].strip()
    options = [opt.strip() for opt in optionsSections.split("\\n") if opt]
    return options

@app.route("/player_input", methods=["POST"])
def playerInput():
    #action = request.json.get('action') 
    #roll = request.json.get('roll', {})  

    action = "Support the King and the old order, defend the established system, and learn about the perspective of the aristocracy."
    roll = 12

    result = processAction(action, roll)

    return jsonify(result)

def processAction( action, roll):
    """ Process the player's action and update the story based on their choice. """
    response = continueStory(action, roll)
    storyElements = extractStoryElements(response)
    return storyElements

def continueStory(action, roll):
    """ Placeholder function to generate a new story based on the player's chosen action. """
    prompt = f"The player chose the action: {action}. Player Name: {playerName}, Species: {playerSpecies}, Job: {playerJob}. with a dice roll of {roll}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
    response.raise_for_status() 

    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
