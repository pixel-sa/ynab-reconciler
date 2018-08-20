import config 
import csv
import json
import os
import requests
import time
import io

from flask import Flask, render_template, jsonify, request, redirect, session, json
from datetime import datetime, date, time, timedelta
from difflib import SequenceMatcher
import utils as utils

application = Flask(__name__)
application.secret_key = config.app_secret_key

@application.route('/')
def index():
    return render_template('home.html')

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/ynab', methods=['GET', 'POST'])
def get_budget():

    access_token = utils.get_session_token()
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

@application.route('/api/accounts', methods=['GET'])
def get_accounts():
    print("accounts api")
    budget_id = request.args['budgetId']

    access_token = utils.get_session_token()
    header = {'Authorization': 'Bearer ' + access_token}

    get_accounts_url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts'
    accounts_response = requests.get(get_accounts_url, headers=header)

    status = accounts_response.status_code
    if status == 200:
        accounts_list = accounts_response.json()
        return jsonify(accounts_list)
    else:
        return("Error!!! " + str(status))




@application.route('/api/transactions', methods=['GET'])
def get_transactions():
    print("transaction api!!!")
    budget_id = request.args['budgetId']
    account_id = request.args['accountId']
    # balance = request.args['balance']
    csv_file = 'transactions.CSV'

    print(budget_id)
    print(account_id)
    # print(balance)
    access_token = utils.get_session_token()
    

    # bank_data = utils.convert_csv_to_json(csv_file)

    # utils.reconcile_differences(transaction_list, bank_data, limit_date)

    return jsonify("success")

@application.route('/upload/csv', methods=["POST"])
def uploadCsv():

    converted_transaction = {'transactions': []}
    print("converting....")

    budget_id = request.form.get('budgetId')
    account_id = request.form.get('accountId')
    print(budget_id)
    print(account_id)

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
        
        if credit:
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
    
    access_token = utils.get_session_token()
    transaction_list = utils.get_ynab_transactions(access_token, budget_id, account_id)

    last_date = datetime.now().date() - timedelta(days=14)
    unmatched_transactions = utils.reconcile_differences(transaction_list, converted_transaction, last_date)    

    return render_template("reconcile.html", unmatched_transactions=unmatched_transactions, accountId=account_id, budgetId=budget_id)

@application.route('/policy')
def policy():
    return render_template('policy.html')

@application.route('/reconcile')
def reconcile():
    return render_template('reconcile.html')

@application.route('/api/transactions/post', methods=['POST'])
def post_transactions():

    params = request.form
    budget_id = params['budget_id']
    account_id = params['account_id']
    date = params['date']
    amount = params['amount']
    payee_id = params['payee_id']
    payee_name = params['payee_name']
    category_id = params['category_id']
    memo = params['memo']
    cleared = params['cleared']
    approved = params['approved']
    flag_color = params['flag_color']
    import_id = params['import_id']

    date = datetime.now().isoformat()


    missing_transaction = {
        "transaction":
        {
            "account_id": account_id,
            "date": date,
            "amount": 5000,
            # "payee_id": "",
            "payee_name": "TEST TEST TEST",
            # "category_id": "",
            "memo": "TEST",
            "cleared": "cleared",
            "approved": True,
            "flag_color": "red",
            "import_id": "null"
        }
    }
    # missing_transaction = {
    #     "transaction":
    #     {
    #         "account_id": account_id,
    #         "date": date,
    #         "amount": amount,
    #         "payee_id": payee_id,
    #         "payee_name": payee_name,
    #         "category_id": category_id,
    #         "memo": memo,
    #         "cleared": "cleared",
    #         "approved": approved,
    #         "flag_color": flag_color,
    #         "import_id": import_id
    #     }
    # }

    print(missing_transaction)


    access_token = utils.get_session_token()
    header = {'Authorization': 'Bearer ' + access_token}
    data = missing_transaction
    print(type(data))

   
    url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/transactions' 
    response = requests.post(url, json=missing_transaction, headers=header)
    print(response)
    print(response.status_code)
    print(response.content)

    data_j = json.dumps(data)
    print(type(data_j))
  
    return jsonify("yay!")

@application.route('/authenticate')
def ynab_auth():
    return redirect(f'https://app.youneedabudget.com/oauth/authorize?client_id={config.client_id}&redirect_uri={config.get_redirect_url()}&response_type=code')

@application.route('/dashboard')
def get_access_token():
    code = request.args.get('code')
    
    params = {'client_id': config.client_id, 'client_secret': config.client_secret, 'redirect_uri': config.get_redirect_url, 'grant_type': 'authorization_code', 'code': code}
    
    response = requests.post(f'https://app.youneedabudget.com/oauth/token?client_id={config.client_id}&client_secret={config.client_secret}&redirect_uri={config.get_redirect_url()}&grant_type=authorization_code&code={code}', data=params)
    print(response.status_code, response.reason)
    
    session['token'] = json.loads(response.content.decode('utf-8'))

    return redirect('/ynab')


if __name__ == '__main__':
    application.run(debug=True)

