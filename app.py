from flask import Flask, render_template,request,jsonify


app = Flask(__name__)
app.secret_key = 'sainath123567'

@app.route('/')
def index():
    return {"response":"Hello User"}

@app.route('/login',methods=["GET","POST"])
def login():
    username=request.args.get("username")
    password=request.args.get("password")
    if username=="admin" and password=="admin123":
        return {"response":"Login Successful"}
    else:
        return {"response":"Invalid Credentials"}

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    return {"response":"You are in dashboard"}

@app.route('/logout',methods=["GET","POST"])
def logout():
    return {"response":"successfully logged out"}

@app.route("/profile",methods=["GET","POST"])
def profile():
    username=request.args.get("username")
    login_status=request.args.get("login_status")
    if username and login_status=="true":
        return {"response":"Welcome to your profile page"}
    else:
        return {"response":"Please login to access your profile"}

@app.route('/testcases_report',methods=['POST','GET'])
def testcasesreport():
    return render_template('report.html')

if __name__ == '__main__':
   app.run(debug=True,port=9090)