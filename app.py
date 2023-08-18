from flask import Flask, render_template, request, url_for
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from function import clean_text, generate_google_search_link
from urllib.parse import quote

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation

app = Flask(__name__)

df = pd.read_csv('./model/clear_data.csv')

df['clean_Book_title']=df['Title'].apply(clean_text)
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
    similar_df = df_without.iloc[idx]

   #  recommendations_df = pd.DataFrame({feature_show: show_value_of_element,
   #                                  "rec_1": simular[0][0],
   #                                  "rec_2": simular[1][0],
   #                                  "rec_3": simular[2][0],
   #                                  "rec_4": simular[3][0],
   #                                  "rec_5": simular[4][0]}, index=[0])
    
    recommendations_df = pd.DataFrame({
        "Title": similar_df['Title'].values[:5],
        "Author": similar_df['Authors'].values[:5],
        "Description": similar_df['Description'].values[:5],  # Get top 5 similar descriptions
        "ImageLink": similar_df['ImageLink'].values[:5]  # Get top 5 similar imagelinks
    })

    return recommendations_df

@app.template_filter('search_link')
def generate_google_search_link(title):
        # Membuat URL dasar Google Search
        google_search_base_url = "https://www.google.com/search?q="
        search_query = f"{title}"
        encoded_query = quote(search_query)
        return f"{google_search_base_url}{encoded_query}"

@app.route('/', methods=['GET', 'POST'])
def main():
   book_titles = df['Title'].tolist()

   if request.method == 'GET':
      result = None
      return render_template('index.html', book_titles=book_titles, result=result)
   
   if request.method == 'POST':
      book = request.form['book_name']

      result = get_recommendations(book, 'Title', df, desc_vectors, 'Title')
      # result_dict = result.to_dict(orient='records')[0]
      return render_template('index.html', result=result, book_titles=book_titles, book=book)
   
@app.route('/book_data')
def book_data():
    return render_template('book_data.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)
