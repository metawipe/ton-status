import os 
import dotenv 

dotenv.load_dotenv() 

VK_API_KEY = os.getenv("VK_API_KEY") 
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
TON_API_URL = os.getenv("TON_API_URL")