import csv

def giniIndex(data, classIndex):
    total = len(data)
    count = {}
    for row in data:
        label = row[classIndex]
        count[label] = count.get(label, 0) + 1
    gini = 1 - sum((c / total) ** 2 for c in count.values())
    return gini

def calculate_gini(file_name):
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        data = [row for row in csv_reader]
        
        classIndex = len(headers) - 1
        attrIndex = 0
        
        attr_values = {}
        for row in data:
            value = row[attrIndex]
            attr_values.setdefault(value, []).append(row)
        
        for value, subset in attr_values.items():
            gini = giniIndex(subset, classIndex)
            print(f'Gini Index for "{value}": {gini:.4f}')
        
        total = len(data)
        gini_attribute = sum((len(subset) / total) * giniIndex(subset, classIndex) for subset in attr_values.values())
        print(f'\nGini Index for "Colour": {gini_attribute:.4f}')

calculate_gini('data.csv')
