import sys
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def update_account_amount(name, amount):
    # Query Firestore to find the document with the given name
    query = db.collection('accounts').where('name', '==', name).limit(1)
    docs = query.stream()

    # If document found, update the amount
    for doc in docs:
        current_amount = doc.to_dict()['amount']
        new_amount = current_amount + amount

        # Update the document with the new amount
        doc.reference.update({'amount': new_amount})
        print(f"Amount updated successfully. New amount for {name}: {new_amount}")
        return

    # If no document found for the given name
    print(f"No account found for {name}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        name = sys.argv[2]
        amount = int(sys.argv[1])
    else:
        name = input("Enter the name of the user whose account amount you want to update: ")
        amount = int(input("Enter the amount to be added: "))
    
    update_account_amount(name, amount)
