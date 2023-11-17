from flask import Flask,render_template

app = Flask(__name__)

application = app

@app.route('/')
def index():
    with open('secilen.txt','r',encoding='utf-8') as f:
        secilen = f.read()
    
    return render_template('index.html',resim=secilen)
    

if __name__ == '__main__':
    app.run(debug=True)