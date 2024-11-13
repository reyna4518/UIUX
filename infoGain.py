import math
import csv

def readFile(file_name):
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        data = list(csv_reader)
    return headers, data

def calInfo(data, classIndex):
    total = len(data)
    countMat = {}
    for row in data:
        label = row[classIndex]
        countMat[label] = countMat.get(label, 0) + 1
    entropy = 0
    for count in countMat.values():
        prob = count / total
        entropy -= prob * math.log2(prob)
    return entropy

def calEachInfo(data, attrIndex, classIndex):
    total = len(data)
    attrGroups = {}
    for row in data:
        attr_value = row[attrIndex]
        if attr_value not in attrGroups:
            attrGroups[attr_value] = []
        attrGroups[attr_value].append(row)
    info = 0
    for subset in attrGroups.values():
        info += (len(subset) / total) * calInfo(subset, classIndex)
    return info

def calEntropy(data, attrIndex):
    total = len(data)
    countMat = {}
    for row in data:
        attr_value = row[attrIndex]
        countMat[attr_value] = countMat.get(attr_value, 0) + 1
    entropy = 0
    for count in countMat.values():
        prob = count / total
        entropy -= prob * math.log2(prob)
    return entropy

def Gain(data, attrIndex, classIndex):
    return calInfo(data, classIndex) - calEachInfo(data, attrIndex, classIndex)

def main():
    headers, data = readFile('data.csv')
    classIndex = len(headers) - 1
    best_gain = -1
    best_attr = None

    print(f'Info of target class ({headers[classIndex]}): {calInfo(data, classIndex):.3f}\n')

    for attrIndex in range(classIndex):
        attr_entropy = calEntropy(data, attrIndex)
        info_gain = Gain(data, attrIndex, classIndex)
        print(f'Entropy of {headers[attrIndex]}: {attr_entropy:.4f}')
        print(f'Information Gain for {headers[attrIndex]}: {info_gain:.4f}\n')
        if info_gain > best_gain:
            best_gain = info_gain
            best_attr = headers[attrIndex]

    print(f'Best Splitting Attribute: {best_attr} with Information Gain: {best_gain:.4f}')

if __name__ == "__main__":
    main()
