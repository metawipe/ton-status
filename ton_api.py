import requests from config 
import TON_API_URL from utils 
import make_number 

def get_ton_data(): 
    try: 
        response = requests.get(TON_API_URL, timeout=5) 
        response.raise_for_status() 
        
        data = response.json()["rates"]["TON"] 
        data["prices"]["USD"] = make_number( data["prices"]["USD"] ) 
        data["prices"]["RUB"] = make_number( data["prices"]["RUB"] ) 
        data["diff_24h"]["USD"] = make_number( data["diff_24h"]["USD"] ) 
        data["diff_7d"]["USD"] = make_number( data["diff_7d"]["USD"] ) 
        
        return data 
    except (requests.RequestException, KeyError, ValueError): 
        return None