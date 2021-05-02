from pymongo import MongoClient

name=input("Enter Your Name  : ")

client = MongoClient('mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
filter={}
result = client['mark_jan']['marks'].find({"name" : name})
for i in result:
    print(i)



