import csv
import json
from datetime import date, datetime, timedelta



def convert_csv_to_json(filename):
    fieldnames = ["Date", "No.", "Description", "Debit", "Credit"]
    csv_filename = filename
    f = open(csv_filename, 'r')
    csv_reader = csv.DictReader(f, fieldnames)
    data = json.dumps([r for r in csv_reader])
    return json.loads(data)

def reconcile_differences(transactions, bank_transactions):
    matches = []

    for transaction in transactions:
        transaction_amount = transaction['amount'] / 1000
        transaction_payee = transaction['payee_name']

        transaction_date_str = transaction['date']
        date_format = '%Y-%m-%d'
        transaction_date = datetime.strptime(transaction_date_str, date_format).date()

        minus_3_days = transaction_date - timedelta(days=3)
        plus_3_days = transaction_date + timedelta(days=3)
        print(minus_3_days, plus_3_days)

        for idx, bank_transaction in enumerate(bank_transactions):
            if idx == 0:
                continue

            bank_amount = 0 - float(bank_transaction['Debit']) if bank_transaction['Credit'] == '' else float(bank_transaction['Credit'])
            bank_payee = bank_transaction['Description']
            
            bank_date_str = bank_transaction['Date']
            bank_date_list = bank_date_str.split('/')
            bank_date = datetime(int(bank_date_list[2]), int(bank_date_list[0]), int(bank_date_list[1])).date()

            if bank_amount == transaction_amount and minus_3_days <= bank_date and bank_date <= plus_3_days:
                previously_used = False
                for check in matches:
                    if check['bank'] == idx:
                        previously_used = True
                        print("Already used transaction")
                        break
                if not previously_used:
                    new_match = {'bank': idx, 'ynab': transaction['id']}
                    matches.append(new_match)
                    print('MATCH!!')
                    break

    print(len(transactions), len(bank_transactions))
    print(len(matches))

    matches.sort(key=lambda x: x['bank'], reverse=False)
    # print(matches)

    unmatched_bank = []

    for idx, bank_transaction in enumerate(bank_transactions):
        match_found = False
        for check in matches:
            if check['bank'] == idx:
                match_found = True
                break

        if not match_found:
            unmatched_bank.append(bank_transaction)

    print(len(unmatched_bank))
    print(unmatched_bank)

    unmatched_transactions = []

    for transaction in transactions:
        match_found = False
        for check in matches:
            if check['ynab'] == transaction['id']:
                match_found = True
                break

        if not match_found:
            unmatched_transactions.append(transaction)

    print(len(unmatched_transactions))
    print(unmatched_transactions)
    