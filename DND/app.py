import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '849481498'
CORS(app)
load_dotenv()
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")
genai.configure(api_key = API_KEY)

# In-memory store for current game session data
model = genai.GenerativeModel(
    model_name= "gemini-1.5-flash" , 
    system_instruction = f"You are tasked with creating a gamified learning platform inspired by Dungeons and Dragons. Unlike D&D it doesn't have to be always medievel themed. Your role is to generate an immersive story, random encounters, and dynamic questlines, along with rewards and penalties to enhance the learning experience. A document is provided, and the entire story should be based on that. The document covers a subject or a part of it. The response should be in the format {{title:str,storyOverview:str(),options:list(str()),experience:int,health:int}}, options are the options given to players. 'health' is the health of player after the story and experience is the experience gained after the story. after recieving players choice, generate the new story."
    )

@app.route("/generate_story", methods=["POST"])
def generate_story():
    playerName = request.args.get('name')
    playerSpecies = request.args.get('species')
    playerJob = request.args.get('')
    session['name'] = playerName
    session['species'] = playerSpecies
    session['job'] = playerJob

    document = "The first clear expression of nationalism came withthe French Revolution in 1789. France, as you would remember, was a full-fledged territorial statein 1789 under the rule of an absolute monarch.The political and constitutional changes that camein the wake of the French Revolution led to thetransfer of sovereignty from the monarchy to abody of French citizens. The revolution proclaimedthat it was the people who would henceforthconstitute the nation and shape its destiny.From the very beginning, the French revolutionariesintroduced various measures and practices thatcould create a sense of collective identity amongstthe French people. The ideas of la patrie (thefatherland) and le citoyen (the citizen) emphasisedthe notion of a united community enjoying equal rights under aconstitution. A new French flag, the tricolour, was chosen to replacethe former royal standard. The Estates General was elected by thebody of active citizens and renamed the National Assembly. Newhymns were composed, oaths taken and martyrs commemorated,all in the name of the nation. A centralised administrative systemwas put in place and it formulated uniform laws for all citizenswithin its territory. Internal customs duties and dues were abolishedand a uniform system of weights and measures was adopted.Regional dialects were discouraged and French, as it was spokenand written in Paris, became the common language of the nation.The revolutionaries further declared that it was the mission and thedestiny of the French nation to liberate the peoples of Europefrom despotism, in other words to help other peoples of Europeto become nations.When the news of the events in France reached the different citiesof Europe, students and other members of educated middle classesbegan setting up Jacobin clubs. Their activities and campaignsprepared the way for the French armies which moved into Holland,Belgium, Switzerland and much of Italy in the 1790s. With theoutbreak of the revolutionary wars, the French armies began tocarry the idea of nationalism abroad."
    global model
    response = model.generate_content(f"This is the document {document}, player Information->name:{playerName}species:{playerSpecies}job:{playerJob}. Create the inital story") 
    response = str(response.text)
    response = response.replace('\\"', '"').replace('\\n', '\n').strip('```json\n').strip('```')
    return response


@app.route("/player_input", methods=["POST"])
def playerInput():
    #action = request.json.get('action') 
    #roll = request.json.get('roll', {})  

    action = "Remain in Paris and observe the unfolding events."
    roll = 12

    response = continueStory(action, roll)

    return response

def continueStory(action, roll):
    """ Placeholder function to generate a new story based on the player's chosen action. """
    playerName = session.get('name')
    playerSpecies = session.get('species')
    playerJob = session.get('job')
    prompt = f"The player chose the action: {action}. Player Name: {playerName}, Species: {playerSpecies}, Job: {playerJob}. with a dice roll of {roll}"
    response = model.generate_content(prompt) 
    response = str(response.text)
    response = response.replace('\\"', '"').replace('\\n', '\n').strip('```json\n').strip('```')
    return response
    
if __name__ == "__main__":
    app.run(debug=True)
