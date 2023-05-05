import pandas as pd
import time
import os


dirname = input("Please enter file name (EX std_data.csv) :")
rowName = input("Please enter target row name :")
subject = input("Please enter target subject name :")
stdNum = input("Please enter student number row name :")
stdName = input("Please enter student name row name :")


 
if (rowName != "" or subject != ""):
    cwd = os.getcwd()
    df = pd.read_csv(f'{cwd}/csv_src/'+dirname)

    target_df = df[df[rowName]==subject]

    filter_df = target_df[[stdNum, stdName, rowName]]

    print("Success to filter subject...")
    print("")

    file_name = input("Please enter the file name to save :")
    filter_df.to_csv(file_name)
else:
    print("ERROR")
    print("Please enter text...")


