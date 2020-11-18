def validate_data(data):
    if data:
        return data.find('div', {'class': 'fieldBody'}).text
    else:
        return ''
