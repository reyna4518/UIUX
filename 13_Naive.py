import csv
import math

def read_csv(file_path):
    dataset = []
    header = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            dataset.append(row)
    return dataset, header

def probCal(dataset):
    countMat = {}
    attrCounts = {}
    numStats = {}
    total = 0

    for row in dataset:
        cls = row[-1]
        countMat[cls] = countMat.get(cls, 0) + 1
        total += 1

        for i in range(len(row) - 1):
            value = row[i]
            if value.replace('.', '', 1).isdigit():
                value = float(value)
                if i not in numStats:
                    numStats[i] = {}
                if cls not in numStats[i]:
                    numStats[i][cls] = []
                numStats[i][cls].append(value)
            else:
                key = (value, cls)
                if i not in attrCounts:
                    attrCounts[i] = {}
                attrCounts[i][key] = attrCounts[i].get(key, 0) + 1

    for i, clsValues in numStats.items():
        for cls, values in clsValues.items():
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            numStats[i][cls] = (mean, math.sqrt(variance))

    return countMat, attrCounts, numStats, total, header, attrCounts, numStats

def gaussianProb(x, mean, std):
    if std == 0:
        return 1.0 if x == mean else 0.0
    exponent = math.exp(-((x - mean) ** 2) / (2 * std ** 2))
    return (1 / (math.sqrt(2 * math.pi) * std)) * exponent

def classify(test_instance, countMat, attrCounts, numStats, total):
    classProbs = {}

    for cls in countMat:
        classProbs[cls] = countMat[cls] / total
        for i in range(len(test_instance)):
            value = test_instance[i]

            if value.replace('.', '', 1).isdigit():
                value = float(value)
                if i in numStats and cls in numStats[i]:
                    mean, std = numStats[i][cls]
                    classProbs[cls] *= gaussianProb(value, mean, std)
            else:
                key = (value, cls)
                if i in attrCounts and key in attrCounts[i]:
                    classProbs[cls] *= attrCounts[i][key] / countMat[cls]
                else:
                    classProbs[cls] *= 1e-6

    return max(classProbs, key=classProbs.get), classProbs

file_path = 'data1.csv'
dataset, header = read_csv(file_path)

countMat, attrCounts, numStats, total, header, attrCounts, numStats = probCal(dataset)

test_instance = []
for i in range(len(header) - 1):
    value = input(f"Enter value for {header[i]}: ")
    test_instance.append(value)

print("\nTest Instance Attributes and Values:")
for i in range(len(header) - 1):
    print(f"{header[i]}: {test_instance[i]}")

predicted_class, probabilities = classify(test_instance, countMat, attrCounts, numStats, total)

print(f"\nPredicted class: {predicted_class}")

print("Probabilities:")
for cls, prob in probabilities.items():
    print(f"  {cls}: {prob:.11f}")
