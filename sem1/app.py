from flask import Flask, render_template


app = Flask(__name__)  # Экзмепляр класса Flask


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/visitor/<name>')
def hello_visitor(name: str):
    return render_template('hello_visitor.html', visitor=name)


@app.route('/static')
def static_page():
    return render_template('static_page.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
    )
