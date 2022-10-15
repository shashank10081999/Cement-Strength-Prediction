import json
import os
import shutil

import pandas as pd
import regex as re


def WholeColumnisNull():
    """
    Checks if any column in the dataset if any columns has all the values as Null , 
    if all the columns are fine then the file will be moved to the good data folder
    else the file is moved to bad data folder 

    Return : None 
    """
    path = "Training_validation/Good"
    for i in os.listdir(path):
        df = pd.read_csv("Training_validation/Good" + "/" + i)
        for j in df.columns:
            if (len(df[j]) - df[j].count())==len(df[j]):
                shutil.move("Training_validation/Good" + "/" + i , "Training_validation/Bad")
                break



def column_validation(NumberofColumns):

    """
    The Column_validation function will check if if the file has the number columns right 
    if all the columns are fine then the file will be moved to the good data folder
    else the file is moved to bad data folder 

    Return : None
    """
    path = "Training_validation/Good"
    for i in os.listdir(path):
        df = pd.read_csv("Training_validation/Good" + "/" + i)
        if df.shape[1] == NumberofColumns:
            pass
        else:
            shutil.move("Training_validation/Good" + "/" + i , "Training_validation/Bad")



def deleteExistingBadDataTrainingFolder():

    """
    The DeleteExistingBadDataTrainingFolder function will delete everything in the bad data folder

    Return : None
    """

    if os.path.isdir("Training_validation/Bad"):
        shutil.rmtree("Training_validation/Bad")

def deleteExistingGoodDataTrainingFolder():
        if os.path.isdir("Training_validation/Good"):
            shutil.rmtree("Training_validation/Good")


def valuesFromSchema():
    path = "schema_training.json"
    with open(path) as file:
        dic = json.load(file)
    return dic["LengthOfDateStampInFile"],dic["LengthOfTimeStampInFile"],dic["ColName"],dic["NumberofColumns"]

def validationFileNameRaw(LengthOfDateStampInFile,LengthOfTimeStampInFile):
    deleteExistingBadDataTrainingFolder()
    deleteExistingGoodDataTrainingFolder()

    os.mkdir("Training_validation/Good")
    os.mkdir("Training_validation/Bad")

    regex = "['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"
    path = "Training_Data"
    list_file = os.listdir(path)
    for i in list_file:
        if re.match(regex,i):
            part_of_filename = re.split(".csv",i)
            part_of_file = re.split("_",part_of_filename[0])
            if len(part_of_file[2]) == LengthOfDateStampInFile:
                if len(part_of_file[3]) == LengthOfTimeStampInFile:
                    shutil.copy(path+"/"+i,"Training_validation/Good")
                else:
                    shutil.copy(path+"/"+i,"Training_validation/Bad")
            else:
                shutil.copy(path+"/"+i,"Training_validation/Bad")
        else:
            shutil.copy(path+"/"+i,"Training_validation/Bad")


if __name__ == "__main__":
    LengthOfDateStampInFile , LengthOfTimeStampInFile , ColName , NumberofColumns = valuesFromSchema()
    validationFileNameRaw(LengthOfDateStampInFile,LengthOfTimeStampInFile)
    column_validation(NumberofColumns)
    WholeColumnisNull()
