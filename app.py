from filecmp import DEFAULT_IGNORES
from flask import Flask, render_template, request, flash, send_file
from flask_mysqldb import MySQL
from flask_paginate import Pagination
from main import match_job
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import io
from mysql_manager import MySQLManager
from scibert import SciBERT
import pandas as pd
import numpy as np
from scipy import spatial
import json
from itertools import chain
from functools import reduce


USER = "syafiq"
PASSWORD = "syafiq123"
HOST = "127.0.0.1"
PORT = '3306'
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


# def prepare_result(query):
#     mysql_m = MySQLManager()
#     df_combined = match_job(query, scibert)
#     meanimage_list = []
#     varimage_list = []
#     for index in df_combined.index:
#         meanimage_list.append('image_base64("img_bytes"): ' + str(index))
#         varimage_list.append('image_base64("img_bytes"): ' + str(index))
#     global result
#     result = save_result(df_combined.copy(), meanimage_list, varimage_list)
#     mysql_m.delete_candidate()
#     for i in result.index:
#         record = {}
#         record["photo"] = result["Photo"][i]
#         record["author"] = result["Candidate"][i]
#         record["university"] = result["university"][i]
#         record["doc_count"] = str(result["Docs"][i])
#         record["avg_sim"] = str(result["AVG_SIM"][i])
#         record["mean"] = str(result["Average_Similarity"][i])
#         record["meanimage"] = result["Image(Avg)"][i]
#         record["var"] = str(result["Variance"][i])
#         record["varimage"] = result["Image(Var)"][i]
#         record["related_count"] = str(result["Related"][i])
#         mysql_m.insert_candidate(record)
#     print("Candidate data inserted", flush=True)
#     return True


# def save_result(df, mean_image_list, var_image_list):
#     mean_list = []
#     var_list = []
#     docs_list = []
#     avg_mean_list = []
#     related_list = []
#     for i in df.index:
#         mean_tuple = (df["mean_2018"][i], df["mean_2019"][i], df["mean_2020"][i], df["mean_2021"][i])
#         avg_mean = sum(mean_tuple) / len(mean_tuple)
#         avg_mean_list.append(avg_mean) 
#         mean_list.append(mean_tuple) 
#         var_list.append((df["var_2018"][i], df["var_2019"][i], df["var_2020"][i], df["var_2021"][i]))
#         docs_list.append(sum((df["docs_2018"][i], df["docs_2019"][i], df["docs_2020"][i], df["docs_2021"][i])))
#         related_list.append(sum((df["r_2018"][i], df["r_2020"][i], df["r_2021"][i])))
#     df.drop(["mean_2018", "mean_2019", "mean_2020", "mean_2021"], axis=1, inplace=True)
#     df.drop(["var_2018", "var_2019", "var_2020", "var_2021"], axis=1, inplace=True)
#     df.drop(["docs_2018", "docs_2019", "docs_2020", "docs_2021"], axis=1, inplace=True)
#     df.drop(["r_2018", "r_2020", "r_2021"], axis=1, inplace=True)
#     df.rename(columns={'photo': 'Photo'}, inplace=True)
#     df.rename(columns={'author': 'Candidate'}, inplace=True)
#     df["Average_Similarity"] = mean_list
#     df["Image(Avg)"] = mean_image_list
#     df["Variance"] = var_list
#     df["Image(Var)"] = var_image_list
#     df["Docs"] = docs_list
#     df["Related"] = related_list 
#     df["AVG_SIM"] = avg_mean_list
#     return df


# @app.route("/")
# def index():
#     return render_template("index.html")

# #search job and company
# @app.route('/expert', methods=['POST', 'GET'])
# def show1():
#     entries = 1000
#     limit = 1000
#     ts = 0.7
#     conn = mysql.connection
#     cursor = conn.cursor()
    
#     if request.method == "POST":
#         query = request.form['query']
#         if query != "":
#             isMatched = prepare_result(query)
#         if isMatched:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
#             conn.commit()
#             total = cursor.fetchall()
#             total_count = total[0][0]
#             message = ""
#             if total_count <= 0:
#                 message = "All author’s average similarity lower than 0.2"

#             page = request.args.get('page', 1, type=int)
#             offset = page * limit - limit
#             cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s", (limit, offset))
#             conn.commit()
#             dataa = cursor.fetchall()
#             #######################################################################
#             pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
#                                     css_framework='bootstrap3')
#             return render_template("searchpage.html", entries=entries, id=id, ts=ts,
#                                    dataa=dataa, pagination=pagination, message=message)

#     if request.method == 'GET':
#         message = ""
        
#         cursor.execute("SELECT COUNT(*) FROM candidate WHERE  Avg_sim > 0.2")
#         conn.commit()
#         total = cursor.fetchall()
#         total_count = total[0][0]
#         message = ""
#         if total_count <= 0:
#             message = "All author’s average similarity lower than 0.2"
        
#         page = request.args.get('page', 1, type=int)
#         offset = page * limit - limit
#         #####################################################################
#         cursor.execute("SELECT * from candidate WHERE Avg_sim > 0.2 LIMIT %s OFFSET %s ", (limit, offset))
#         conn.commit()
#         dataa = cursor.fetchall()

#         #######################################################################
#         pagination = Pagination(page=page, per_page=limit, offset=offset, total=total_count, record_name='user',
#                                 css_framework='bootstrap3')
#         return render_template("searchpage.html", entries=entries, id=id, ts=ts,
#                                dataa=dataa, pagination=pagination, message=message)

def similarity(a, b):
    return 1 - spatial.distance.cosine(a, b)

@app.route('/expert', methods=['POST', 'GET'])
def match():
    if request.method == "POST":
        searchquery = request.form['query']

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
        #  We are going to output ['photo','expert', 'matching rate', 'total related publications', 'total publications' ]
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
        # print(df_author_photo)
        # print(len(df_author_photo))

        #   print(authors)
        #b. Compute the authors yearly average similarity
        df_year_similarity = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df.query('similarity > .5') #Similarity must higher than 0.6
            df_g = df_g.filter(['Authors', 'similarity'])
            df_g = df_g.groupby('Authors')['similarity'].mean()
            df_year_similarity[year] = df_g

        #c. Count the related publications (count based on df_g $\in$ df_year)
        df_year_related_publications = {}
        for df in dfs:
            year = df['Year'].values[0]
            df_g = df.query('similarity > .5') #Similarity must higher than 0.6
            df_g = df_g.filter(['Authors'])
            df_g = df_g.groupby(['Authors'])['Authors'].count()
            df_year_related_publications[year] = df_g
        # print(df_year_related_publications)
        #d. Count all publications
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
            # if author in df_author_photo.index:
            #     print(author, ": True")
            #     author_record.append({"photo":df_author_photo[author]})
            # else:
            #     print(author, ": false")
            # # else:
            # #     author_record.append({"photo":df_author_photo[author]})
            result_author_record = reduce(lambda a, b: {**a, **b}, author_record)
            records.append(result_author_record)
        
        #Merge a list of dicts to single dicts
        df_output = pd.DataFrame(records)
        df_output.set_index('name', inplace=True)

        #Output dataframe to csv
        df_output.to_csv('sample.csv')

        #Output dataframe to flask
        data_dict = df_output.to_dict('index')

        return render_template("searchpage.html", output_data = data_dict)
        

    return render_template("searchpage.html") 


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)