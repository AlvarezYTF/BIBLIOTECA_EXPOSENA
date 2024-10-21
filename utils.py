# utils.py
import json

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

def truncar_texto(texto, longitud_max=25):
    return texto if len(texto) <= longitud_max else texto[:longitud_max-3] + '...'