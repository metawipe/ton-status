import re 

HELP_TEXT = ( 'Команды:\n' '• Курс\n' '• Анализ\n' '• Конвертер\n\n' 'Для конвертации напиши:\n' '"10 TON"' ) 
ERROR_TEXT = "❌ Не удалось получить курс TON" 

def make_number(value) -> float: 
    value = str(value) 
    value = value.replace("%", "") 
    value = value.replace("−", "-") 
    
    return float(value) 

def get_ton_amount(text: str) -> float | None: 
    text = text.lower() 
    text = text.replace(",", ".") 
    text = text.replace("тон", "ton") 
    
    match = re.search(r"(\d+(?:\.\d+)?)\s*ton", text) 
    
    if not match: 
        return None 
    
    try: 
        amount = float(match.group(1)) 
    except ValueError: 
        return None 
    
    return amount if amount > 0 else None