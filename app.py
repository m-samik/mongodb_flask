from flask import Flask , render_template ,request
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

"""
import os
db_user = os.environ['USER']
db_pass = os.environ['PASS']
print(db_user, db_pass)
"""

app=Flask("myapp")


client = MongoClient('mongodb://127.0.0.1:27017')
mydb = client["student_db"]
mycol = client["result"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register" )
def register():
    return render_template("register.html")

@app.route('/submit',methods =['POST'])
def up():
    if request.method == "POST":
        #Values getting from HTML Form 
        name=request.form.get("name")
        rollno=request.form.get("rollno")
        mobile=request.form.get("mobile")
        phym=request.form.get("physics")
        chm=request.form.get("chemistry")
        mthm=request.form.get("maths")
        #Getting File for Profile Picture
        imagefolder="static/images"
        f = request.files['file']
        filename=secure_filename(f.filename)
        path=os.path.join(imagefolder,filename)
        f.save(path)
        values=[{
                    "name"	:name,
                    "phone" :mobile,
                    "rollno":rollno,
                    "marks" : {
                                "physics":phym,
                                "chemistry":chm,
                                "maths" : mthm
                                },
                    "image" :imagefolder+filename

                }]
        client['student_db']['result'].insert_many(values)
        return render_template("registerc.html" , uname=name)
    


@app.route("/result")
def result():
    if request.method == "GET":
        name=request.args.get("name")
        roll=request.args.get("roll")
        result = client['student_db']['result'].find({"name" : name , "rollno" : int(roll)} )
        if result.count() == 0:
            return "Wrong Credentials"

        for i in result:
            namer=(i['name'])
            rollr=(i['rollno'])
            physics=(i['marks']['physics'])
            chemistry=(i['marks']['chemistry'])
            maths=(i['marks']['maths'])
            image=(i['image'])

            total=physics+chemistry+maths
            per=total/300*100
            formrender=render_template(
                "result.html",name=namer, roll=rollr,phy=str(physics) , chem=str(chemistry) , mth=str(maths) , tot=str(total) , percent=str(per) , img=image
            )
            output="Marks obtained by " + name + " are : " + str(total) + "percentage = " + str(per)
            return formrender
                      
        
if __name__ == '__main__':
    app.run(debug=True)


