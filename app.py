from re import X
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

dataset = pickle.load(open('fix_wisata.pkl', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pkl', 'rb'))
dataset = dataset.reset_index()
idcs = pd.Series(dataset.index, index=dataset['Name '])

app = Flask(__name__)

@app.route('/', methods=['GET'])
def start():
    return(render_template('index.html'))

def recommend(Name ):
    index = idcs[Name ]
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    category_idcs = [i[0] for i in sim_scores]
    rec_categories = dataset['Category '].iloc[category_idcs]
    rec_wisata_names = dataset['Name '].iloc[category_idcs]
    rec_cities = dataset['City'].iloc[category_idcs]
    

    re_dataset = pd.DataFrame(columns=['Category ','Name ', 'City'])
    re_dataset['Category '] = rec_categories
    re_dataset['Name '] = rec_wisata_names
    re_dataset['City'] = rec_cities

    return re_dataset

@app.route('/', methods=['POST'])
def main():
    Name = request.form['Name']
    result_final = recommend(Name)
    rec_category = []
    rec_wisata_name = []
    rec_city = []
    for i in range(len(result_final)):
        rec_category.append(result_final.iloc[i][0])
        rec_wisata_name.append(result_final.iloc[i][1])
        rec_city.append(result_final.iloc[i][2])

    return render_template ('rekomendasi.html', category=rec_category, wisata_name=rec_wisata_name, city=rec_city, search=Name)

if __name__ == "__main__":
    app.run(debug=True)
