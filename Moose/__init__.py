from flask import Flask
from flask import render_template
from flask import request
from models.query import Query

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/', methods=['POST'])
def requested_query():
    if request.method == 'POST':
        text = request.form['search']
        if text == '':
            return start()
    
        return search(text)

    return start()

@app.route('/aggregate')
def search(text):
    query = Query(text)
    return render_template('index.html', facts=query.facts, articles=query.articles)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
