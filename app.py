from flask import Flask, render_template, request, url_for
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from function import clean_text

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation

app = Flask(__name__)

df = pd.read_csv('./model/prog_book.csv')

df['clean_Book_title']=df['Book_title'].apply(clean_text)
df['clean_Description']=df['Description'].apply(clean_text)

# Initializing vectorizer
vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)

# Applying vectorized to clean text
X = vectorizer.fit_transform(df['clean_Book_title'])

# Getting array with vectorized titles
title_vectors = X.toarray()

desc_vectorizer = TfidfVectorizer(analyzer='word', lowercase=False)
Y = desc_vectorizer.fit_transform(df['clean_Description'])
desc_vectors = Y.toarray()

def get_recommendations(value_of_element, feature_locate, df, vectors_array, feature_show):
    """Returns DataFrame with particular feature of target and the same feature of five objects similar to it.

    value_of_element     - unique value of target object
    feature_locate       - name of the feature which this unique value belongs to
    df                   - DataFrame with feautures
    vectors_array        - array of vectorized text used to find similarity
    feature_show         - feature that will be shown in final DataFrame
    """

    # Locating target element by its specific value
    index_of_element = df[df[feature_locate]==value_of_element].index.values[0]

    # Finding its value to show
    show_value_of_element = df.iloc[index_of_element][feature_show]

    # Dropping target element from df
    df_without = df.drop(index_of_element).reset_index().drop(['index'], axis=1)

    # Dropping target element from vectors array
    vectors_array = list(vectors_array)
    target = vectors_array.pop(index_of_element).reshape(1,-1)
    vectors_array = np.array(vectors_array)

    # Finding cosine similarity between vectors
    most_similar_sklearn = cosine_similarity(target, vectors_array)[0]

    # Sorting coefs in desc order
    idx = (-most_similar_sklearn).argsort()

    # Finding features of similar objects by index
    all_values = df_without[[feature_show]]
    for index in idx:
      simular = all_values.values[idx]

    recommendations_df = pd.DataFrame({feature_show: show_value_of_element,
                                    "rec_1": simular[0][0],
                                    "rec_2": simular[1][0],
                                    "rec_3": simular[2][0],
                                    "rec_4": simular[3][0],
                                    "rec_5": simular[4][0],
                                    "rec_6": simular[5][0],
                                    "rec_7": simular[6][0],
                                    "rec_8": simular[7][0],
                                    "rec_9": simular[8][0],
                                    "rec_10": simular[9][0]}, index=[0])


    return recommendations_df

@app.route('/', methods=['GET', 'POST'])
def main():
   book_titles = df['Book_title'].tolist()

   if request.method == 'GET':
      return render_template('index.html', book_titles=book_titles)
   
   if request.method == 'POST':
      book = request.form['book_name']

      result = get_recommendations(book, 'Book_title', df, title_vectors, 'Book_title')
      result_dict = result.to_dict(orient='records')[0]
      return render_template('index.html', result_dict=result_dict, book_titles=book_titles)

if __name__ == '__main__':
    app.run(debug=True)
