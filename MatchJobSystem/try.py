#from statistics import variance
from flask import Flask, render_template, request, flash, send_file
from flask_mysqldb import MySQL
from flask_paginate import Pagination
# from sumSimilarity import Sum
#from model import calculateSim
# from preprocessingParagraph import preProcessing
from main import match_job
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import io
from mysql_manager import MySQLManager
from scibert import SciBERT

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'publications_db'
app.config['MYSQL_PORT'] = 3307
app.config['SECRET_KEY'] = 'something only you know'

isMatched = False
global_id = "id"
result = "result"
mysql = MySQL()
mysql.init_app(app)
scibert = SciBERT()
plt.rcParams.update({'figure.max_open_warning': 0})

@app.route("/")
def index():
    return render_template("searchpage.html")

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)