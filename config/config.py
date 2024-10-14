from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

# uri = "mongodb+srv://johndeo:123456pymongo@funtechs.kjb5dop.mongodb.net/?retryWrites=true&w=majority"
uri="mongodb+srv://pabbyvs:cI8g2HzjoEi4TaQN@cluster0.0wegy.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
db = client.ems 
blogs_collection = db["blogs"]
telemetries_collection = db["telemetries"]
projects_collection = db["projects"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
