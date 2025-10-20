from flask import Flask, render_template,request,jsonify


app = Flask(__name__)
app.secret_key = 'sainath123567'

@app.route('/')
def index():
    return {"response":"Hello User"}

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    return {"response":"You are in dashboard"}

@app.route('/logout',methods=["GET","POST"])
def logout():
    return {"response":"successfully logged out"}

@app.route("/profile",methods=["GET","POST"])
def profile():
    return {"response":"This is your profile page"}
    
if __name__ == '__main__':
   app.run(debug=True,port=9090)