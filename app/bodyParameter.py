def get(response_data,value):
    if value in response_data:
        return response_data[value]
    else:
        return None