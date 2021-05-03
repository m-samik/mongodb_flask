from flask import Flask , render_template ,request
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app=Flask("myapp")


client = MongoClient('mongodb://127.0.0.1:27017')
mydb = client["student_db"]
mycol = client["result"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/register",methods =['POST'])
def auth():
    if request.method == "POST":
        uname=request.form.get("uname")
        passwd=request.form.get("passwd")
    data = client['student_db']['passwd'].find({"uname" : uname , "passwd" : passwd} )
    user =[]
    passw=[]
    for i in data :
        user=i['uname']
        passw=i['passwd']
    
    if uname == user and passwd == passw:
        return render_template("register.html")
    else:
        error="Check the username and passwoord again!!"
        return render_template("admin.html" , error = error)



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
        imagefolder="static/images/"
        f = request.files['file']
        filename=secure_filename(f.filename)
        filename=rollno+filename
        path=os.path.join(imagefolder,filename)
        f.save(path)
        values=[{
                    "name"	:name,
                    "phone" :mobile,
                    "rollno":int(rollno),
                    "marks" : {
                                "physics":int(phym),
                                "chemistry":int(chm),
                                "maths" : int(mthm)
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
            return render_template("index.html")

        for i in result:
            namer=(i['name'])
            rollr=(i['rollno'])
            physics=(i['marks']['physics'])
            chemistry=(i['marks']['chemistry'])
            maths=(i['marks']['maths'])
            image=(i['image'])

            total=physics+chemistry+maths
            per=(total/300)*100
            per=round(per)
            formrender=render_template(
                "result.html",name=namer, roll=rollr,phy=str(physics) , chem=str(chemistry) , mth=str(maths) , tot=str(total) , percent=str(per) , img=image
            )
            output="Marks obtained by " + name + " are : " + str(total) + "percentage = " + str(per)
            return formrender
                      
        
if __name__ == '__main__':
    app.run(debug=True)


