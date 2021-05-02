from pymongo import MongoClient
"""
import os
db_user = os.environ['USER']
db_pass = os.environ['PASS']
print(db_user, db_pass)
"""

name=input("Enter Your Name  : ")

client = MongoClient('mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

result = client['mark_jan']['marks'].find({"name" : name , "marks" : 75} )
for i in result:
    mk=int(i['marks'])
    print("Marks obtained by " + name + " are : " + str(mk))
    if mk >= 90:
        print("Congrats You Got First Division")
    else:
        print("Oops ! You need to World Hard") 



