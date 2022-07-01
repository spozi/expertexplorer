from scibert import SciBERT
import numpy as np
import pandas as pd

USER = "root"
PASSWORD = "mysqlpw"
HOST = "127.0.0.1"
PORT = '55000'
DATABASE = "publications_db" #Please create this db first in mysql



from sqlalchemy import create_engine
eng_str = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (USER,PASSWORD,HOST,PORT,DATABASE)
engine = create_engine(eng_str)

#Load scibert model
scibert = SciBERT()

#1. Load data into dataframe
print("Load data into dataframe")
df1 = pd.read_excel('18.xlsx')
df2 = pd.read_excel('19.xlsx')
df3 = pd.read_excel('20.xlsx')
df4 = pd.read_excel('21.xlsx')

#2. Vectorize the abstract and put into mysql
print("Vectorize and put into mysql")
print(2018)
df1['scibert_vector'] = df1['Abstract'].apply(scibert.vectorize)
df1.to_sql('publications_2018', engine) #Use numpy eval to convert numpy string to numpy

print(2019)
df2['scibert_vector'] = df2['Abstract'].apply(scibert.vectorize)
df2.to_sql('publications_2019', engine)

print(2020)
df3['scibert_vector'] = df3['Abstract'].apply(scibert.vectorize)
df3.to_sql('publications_2020', engine)

print(2021)
df4['scibert_vector'] = df4['Abstract'].apply(scibert.vectorize)
df4.to_sql('publications_2021', engine)

#3. Put into mysql
# df1.to_sql('publications_2018', engine) #Use numpy eval to convert numpy string to numpy
# df2.to_sql('publications_2019', engine)
# df3.to_sql('publications_2020', engine)
# df4.to_sql('publications_2021', engine)