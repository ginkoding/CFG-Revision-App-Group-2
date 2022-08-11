from flask import Flask, render_template, jsonify, request
# from questions_css_data import questions
# from questions_html_data import questions
# from questions_javascript_data import questions
# from questions_python_data import questions
# from questions_sql_data import questions

app = Flask(__name__)

# App routes to high level Questions
@app.route('/')
@app.route('/index/questions')
def questions():
    return render_template("questions.html")

@app.route('/index/questions/learn_css')
def retrieve_css():
    return render_template("learn_css.html")

@app.route('/index/questions/learn_html')
def retrieve_html():
    return render_template("learn_html.html")

@app.route('/index/questions/learn_javascript')
def retrieve_javascript():
    return render_template("learn_javascript.html")

@app.route('/index/questions/learn_python')
def retrieve_python():
    return render_template("learn_python.html")

@app.route('/index/questions/learn_sql')
def retrieve_sql():
    return render_template("learn_sql.html")



# App routes Css topics

@app.route('/index/questions/learn_css/css_basics')
def css_basics():
    return render_template("css_basics.html")

@app.route('/index/questions/learn_css/css_data_types')
def css_data_types():
    return render_template("css_data_types.html")


# App routes HTML topics

@app.route('/index/questions/learn_html/html_basics')
def html_basics():
    return render_template("html_basics.html")

@app.route('/index/questions/learn_html/html_data_types')
def html_data_types():
    return render_template("html_data_types.html")


# App routes Javascript topics

@app.route('/index/questions/learn_javascript/javascript_operators')
def javascript_operators():
    return render_template("javascript_operators.html")

@app.route('/index/questions/learn_javascript/javascript_data_types')
def javascript_data_types():
    return render_template("javascript_data_types.html")

@app.route('/index/questions/learn_javascript/javascript_methods')
def javascript_methods():
    return render_template("javascript_methods.html")

# App routes Python topics

@app.route('/index/questions/learn_python/python_operators')
def python_operators():
    return render_template("python_operators.html")

@app.route('/index/questions/learn_python/python_data_types')
def python_data_types():
    return render_template("python_data_types.html")

# App routes SQL topics

@app.route('/index/questions/learn_sql/sql_basics')
def sql_basics():
    return render_template("sql_basics.html")

@app.route('/index/questions/learn_sql/sql_ordering_data')
def sql_ordering_data():
    return render_template("sql_ordering_data.html")


if __name__ == '__main__':
    app.run(debug=True)




