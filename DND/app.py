from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

CORS(app)

quests = [
    {"id": 1, "title": "Rescue the Lost Treasure", "description": "Help the villagers find their lost treasure hidden in the dark cave."},
    {"id": 2, "title": "Defeat the Goblin King", "description": "The Goblin King has been terrorizing the countryside. Gather your team to defeat him."},
    {"id": 3, "title": "Retrieve the Ancient Scroll", "description": "An ancient scroll containing powerful spells is lost in the library of the old wizard."},
]

options = [
    {"action": "Attack", "description": "Engage in combat."},
    {"action": "Talk", "description": "Attempt to negotiate."},
    {"action": "Explore", "description": "Look around for clues."},
]

@app.route('/quests', methods=['GET'])
def get_quests():
    return jsonify(random.sample(quests, min(2, len(quests)))), 200

@app.route('/options', methods=['GET'])
def get_options():
    return jsonify(options), 200

if __name__ == '__main__':
    app.run(debug=True)
