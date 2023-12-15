from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import os

app = Flask(__name__)

def convert_percentage(value):
    if isinstance(value, str):
        return float(value.strip('%')) / 100
    return value

def process_data(data_champion):
    percentage_columns = ['Win %', 'Role %', 'Pick %', 'Ban %']
    for col in percentage_columns:
        data_champion[col] = data_champion[col].apply(convert_percentage)

    data_champion['Combined Score'] = data_champion['Win %'] * data_champion['Pick %']

    roles = ['TOP', 'JUNGLE', 'MID', 'ADC', 'SUPPORT']
    top_3_per_role = {}
    for role in roles:
        top_3_champions = data_champion[data_champion['Role'] == role].sort_values(by='Combined Score', ascending=False).head(3)
        champions_data = []
        for _, row in top_3_champions.iterrows():
            champion_name = row['Name']
            image_path = f'static/tiles/{champion_name}_0.jpg'  # Construire le chemin de l'image
            champion_info = row.to_dict()
            champion_info['ImagePath'] = image_path
            champions_data.append(champion_info)
        top_3_per_role[role] = champions_data

    return top_3_per_role

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['csvFile']
    if not file:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    data_champion = pd.read_csv(file, sep=';')
    print(data_champion.columns)
    if 'Win %' not in data_champion.columns:
        return jsonify({"error": "La colonne 'Win %' n'est pas présente dans le fichier CSV."}), 400

    result = process_data(data_champion)
    return jsonify(result)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
