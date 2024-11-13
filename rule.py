import csv

def load_frequent_itemsets(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        frequent_itemsets = {}
        for row in reader:
            itemset = sorted(row[0].split(', '))
            support = float(row[1])
            frequent_itemsets[str(itemset)] = frequent_itemsets.get(str(itemset), 0) + support
    return frequent_itemsets

def generate_combinations(itemset, length):
    if length == 0:
        return [[]]
    result = []
    for i in range(len(itemset)):
        for combo in generate_combinations(itemset[i+1:], length-1):
            result.append([itemset[i]] + combo)
    return result

def generate_association_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        itemset = eval(itemset)
        for i in range(1, len(itemset)):
            for freqItem in generate_combinations(itemset, i):
                item = list(set(itemset) - set(freqItem))
                confidence = frequent_itemsets[str(itemset)] / frequent_itemsets[str(freqItem)]
                if confidence >= min_confidence:
                    rules.append([freqItem, item, confidence])
    return rules

def write_rules(filename, rules):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['A', 'B', 'Confidence'])
        for freqItem, item, confidence in rules:
            writer.writerow([', '.join(freqItem), ', '.join(item), confidence])
    print(f"Association rules stored at {filename}")

def print_rules(rules):
    for freqItem, item, confidence in rules:
        print(f"A: {', '.join(freqItem)}, B: {', '.join(item)}, Confidence: {confidence:.2f}")

if __name__ == "__main__":
    filename = 'freqItem.csv'
    min_confidence = float(input("Enter minimum confidence: "))

    frequent_itemsets = load_frequent_itemsets(filename)
    
    rules = generate_association_rules(frequent_itemsets, min_confidence)
    
    print("\nGenerated Association Rules:")
    print_rules(rules)
    
    output_filename = 'association_rules.csv'
    write_rules(output_filename, rules)
