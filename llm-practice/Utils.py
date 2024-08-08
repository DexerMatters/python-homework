from openai import OpenAI
import json

API_KEY = "sk-nAs5ILkcWdxhJFenOdZBJrlPuxFAazEKKL6Nv50u1g1GZ2BJ"
MODEL = "moonshot-v1-8k"
BASE_URL = "https://api.moonshot.cn/v1"

DATA_PATH = "./agents.json"

class Utils:

  data = []
  memory = []
  chosen_agent = None

  def __init__(self):
    self.data = json.loads(open(DATA_PATH, "r"))

  def save_data(self):
    f = open(DATA_PATH, "w")
    f.write(json.dumps(self.data))

  def findAgent(self, name):
    for agent in self.data:
      if agent["name"] == name:
        return agent
    return None

  def removeAgent(self, name):
    for agent in self.data:
      if agent["name"] == name:
        self.data.remove(agent)
  
  def addAgent(
      self, 
      name, 
      agent_description, 
      client_description,
      persona,
      temperature):
    self.data.append({
      "name": name,
      "agent_description": agent_description,
      "client_description": client_description,
      "persona": persona,
      "temperature": temperature
    })

  
def get_response(user_input, agent):
    
    system_prompt = f"""
    Your name:
    {agent["name"]}
    Your description: 
    {agent["agent_description"]}
    Your persona:
    {agent["persona"]}
    Client description:
    {agent["client_description"]}
    """

    client = OpenAI(
        api_key = API_KEY,
        base_url = BASE_URL
    )

    completion = client.chat.completions.create(
        model = MODEL,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature = agent["temperature"]
    )
 
    return completion.choices[0].message.content