from datetime import datetime

def converter_AAAA_MM_DD(data):
    if data is None:
        return None
    return datetime.strptime(data, "%Y-%m-%d")