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

        #2. Compute the similarity
        #2a. Vectorize the query
        searchqueryvector = scibert.vectorizeWithYake(searchquery)
        for df in dfs:
            df['numpy_vector'] = df['scibert_vector'].apply(lambda x: np.eval(x))



if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)