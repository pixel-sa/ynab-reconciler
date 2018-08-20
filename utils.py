import csv
import json
import requests
from datetime import date, datetime, timedelta



def convert_csv_to_json(filename):
    fieldnames = ["Date", "No.", "Description", "Debit", "Credit"]
    # csv_filename = filename
    # f = open(csv_filename, 'r')
    # csv_reader = csv.DictReader(f, fieldnames)
    csv_reader = csv.DictReader(filename, fieldnames)
    data = json.dumps([r for r in csv_reader])
    return json.loads(data)

def reconcile_differences(transactions, converted_bank_csv, since_date):
    matches = []
    bank_transactions = converted_bank_csv['transactions']
    
    for transaction in transactions:
    
        transaction_amount = transaction['amount'] / 1000
        transaction_payee = transaction['payee_name']
        print(transaction_payee + ' - ' + str(transaction_amount))
        transaction_date_str = transaction['date']
        date_format = '%Y-%m-%d'
        transaction_date = datetime.strptime(transaction_date_str, date_format).date()

        minus_3_days = transaction_date - timedelta(days=3)
        plus_3_days = transaction_date + timedelta(days=3)

        for idx, bank_transaction in enumerate(bank_transactions):
            bank_amount = 0 - float(bank_transaction['Debit']) if bank_transaction['Credit'] == '' else float(bank_transaction['Credit'])
            bank_payee = bank_transaction['Description']
            
            bank_date_str = bank_transaction['Date']
            bank_date_list = bank_date_str.split('/')
            bank_date = datetime(int(bank_date_list[2]), int(bank_date_list[0]), int(bank_date_list[1])).date()

            if bank_date < since_date:
                continue

            if bank_amount == transaction_amount and minus_3_days <= bank_date and bank_date <= plus_3_days:
                previously_used = False
                for check in matches:
                    if check['bank'] == idx:
                        previously_used = True
                        break
                if not previously_used:
                    new_match = {'bank': idx, 'ynab': transaction['id']}
                    matches.append(new_match)
                    break
    
    print(len(transactions), len(bank_transactions))
    print(len(matches))
    

    matches.sort(key=lambda x: x['bank'], reverse=False)
    # print(matches)

    unmatched_bank = []

    for idx, bank_transaction in enumerate(bank_transactions):
        match_found = False

        bank_date_str = bank_transaction['Date']
        bank_date_list = bank_date_str.split('/')
        bank_date = datetime(int(bank_date_list[2]), int(bank_date_list[0]), int(bank_date_list[1])).date()

        for check in matches:
            if check['bank'] == idx:
                match_found = True
                break

        if not match_found and bank_date > since_date:
            unmatched_bank.append(bank_transaction)
    print('-unmatched bank transaction------------------------')
    print(len(unmatched_bank))
    print(unmatched_bank)
    print('---------------------------------------')

    unmatched_transactions = []

    for transaction in transactions:
        match_found = False

        transaction_date_str = transaction['date']
        date_format = '%Y-%m-%d'
        transaction_date = datetime.strptime(transaction_date_str, date_format).date()

        for check in matches:
            if check['ynab'] == transaction['id']:
                match_found = True
                break

        if not match_found and transaction['cleared'] == 'cleared' and transaction_date > since_date:
            unmatched_transactions.append(transaction)
    print('Unmatched ynab transactions -------')
    print(len(unmatched_transactions))
    print(unmatched_transactions)
    print('-----------------------------------------')
    
    return {'bank': unmatched_bank, 'ynab': unmatched_transactions}


def get_ynab_transactions(access_token, budget_id, account_id):
    header = {'Authorization': 'Bearer ' + access_token}
    since_date = datetime.now().date() - timedelta(days=10)
    
    query = f'?since_date={since_date}'
    url = f'https://api.youneedabudget.com/v1/budgets/{budget_id}/accounts/{account_id}/transactions' + query
    response = requests.get(url, headers=header)
    
    data = json.loads(response.content.decode('utf-8'))
    transaction_list = data['data']['transactions']
    

    return transaction_list