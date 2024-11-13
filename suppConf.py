import csv

def read_transactions(filename):
    transactions = []
    items = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        items = header[1:]
        
        for row in reader:
            transaction = []
            for i in range(1, len(row)):
                if row[i].strip():
                    transaction.append(items[i-1])
            transactions.append(transaction)
    
    return transactions, items

def get_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        match = True
        for item in itemset:
            found = False
            for transaction_item in transaction:
                if transaction_item == item:
                    found = True
                    break
            if not found:
                match = False
                break
        if match:
            count += 1
    return count

def calculate_confidence(A, B, transactions):
    support_A = get_support([A], transactions)
    support_AB = get_support([A, B], transactions)
    
    if support_A == 0:
        return 0
    
    confidence = support_AB / support_A
    return confidence

def main():
    filename = 'IP.csv'
    transactions, items = read_transactions(filename)
    total_transactions = len(transactions)
    
    print("Items in Data:")
    for item in items:
        print(f"{item}")
    print()
    
    print("For Rule A--->B enter the items")
    A_input = input("Enter item A: ")
    A = A_input.strip()
    
    B_input = input("Enter item B: ")
    B = B_input.strip()

    support_AB = get_support([A, B], transactions)

    confidence = calculate_confidence(A, B, transactions)
    
    support_percentage = (support_AB / total_transactions) * 100
    confidence_percentage = confidence * 100

    print(f"\nRule: {A} ---> {B}")
    print(f"Support: {support_percentage:.2f}%")
    print(f"Confidence: {confidence_percentage:.2f}%")

if __name__ == "__main__":
    main()
