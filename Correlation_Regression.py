import csv

def readFile(filePath):
    with open(filePath, mode="r") as file:
        robj = csv.reader(file)
        headers = next(robj)
        data = list(robj)
    return headers, data

def extractColumn(data, index):
    return [float(row[index]) for row in data]

def linearRegression(x, y):
    n = len(x)
    sumX = sum(x)
    sumY = sum(y)
    sumXY = sum(x[i] * y[i] for i in range(n))
    sumXX = sum(x[i] ** 2 for i in range(n))
    
    a = (sumY * sumXX - sumX * sumXY) / (n * sumXX - sumX ** 2)
    b = (n * sumXY - sumX * sumY) / (n * sumXX - sumX ** 2)
    
    return a, b

def correlation(x, y):
    n = len(x)
    meanX = sum(x) / n
    meanY = sum(y) / n
    sumXY = sum((x[i] - meanX) * (y[i] - meanY) for i in range(n))
    sumXX = sum((x[i] - meanX) ** 2 for i in range(n))
    sumYY = sum((y[i] - meanY) ** 2 for i in range(n))
    corr = sumXY / ((sumXX * sumYY) ** 0.5)
    return corr

def getColumnsToProcess(headers):
    for i, header in enumerate(headers):
        print(f"{i+1}: {header}")
    
    x_index = int(input("X Column: ").strip()) - 1
    y_index = int(input("Y Column: ").strip()) - 1
    
    return x_index, y_index

def main():
    filePath = "Folds5x2_pp.csv"
    headers, data = readFile(filePath)
    x_index, y_index = getColumnsToProcess(headers)
    x = extractColumn(data, x_index)
    y = extractColumn(data, y_index)
    
    intercept, slope = linearRegression(x, y)
    print(f"Slope: {slope:.2f}")
    print(f"Intercept: {intercept:.2f}")
    print(f"Y = {slope:.2f} X + {intercept:.2f}")
    
    corr = correlation(x, y)
    print(f"Correlation: {corr:.2f}")

if __name__ == "__main__":
    main()
