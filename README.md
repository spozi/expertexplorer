**Career-Prospect-System**

This web-based system is a search engine to match a job or career with job candidates by using job candidates's publications. A pretrained SciBERT model is used to obtain the job matching rate and average similarity between each job candidates and jobs by the users.


**Installation**
1. Download this repository.
2. Change the MySQL connection to your own MySQL scheme from app.py line 14 to 19.
![image](https://user-images.githubusercontent.com/93475397/169473035-4315b394-f145-4948-a29a-97714109c7a5.png)
3. Create database in MySQL. There are 6 databases that should be created, including job, candidate, publications_tab_2018, publications_tab_2019, publications_tab_2020, and publications_tab_2021. You can copy the code from the MySQL folder and paste it into your MySQL to create these databases. 
4. Import data into database. Only job databases need to import the excel file from MySQL.
5. Import data from init_db.py. 
   * Import excel file 18.xlsx, 19.xlsx, 20.xlsx, and 21.xlsx.
   
   * Import excel file 18.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   ![image](https://user-images.githubusercontent.com/93475397/169506384-ed7f24cb-26cc-4f07-8db4-6e4ccba29c3b.png)
   ![image](https://user-images.githubusercontent.com/93475397/169506496-ea423afd-e22d-4132-9a41-4c51f62be7a6.png)

   * Import excel file 19.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   ![image](https://user-images.githubusercontent.com/93475397/169509417-3aab8a81-7022-49b0-8994-2124eece3406.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509516-3cf7e4b2-6e60-4080-952f-de54df69168a.png)

   * Import excel file 20.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   ![image](https://user-images.githubusercontent.com/93475397/169509741-150a577b-36ee-4152-927f-5feb69efcf11.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509623-7647b4de-2818-412b-8e77-786c6b220598.png)

   * Import excel file 21.xlsx, change line 7 in init_db.py and line 55 in mysql_manager.py before import data. Then, run init_db.py.
   ![image](https://user-images.githubusercontent.com/93475397/169509864-a0e9ea63-5e39-429e-bcf5-84ef9b028ea0.png)
   ![image](https://user-images.githubusercontent.com/93475397/169509945-978831d4-6b69-453d-9a48-88fc98611945.png)
   * Check and make sure the excel file is imported into the correct database.




 
