import csv

def readFile(filePath):
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        columns = {header: [] for header in headers}
        for row in reader:
            for i, value in enumerate(row):
                columns[headers[i]].append(float(value))
    return headers, columns

def writeFile(filePath, originalData, binnedData, minMaxData, zScoreData, columnName):
    with open(filePath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"{columnName} (Original)", 
                         f"{columnName} (Binned)", 
                         f"{columnName} (Min-Max)", 
                         f"{columnName} (Z-Score)"])
        for i in range(len(originalData)):
            writer.writerow([f"{originalData[i]:.2f}", 
                             f"{binnedData[i]:.2f}", 
                             f"{minMaxData[i]:.2f}", 
                             f"{zScoreData[i]:.2f}"])

def create_bins(data, bin_size):
    bins = []
    for i in range(0, len(data), bin_size):
        bins.append(data[i:i + bin_size])
    return bins

def binning_by_mean(bins):
    smoothed_data = []
    for bin in bins:
        mean_value = sum(bin) / len(bin)
        smoothed_data.extend([mean_value] * len(bin))
    return smoothed_data

def binning_by_median(bins):
    smoothed_data = []
    for bin in bins:
        median_value = sorted(bin)[len(bin) // 2]
        smoothed_data.extend([median_value] * len(bin))
    return smoothed_data

def binning_by_boundaries(bins):
    smoothed_data = []
    for bin in bins:
        min_value = min(bin)
        max_value = max(bin)
        for value in bin:
            smoothed_data.append(min_value if abs(value - min_value) < abs(value - max_value) else max_value)
    return smoothed_data

def minMax(data, minValue, maxValue):
    minOriginal = min(data)
    maxOriginal = max(data)
    return [(x - minOriginal) * (maxValue - minValue) / (maxOriginal - minOriginal) + minValue for x in data]

def zScore(data):
    mean = sum(data) / len(data)
    stdDev = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
    return [(x - mean) / stdDev for x in data]

def binning_and_normalization(ipfilePath, opFilePath):
    headers, columns = readFile(ipfilePath)

    print("Columns:")
    for i, header in enumerate(headers):
        print(f"{i + 1}. {header}")

    selectedColumnIndex = int(input("Select column for binning and normalization: ")) - 1
    columnName = headers[selectedColumnIndex]
    colData = columns[columnName]

    print("\nBinning Method:\n1. Mean\n2. Median\n3. Boundary")
    binningChoice = int(input("Choice: "))
    bin_num = int(input("Number of Bins: "))
    bin_size = len(colData)//bin_num  
    colData.sort()

    bins = create_bins(colData, bin_size)
    if binningChoice == 1:
        binnedData = binning_by_mean(bins)
    elif binningChoice == 2:
        binnedData = binning_by_median(bins)
    else:
        binnedData = binning_by_boundaries(bins)

    print("\nNormalization:")
    minValue = float(input("Min value for Min-Max scaling: "))
    maxValue = float(input("Max value for Min-Max scaling: "))

    minMaxResult = minMax(binnedData, minValue, maxValue)
    zScoreResult = zScore(binnedData)

    writeFile(opFilePath, colData, binnedData, minMaxResult, zScoreResult, columnName)
    print(f"\nData saved to {opFilePath}")

inputFilePath = 'Folds5x2_pp.csv'
outputFilePath = 'output.csv'
binning_and_normalization(inputFilePath, outputFilePath)