# used to add money to the account

import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase app
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def update_account_amount(name=None, amount=None):
    if name is None:
        name = input("Enter your name: ")
    if amount is None:
        amount = float(input("Enter the transaction amount: "))

    # Query for the document in the "accounts" collection based on the user's name
    query = db.collection("accounts").where("name", "==", name).limit(1)
    docs = query.stream()

    # Update the amount field in the existing document
    for doc in docs:
        doc_ref = db.collection("accounts").document(doc.id)
        doc_ref.update({
            'amount': firestore.Increment(amount)
        })
        print("Amount updated successfully.")

def save_transaction(name=None, amount=None):
    if name is None:
        name = input("Enter your name: ")
    if amount is None:
        amount = float(input("Enter the transaction amount: "))
    
    transaction_desc = f"Added {amount} money."

    transaction_time = time.strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Reference the existing "transactions" collection and add a new document
        db.collection("transactions").add({
            'name': name,
            'amount': amount,
            'transaction_time': transaction_time,
            'transaction_desc': transaction_desc
        })

        # Update the amount in the "accounts" collection for the specified user
        update_account_amount(name, amount)
        
        print("Transaction saved successfully.")
    except Exception as e:
        print("Failed to save transaction:", e)

if __name__ == "__main__":
    save_transaction()
