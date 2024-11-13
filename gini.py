import math
import csv

def giniIndex(data, classIndex):
    total = len(data)
    countMat = {}
    
    for row in data:
        label = row[classIndex]
        if label not in countMat:
            countMat[label] = 0
        countMat[label] += 1

    gini = 1
    for count in countMat.values():
        prob = count / total
        gini -= prob ** 2
    return gini

def attributeGini(data, attrIndex, classIndex):
    total = len(data)
    attrVal = {}

    for row in data:
        value = row[attrIndex]
        if value not in attrVal:
            attrVal[value] = []
        attrVal[value].append(row)

    classGini = 0
    for subset in attrVal.values():
        subset_gini = giniIndex(subset, classIndex)
        classGini += (len(subset) / total) * subset_gini
    return classGini

def calculate_gini_from_csv(file_name):
    with open(file_name, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        data = [row for row in csv_reader]
        
        classIndex = len(headers) - 1
        
        target_class_gini = giniIndex(data, classIndex)
        print(f'Gini Index of target class ({headers[classIndex]}): {target_class_gini:.4f}\n')

        best_gini = float('inf')
        best_gini_attr = None

        for attrIndex in range(classIndex):
            gini_index = attributeGini(data, attrIndex, classIndex)

            print(f'Attribute: {headers[attrIndex]}')
            print(f'  Gini Index: {gini_index:.4f}\n')

            if gini_index < best_gini:
                best_gini = gini_index
                best_gini_attr = headers[attrIndex]

        print(f'Best attribute for splitting based on Gini Index {best_gini_attr} with Gini Index: {best_gini:.4f}')

calculate_gini_from_csv('data.csv')
