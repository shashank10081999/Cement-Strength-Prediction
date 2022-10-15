import json
import os
import shutil

import pandas as pd
import regex as re


def WholeColumnisNull():
    path = "Prediction_validation/Good"
    for i in os.listdir(path):
        df = pd.read_csv("Prediction_validation/Good" + "/" + i)
        for j in df.columns:
            if (len(df[j]) - df[j].count())==len(df[j]):
                shutil.move("Prediction_validation/Good" + "/" + i , "Prediction_validation/Bad")
                break



def column_validation(NumberofColumns):
    path = "Prediction_validation/Good"
    for i in os.listdir(path):
        df = pd.read_csv("Prediction_validation/Good" + "/" + i)
        if df.shape[1] == NumberofColumns-1:
            pass
        else:
            shutil.move("Prediction_validation/Good" + "/" + i , "Prediction_validation/Bad")



def deleteExistingBadDataTrainingFolder():
    if os.path.isdir("Prediction_validation/Bad"):
        shutil.rmtree("Prediction_validation/Bad")

def deleteExistingGoodDataTrainingFolder():
        if os.path.isdir("Prediction_validation/Good"):
            shutil.rmtree("Prediction_validation/Good")


def valuesFromSchema():
    path = "schema_training.json"
    with open(path) as file:
        dic = json.load(file)
    return dic["LengthOfDateStampInFile"],dic["LengthOfTimeStampInFile"],dic["ColName"],dic["NumberofColumns"]

def validationFileNameRaw(LengthOfDateStampInFile,LengthOfTimeStampInFile):
    deleteExistingBadDataTrainingFolder()
    deleteExistingGoodDataTrainingFolder()

    os.mkdir("Prediction_validation/Good")
    os.mkdir("Prediction_validation/Bad")

    regex = "['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"
    path = "Prediction_Batch_files"
    list_file = os.listdir(path)
    for i in list_file:
        if re.match(regex,i):
            part_of_filename = re.split(".csv",i)
            part_of_file = re.split("_",part_of_filename[0])
            if len(part_of_file[2]) == LengthOfDateStampInFile:
                if len(part_of_file[3]) == LengthOfTimeStampInFile:
                    shutil.copy(path+"/"+i,"Prediction_validation/Good")
                else:
                    shutil.copy(path+"/"+i,"Prediction_validation/Bad")
            else:
                shutil.copy(path+"/"+i,"Prediction_validation/Bad")
        else:
            shutil.copy(path+"/"+i,"Prediction_validation/Bad")


if __name__ == "__main__":
    LengthOfDateStampInFile , LengthOfTimeStampInFile , ColName , NumberofColumns = valuesFromSchema()
    validationFileNameRaw(LengthOfDateStampInFile,LengthOfTimeStampInFile)
    column_validation(NumberofColumns)
    WholeColumnisNull()
