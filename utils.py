import csv
import json
from datetime import date, datetime



def convert_csv_to_json(filename):
    fieldnames = ["Date", "No.", "Description", "Debit", "Credit"]
    # csv_filename = filename
    # f = open(csv_filename, 'r')
    # csv_reader = csv.DictReader(f, fieldnames)
    csv_reader = csv.DictReader(filename, fieldnames)
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

        print(transaction_amount, transaction_date, transaction_payee)

        for idx, bank_transaction in enumerate(bank_transactions):
            if idx == 0:
                continue

            bank_amount = bank_transaction['Debit'] if bank_transaction['Credit'] == '' else bank_transaction['Credit'] 
            bank_payee = bank_transaction['Description']
            
            bank_date_str = bank_transaction['Date']
            bank_date_list = bank_date_str.split('/')
            bank_date = datetime(int(bank_date_list[2]), int(bank_date_list[0]), int(bank_date_list[1])).date()

            print(bank_amount, bank_date, bank_payee)
