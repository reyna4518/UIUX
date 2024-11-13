import csv

def readCSV(filePath):
    data = {}
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for header in headers:
            data[header] = []

        for row in reader:
            for i, val in enumerate(row):
                try:
                    data[headers[i]].append(float(val))
                except ValueError:
                    data[headers[i]].append(None)

    return headers, data

def calcFiveNum(data):
    sortedData = sorted([x for x in data if x is not None])
    n = len(sortedData)

    minVal = sortedData[0]
    maxVal = sortedData[-1]
    median = (sortedData[n // 2] + sortedData[(n - 1) // 2]) / 2
    q1 = sortedData[n // 4]
    q3 = sortedData[(3 * n) // 4]
    iqr = q3 - q1

    return minVal, q1, median, q3, maxVal, iqr

def findOutliers(data, q1, q3, iqr):
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = [x for x in data if x is not None and (x < lower or x > upper)]

    return outliers, lower, upper

def boxPlot(filePath):
    headers, data = readCSV(filePath)
    print("\nAvailable Columns:")
    for i, col in enumerate(headers):
        print(f"{i + 1}. {col}")

    colIndex = int(input("Select column number to analyze: ")) - 1
    colName = headers[colIndex]
    values = data[colName]

    minVal, q1, median, q3, maxVal, iqr = calcFiveNum(values)
    outliers, lower, upper = findOutliers(values, q1, q3, iqr)

    print(f"\nBox Plot of '{colName}':")
    print(f"Min: {minVal:.2f}")
    print(f"Q1: {q1:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Q3: {q3:.2f}")
    print(f"Max: {maxVal:.2f}")

    print(f"IQR: {iqr:.2f}, Lower Bound: {lower:.2f}, Upper Bound: {upper:.2f}")
    print(f"Outliers: {outliers}")

filePath = 'Folds5x2_pp.csv'
boxPlot(filePath)
