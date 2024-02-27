import re

def extract_dates(string):
    pattern = r"Posted (\d{2}\.\d{2}\.\d{4})(?:Renewed (\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}))?"
    matches = re.search(pattern, string)
    
    if matches:
        creating_date = matches.group(1)
        updating_date = matches.group(2)
        
        if updating_date is None:
            return {"creating": creating_date, "updating": None}
        else:
            return {"creating": creating_date, "updating": updating_date}
    
    return None