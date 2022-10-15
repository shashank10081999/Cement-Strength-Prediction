import csv
import json
import os
import sqlite3

import pandas as pd


class Database_operations():

    def __init__(self):
        self.path = "Prediction_database/"
        self.bad_path = "Prediction_validation/Bad"
        self.good_path = "Prediction_validation/Good"
    
    def DatabaseConnection(self,database_name):
        if os.path.isdir(self.path):
            pass
        else:
            os.mkdir(self.path)
        return sqlite3.connect(self.path+database_name+".db")

    def create_tabel(self,database_name,columns):
        try:
            conn = self.DatabaseConnection(database_name)
            conn.cursor()
            c = conn.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            
            if len(c.fetchall())  == 0:
                conn.close()
            else:
                for i in columns.keys():
                    column_type = columns[i]

                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=i,dataType=column_type))
                    except:
                        conn.execute('CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=i,dataType=column_type))
                    
                conn.close()

        except Exception as e:
            raise e

    def insertIntoTableGoodData(self,database_name):
        conn = self.DatabaseConnection(database_name)

        for i in os.listdir(self.good_path):
            with open(self.good_path+"/"+i,"r") as f:
                lines = f.readlines()
                for j in lines[1:]:
                    conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(j)))
                    conn.commit()
    

    def DatabasetoCSVFile(self,database_name):
        export_path = "Prediction_FileFromDB/"
        conn = self.DatabaseConnection(database_name)
        if os.path.isdir(export_path):
            pass
        else:
            os.mkdir(export_path)
        df = pd.read_sql_query("SELECT * from Good_Raw_Data",conn)
        df.to_csv(export_path+"InputFile.csv",index=False)
        



if __name__=="__main__":
    database_object = Database_operations()
    with open("schema_prediction.json","r") as f:
        dic = json.load(f)
    database_object.create_tabel("Prediction",dic["ColName"])
    database_object.insertIntoTableGoodData("Prediction")
    database_object.DatabasetoCSVFile("Prediction")


