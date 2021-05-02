from flask import Flask , render_template ,request
from pymongo import MongoClient

"""
import os
db_user = os.environ['USER']
db_pass = os.environ['PASS']
print(db_user, db_pass)
"""

app=Flask("myapp")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/result")
def result():
    if request.method == "GET":
        name=request.args.get("name")
        roll=request.args.get("roll")
        client = MongoClient('mongodb://127.0.0.1:27017')
        result = client['flask_db']['marks'].find({"name" : name , "rollno" : int(roll)} )
        if result.count() == 0:
            return "Wrong Credentials"

        for i in result:
            mk=int(i['marks'])
            output="Marks obtained by " + name + " are : " + str(mk)
            if mk >= 90:
               print("Congrats You Got First Division")
            else:
                print("Oops ! You need to World Hard")
            return str(output)
                      
        
if __name__ == '__main__':
    app.run(debug=True)


