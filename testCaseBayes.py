import csv
import itertools

def readFile(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return headers, data

def probCal(dataset):
    countMat = {}
    attrCounts = {}
    total = 0
    for row in dataset:
        cls = row[-1]
        if cls not in countMat:
            countMat[cls] = 0
        countMat[cls] += 1
        total += 1
        for i in range(len(row) - 1):
            key = (row[i], cls)
            if i not in attrCounts:
                attrCounts[i] = {}
            if key not in attrCounts[i]:
                attrCounts[i][key] = 0
            attrCounts[i][key] += 1
    return countMat, attrCounts, total

def condProbs(attrCounts, countMat):
    cond_probs = {}
    for i in attrCounts:
        cond_probs[i] = {}
        for key in attrCounts[i]:
            val = attrCounts[i][key]
            cls = key[1]
            cond_probs[i][key] = val / countMat[cls]
    return cond_probs

def posteriorProb(countMat, attrCounts, total, instance):
    probabilities = {}
    for cls in countMat:
        clsCount = countMat[cls]
        prob = clsCount / total
        for i in range(len(instance)):
            key = (instance[i], cls)
            if key in attrCounts[i]:
                count = attrCounts[i][key]
                prob *= count / clsCount
            else:
                prob = 0
        if cls not in probabilities or prob > probabilities[cls]:
            probabilities[cls] = prob
    prediction = None
    max_prob = -1
    for cls in probabilities:
        if probabilities[cls] > max_prob:
            max_prob = probabilities[cls]
            prediction = cls
    return prediction, probabilities

def generate_test_cases(dataset, headers):
    unique_values = []
    for i in range(len(headers) - 1):
        unique_values.append(set(row[i] for row in dataset))
    return list(itertools.product(*unique_values))

def save_output_to_csv(test_cases, predictions, probabilities, filename='output.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Test Case'] + ['Predicted Class'] + ['Probabilities'])
        for i, test_case in enumerate(test_cases):
            prob_str = ", ".join([f"{cls}: {probabilities[i].get(cls, 0):.5f}" for cls in probabilities[i]])
            writer.writerow(list(test_case) + [predictions[i]] + [prob_str])

filename = 'data.csv'
headers, dataset = readFile(filename)
countMat, attrCounts, total = probCal(dataset)
cond_probs = condProbs(attrCounts, countMat)

test_cases = generate_test_cases(dataset, headers)
predictions = []
probabilities = []

for test_case in test_cases:
    prediction, prob = posteriorProb(countMat, attrCounts, total, test_case)
    predictions.append(prediction)
    probabilities.append(prob)

save_output_to_csv(test_cases, predictions, probabilities)

print("\nOutput saved to 'output.csv'.")
