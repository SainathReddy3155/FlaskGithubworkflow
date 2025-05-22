from flask import Flask, render_template,request,jsonify
import requests

app = Flask(__name__)
app.secret_key = 'sainath123567'

@app.route('/')
def index():
    return {"response":"Hello User"}

@app.route("/login",methods=['GET','POST'])
def login():
    print("Hey user")
    
    return {"response":"Successfully loggedin"}

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    return {"response":"You are in dashboard"}

@app.route('/logout',methods=["GET","POST"])
def logout():
    return {"response":"successfully logged out"}
    
if __name__ == '__main__':
   app.run(debug=True,port=9090)