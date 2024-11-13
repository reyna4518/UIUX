import csv

def readFile(filename):
    with open(filename, 'r') as file:
        robj = csv.reader(file)
        data = [row for row in robj]
    
    header = data[0][1:]
    transactions = []

    for row in data[1:]:
        transaction = row[1:]
        transactions.append(transaction)
    
    return header, transactions

def candidateSet(prevFreqItem, k):
    candidates = []
    n = len(prevFreqItem)
    
    for i in range(n):
        for j in range(i + 1, n):
            combined = prevFreqItem[i] + prevFreqItem[j]
            uniqueItems = []
            for item in combined:
                if item not in uniqueItems:
                    uniqueItems.append(item)
            if len(uniqueItems) == k:
                candidates.append(uniqueItems)
    
    return candidates

def supportCal(transactions, candidates, minsup, total):
    itemSup = {}

    for candidate in candidates:
        candidate_key = tuple(candidate)
        itemSup[candidate_key] = 0
        for transaction in transactions:
            if all(item in transaction for item in candidate):
                itemSup[candidate_key] += 1

    freqItem = {}
    for itemset, support_count in itemSup.items():
        support = support_count / total
        if support >= minsup:
            freqItem[itemset] = support
    
    return freqItem

def apriori(transactions, minsup):
    total = len(transactions)
    k = 1
    unique_items = []
    for transaction in transactions:
        for item in transaction:
            if item not in unique_items:
                unique_items.append(item)
    
    candidates = [[item] for item in unique_items]
    freqItemSet = []

    while candidates:
        freqItem = supportCal(transactions, candidates, minsup, total)
        if not freqItem:
            break
        
        freqItemSet.append(freqItem)

        print(f'Frequent itemsets of length {k}:')
        for itemset, support in freqItem.items():
            frequency = int(support * total)
            support_percentage = support * 100
            print(f'Itemset: {", ".join(itemset)} | Frequency: {frequency} | Support: {support_percentage:.2f}%')
        print('\n')
        
        candidates = candidateSet(list(freqItem.keys()), k + 1)
        k += 1
    
    return freqItemSet

def writeFile(filename, freqItemSet, total_transactions):
    with open(filename, 'w', newline='') as file:
        wobj = csv.writer(file)
        wobj.writerow(['Itemset', 'Frequency', 'Support (%)'])
        for k_itemsets in freqItemSet:
            for itemset, support in k_itemsets.items():
                frequency = int(support * total_transactions)
                support_percentage = support * 100
                wobj.writerow([', '.join(itemset), frequency, f'{support_percentage:.2f}'])

ip = 'IP.csv'
op = 'freqItem.csv'
minsup = float(input('Enter the minimum support (as a decimal): '))

header, transactions = readFile(ip)
total_transactions = len(transactions)
freqItemSet = apriori(transactions, minsup)
writeFile(op, freqItemSet, total_transactions)
