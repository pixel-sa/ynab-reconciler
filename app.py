import config 
import csv
import json
import os
import requests
import time
import pandas as pd

from flask import Flask, render_template, jsonify, request, redirect, session, json
from datetime import datetime, date, time, timedelta
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = config.app_secret_key

@app.route('/')
def index():
    print(config.access_token)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ynab')
def get_budget():

    # access_token = config.access_token
    print(session['token'])
    access_token = session['token']
    access_token = access_token['access_token']
    print(access_token)
    header = {'Authorization': 'Bearer ' + access_token}

    url = 'https://api.youneedabudget.com/v1/budgets'
    response = requests.get(url, headers=header)

    print(response)
    print(response.status_code)

    if response.status_code == 200:
        budget_list = response.json()
        # print(json.dumps(budget_list, indent=4))
        return render_template("about.html", budgets=budget_list)
    else:
        return("Error!!! " + str(response.status_code))


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    print("transaction api!!!")
    budget_id = request.args['budgetId']

    access_token = config.access_token
    header = {'Authorization': 'Bearer ' + access_token}

    get_accounts_url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts'
    accounts_response = requests.get(get_accounts_url, headers=header)
    # print(accounts_response.json())

    query = '?since_date=2018-08-01'
    url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/transactions' + query
    response = requests.get(url, headers=header)

    print(response)
    print(response.headers)
    # print(response.json())
    transaction_list = response.json()
    # print(json.dumps(transaction_list, indent=4))
    print(type(transaction_list))
    print(len(transaction_list['data']['transactions']))



    return jsonify("yay!")


@app.route('/authenticate')
def ynab_auth():
    print(config.get_redirect_url())
    return redirect(f'https://app.youneedabudget.com/oauth/authorize?client_id={config.client_id}&redirect_uri={config.get_redirect_url()}&response_type=code')
    # return redirect(f'https://app.youneedabudget.com/oauth/authorize?client_id={config.client_id}&redirect_uri={config.get_redirect_url()}&response_type=token')

@app.route('/dashboard')
def get_access_token():
    code = request.args.get('code')
    print(code)
    params = {'client_id': config.client_id, 'client_secret': config.client_secret, 'redirect_uri': config.get_redirect_url, 'grant_type': 'authorization_code', 'code': code}
    # response = requests.post('https://app.youneedabudget.com/oauth/token', data=params)
    response = requests.post(f'https://app.youneedabudget.com/oauth/token?client_id={config.client_id}&client_secret={config.client_secret}&redirect_uri={config.get_redirect_url()}&grant_type=authorization_code&code={code}', data=params)
    print(response.status_code, response.reason)
    
    print(response.content.decode('utf-8'))
    session['token'] = json.loads(response.content.decode('utf-8'))

    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

