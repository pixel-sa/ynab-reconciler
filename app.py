import config 
import json
import os
import requests

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ynab')
def get_budget():

    access_token = config.access_token
    header = {'Authorization': 'Bearer ' + access_token}

    url = 'https://api.youneedabudget.com/v1/budgets'
    response = requests.get(url, headers=header)

    print(response)
    print(response.status_code)

    if response.status_code == 200:
        budget_list = response.json()
        print(json.dumps(budget_list, indent=4))
        return render_template("about.html", budgets=budget_list)
    else:
        return("Error!!! " + str(response.status_code))

if __name__ == '__main__':
    app.run(debug=True)

