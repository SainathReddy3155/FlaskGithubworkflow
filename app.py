from flask import Flask, render_template,request,jsonify


app = Flask(__name__)
app.secret_key = 'sainath123567'

@app.route('/')
def index():
    return {"response":"Hello Guest"}



if __name__ == '__main__':
   app.run(debug=True,port=9090)