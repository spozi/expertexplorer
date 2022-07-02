from flask import Flask, render_template, request
from scibert import SciBERT
import pandas as pd
import numpy as np
from scipy import spatial
from functools import reduce
from collections import OrderedDict


USER = "root"
PASSWORD = "mysqlpw"
HOST = "127.0.0.1"
PORT = '55000'
DATABASE = "publications_db"

from sqlalchemy import create_engine
from sqlalchemy.sql import text

eng_str = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (USER,PASSWORD,HOST,PORT,DATABASE)
engine = create_engine(eng_str)


app = Flask(__name__)

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DATABASE
app.config['MYSQL_PORT'] = PORT
# app.config['SECRET_KEY'] = 'something only you know'

scibert = SciBERT()

def similarity(a, b):
    return 1 - spatial.distance.cosine(a, b)

@app.route('/', methods=['POST', 'GET'])
def match():
    if request.method == "POST":
        searchquery = request.form['query']
        threshold = request.form['threshold']

        #1. Get all data from each table
        sql = [
            "SELECT * FROM publications_2018;",
            "SELECT * FROM publications_2019;",
            "SELECT * FROM publications_2020;",
            "SELECT * FROM publications_2021;"
        ]

        dfs = []
        with engine.connect().execution_options(autocommit=True) as conn:
            for cmd in sql:
                query = conn.execute(text(cmd))
                df = pd.DataFrame(query.fetchall())
                dfs.append(df)

        #2. Vectorize the query and compute the similarity
        searchqueryvector = scibert.vectorize(searchquery)
        for df in dfs:
            df['numpy_vector'] = df['scibert_vector'].apply(lambda x: np.fromstring(x[1:-1], sep=' '))
            df['similarity'] = df.apply(lambda x: similarity(x['numpy_vector'],searchqueryvector), axis=1)
    
        #3. Group into authors
        #  We are going to output ['photo','expert', 'expert score', 'total related publications', 'total publications' ]
        # ['author, 'year', 'title', 'similarity']

        #1. Set the expertise threshold >= 0.6
        #2. Compute the expertise yearly average similarity
        #3. Matching rate = the sum of yearly average similarity / year
        #4. Total related publications for whole time must be follow (1.)
        #5. Total publications for whole time

        #a. Get list of unique authors
        authors = []
        photos = []
        for df in dfs:
            authors += df['Authors'].tolist()
            photos += df['Photo'].tolist()   
        
        #Create a new dataframe author photo  
        df_author_photo = pd.DataFrame({'Authors': authors,
                   'Photos': photos})
        authors = list(set(authors)) #Extract unique authors

        df_author_photo = df_author_photo.drop_duplicates('Authors')
        df_author_photo = df_author_photo.set_index('Authors')
        author_photo_dict = df_author_photo.to_dict('index')

        #b. Compute the authors yearly average similarity
        df_year_similarity = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df.query(f"similarity > {threshold}") #Similarity must higher than 0.6
            df_g = df_g.filter(['Authors', 'similarity'])
            df_g = df_g.groupby('Authors')['similarity'].mean()
            df_year_similarity[year] = df_g

        #c. Count the related publications (count based on df_g $\in$ df_year)
        df_year_related_publications = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df.query(f"similarity > {threshold}") #Similarity must higher than 0.6
            df_g = df_g.filter(['Authors'])
            df_g = df_g.groupby(['Authors'])['Authors'].count()
            df_year_related_publications[year] = df_g

        #d. Store the related publications title
        df_year_related_titles_publications = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df.query(f"similarity > {threshold}") #Similarity must higher than 0.6
            df_g = df_g.filter(['Authors', 'Title'])
            df_g = df_g.groupby('Authors')['Title'].apply(list)
            df_year_related_titles_publications[year] = df_g

        #e. Count all publications
        df_year_all_publications = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df['Authors'].value_counts() #Return a series
            df_year_all_publications[year] = df_g

        records = []
        for author in authors:
            author_record = [{"name":author}]
            for year, df in df_year_similarity.items():
                if author in df:
                    author_record.append({f"average_similarity_{year}":df[author]})
            for year, df in df_year_related_publications.items():
                if author in df:
                    author_record.append({f"total_related_publications_{year}":df[author]})
            for year, df in df_year_all_publications.items():
                if author in df:
                    author_record.append({f"total_year_all_publications_{year}":df[author]})
            for year, df in df_year_related_titles_publications.items():
                if author in df:
                    author_record.append({f"title_publications_{year}":df[author]})
            if author in author_photo_dict:
                author_record.append(author_photo_dict[author])
            result_author_record = reduce(lambda a, b: {**a, **b}, author_record)
            records.append(result_author_record)
        
        #Merge a list of dicts to single dicts
        #The following codes should be refactored
        df_output = pd.DataFrame(records)
        df_output = df_output.fillna(0)
        if "average_similarity_2018" not in df_output:
            df_output["average_similarity_2018"] = 0
        if "average_similarity_2019" not in df_output:
            df_output["average_similarity_2019"] = 0
        if "average_similarity_2020" not in df_output:
            df_output["average_similarity_2020"] = 0
        if "average_similarity_2021" not in df_output:
            df_output["average_similarity_2021"] = 0
        df_output['Similarity_Score'] = df_output['average_similarity_2018'] + df_output['average_similarity_2019'] + df_output['average_similarity_2020'] + df_output['average_similarity_2021']
        
        if "total_related_publications_2018" not in df_output:
            df_output["total_related_publications_2018"] = 0
        if "total_related_publications_2019" not in df_output:
            df_output["total_related_publications_2019"] = 0
        if "total_related_publications_2020" not in df_output:
            df_output["total_related_publications_2020"] = 0
        if "total_related_publications_2021" not in df_output:
            df_output["total_related_publications_2021"] = 0
        df_output['Total_Related_Publications'] = df_output['total_related_publications_2018'] + df_output['total_related_publications_2019'] + df_output['total_related_publications_2020'] + df_output['total_related_publications_2021']
        
        df_output['Total_Publications'] = df_output['total_year_all_publications_2018'] + df_output['total_year_all_publications_2019'] + df_output['total_year_all_publications_2020'] + df_output['total_year_all_publications_2021']
        
        if "title_publications_2018" not in df_output:
            df_output["title_publications_2018"] = 0
        if "title_publications_2019" not in df_output:
            df_output["title_publications_2019"] = 0
        if "title_publications_2020" not in df_output:
            df_output["title_publications_2020"] = 0
        if "title_publications_2021" not in df_output:
            df_output["title_publications_2021"] = 0
        
        df_output['title_publications_2018'] = df_output['title_publications_2018'].apply(lambda x: [] if x == 0 else x)
        df_output['title_publications_2019'] = df_output['title_publications_2019'].apply(lambda x: [] if x == 0 else x)
        df_output['title_publications_2020'] = df_output['title_publications_2020'].apply(lambda x: [] if x == 0 else x)
        df_output['title_publications_2021'] = df_output['title_publications_2021'].apply(lambda x: [] if x == 0 else x)

        df_output['Related_Publications'] = df_output['title_publications_2018'] + df_output['title_publications_2019'] + df_output['title_publications_2020'] + df_output['title_publications_2021']    

        #change some of the columns datatype to int
        df_output = df_output.astype({"Total_Related_Publications": int}, errors='raise') 
        df_output = df_output.astype({"Total_Publications": int}, errors='raise') 

        
        df_output = df_output.set_index('name')
        df_output = df_output.sort_values(by='Similarity_Score', ascending=False)

        #Output dataframe to csv
        df_output.to_csv('sample.csv')

        #Output dataframe to flask
        data_dict = df_output.to_dict(orient='index', into=OrderedDict)
        return render_template("searchpage.html", output_data=data_dict)
    return render_template("searchpage.html", output_data={}) 


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host='0.0.0.0', port=80)