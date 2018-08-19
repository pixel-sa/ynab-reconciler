import config 
import csv
import json
import os
import requests
import time
import pandas as pd
import io

from flask import Flask, render_template, jsonify, request, redirect, session, json
from datetime import datetime, date, time, timedelta
from difflib import SequenceMatcher
import utils as utils

app = Flask(__name__)
# app.secret_key = config.app_secret_key

@app.route('/')
def index():
    print(config.access_token)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ynab', methods=['GET', 'POST'])
def get_budget():

    access_token = config.access_token
    # print(session['token'])
    # access_token = session['token']
    # access_token = access_token['access_token']
    # print(access_token)
    header = {'Authorization': 'Bearer ' + access_token}

    url = 'https://api.youneedabudget.com/v1/budgets'
    response = requests.get(url, headers=header)
    print(response.headers['X-RATE-LIMIT'])

    if response.status_code == 200:
        budget_list = response.json()
        return render_template("about.html", budgets=budget_list)
    else:
        return("Error!!! " + str(response.status_code))

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    print("accounts api")
    budget_id = request.args['budgetId']

    access_token = config.access_token
    header = {'Authorization': 'Bearer ' + access_token}

    get_accounts_url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts'
    accounts_response = requests.get(get_accounts_url, headers=header)

    status = accounts_response.status_code
    if status == 200:
        accounts_list = accounts_response.json()
        return jsonify(accounts_list)
    else:
        return("Error!!! " + str(status))




@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    print("transaction api!!!")
    budget_id = request.args['budgetId']
    account_id = request.args['accountId']
    balance = request.args['balance']
    csv_file = 'transactions.CSV'

    print(budget_id)
    print(account_id)
    print(balance)
    access_token = config.access_token
    header = {'Authorization': 'Bearer ' + access_token}

    query = '?since_date=2018-08-01'
    url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts/{account_id}/transactions' + query
    response = requests.get(url, headers=header)

    data = json.loads(response.content.decode('utf-8'))
    transaction_list = data['data']['transactions']

    # bank_data = utils.convert_csv_to_json(csv_file)

    # utils.reconcile_differences(transaction_list, bank_data)

    return jsonify(transaction_list)

@app.route('/upload/csv', methods=["POST"])
def uploadCsv():

    converted_transaction = {'transactions': []}
    print("converting....")

    # https://stackoverflow.com/questions/10617286/getting-type-error-while-opening-an-uploaded-csv-file
    filename = request.files['file'].read()
    filename = filename.decode("utf-8")
    io_string = io.StringIO(filename)

    for transaction in csv.reader(io_string, delimiter=",", quotechar='"'):
        transaction_date = transaction[0]
        no = transaction[1]
        description = transaction[2]
        debit = transaction[3]
        credit = transaction[4]

        if transaction_date.isalpha():
            continue
        
        if debit:
            converted_transaction['transactions'].append({
                "Date": transaction_date,
                "No.": "",
                "Description":description,
                "Debit": "",
                "Credit": credit
                
            })         
        elif debit:
            converted_transaction['transactions'].append({
                "Date": transaction_date,
                "No.": "",
                "Description":description,
                "Debit": debit,
                "Credit": ""
                            
            })  
    # print(converted_transaction)
    return jsonify("success!")

# @app.route('/authenticate')
# def ynab_auth():
#     print(config.get_redirect_url())
#     return redirect(f'https://app.youneedabudget.com/oauth/authorize?client_id={config.client_id}&redirect_uri={config.get_redirect_url()}&response_type=code')
#     # return redirect(f'https://app.youneedabudget.com/oauth/authorize?client_id={config.client_id}&redirect_uri={config.get_redirect_url()}&response_type=token')

# @app.route('/dashboard')
# def get_access_token():
#     code = request.args.get('code')
#     print(code)
#     params = {'client_id': config.client_id, 'client_secret': config.client_secret, 'redirect_uri': config.get_redirect_url, 'grant_type': 'authorization_code', 'code': code}
#     # response = requests.post('https://app.youneedabudget.com/oauth/token', data=params)
#     response = requests.post(f'https://app.youneedabudget.com/oauth/token?client_id={config.client_id}&client_secret={config.client_secret}&redirect_uri={config.get_redirect_url()}&grant_type=authorization_code&code={code}', data=params)
#     print(response.status_code, response.reason)
    
#     print(response.content.decode('utf-8'))
#     session['token'] = json.loads(response.content.decode('utf-8'))

#     return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

