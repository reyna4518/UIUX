import csv

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


filename = 'data.csv'
headers, dataset = readFile(filename)
countMat, attrCounts, total = probCal(dataset)
cond_probs = condProbs(attrCounts, countMat)

print("Conditional Probabilities:")
for i in cond_probs:
    for key in cond_probs[i]:
        val, cls = key
        print(f"P({headers[i]}={val}|Class={cls}) = {cond_probs[i][key]:.5f}")
    print()

print("\nAttributes:")
for i in range(len(headers) - 1):
    unique_values = []
    for row in dataset:
        if row[i] not in unique_values:
            unique_values.append(row[i])
    print(f"{headers[i]}: {unique_values}")
print()

print("Enter attributes for test:")
test_instance = []
for i in range(len(headers) - 1):
    val = input(f"{headers[i]}: ")
    test_instance.append(val)

prediction, probabilities = posteriorProb(countMat, attrCounts, total, test_instance)

print("\nPredicted class:", prediction)
print("Probabilities:")
for cls in probabilities:
    print(f"Class {cls}: {probabilities[cls]:.5f}")