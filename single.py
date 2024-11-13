import csv

def readFile(filename):
    labels = []
    distMat = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        labels = header[1:]

        n = len(labels)
        distMat = [[float('inf')] * n for _ in range(n)]

        for i, row in enumerate(reader):
            for j in range(i + 1):
                value = row[j + 1]
                dist = float(value) if value != '-' else float('inf')
                distMat[i][j] = dist
                distMat[j][i] = dist

    return labels, distMat

def clusterDistSingleLinkage(cluster1, cluster2, distMat):
    minDist = float('inf')
    for i in cluster1:
        for j in cluster2:
            dist = distMat[min(i, j)][max(i, j)]
            if dist < minDist:
                minDist = dist
    return minDist

def distMatUpdateSingleLinkage(distMat, clusters):
    numClusters = len(clusters)
    for i in range(numClusters):
        for j in range(i + 1, numClusters):
            dist = clusterDistSingleLinkage(clusters[i], clusters[j], distMat)
            distMat[i][j] = dist
            distMat[j][i] = dist

def printDistMat(labels, distMat, clusters):
    print("\nDistance Matrix:")
    header = " " * 10
    for i in range(len(clusters)):
        header += f"{labels[i]:>10}"
    print(header)
    
    for i in range(len(clusters)):
        row = f"{labels[i]:>10} "
        for j in range(len(clusters)):
            if distMat[i][j] == float('inf'):
                row += "       -"
            else:
                row += f"{distMat[i][j]:>10.2f}"
        print(row)
    print()

def clusteringSingleLinkage(labels, distMat):
    clusters = [[i] for i in range(len(labels))]
    merge_count = 1 
    printDistMat(labels, distMat, clusters)

    while len(clusters) > 1:
        minDist = float('inf')
        closestPair = None

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = clusterDistSingleLinkage(clusters[i], clusters[j], distMat)
                if dist < minDist:
                    minDist = dist
                    closestPair = (i, j)

        i, j = closestPair
        merged_cluster = clusters[i] + clusters[j]
        clusters[i] = merged_cluster
        del clusters[j]

        merged_label = f"({labels[i]},{labels[j]})"
        labels[i] = merged_label
        del labels[j]

        distMatUpdateSingleLinkage(distMat, clusters)

        print(f"Step {merge_count}: Merged clusters {labels[i]} at distance {minDist:.2f}")
        printDistMat(labels, distMat, clusters)
        merge_count += 1

    if len(clusters) == 1:
        print(f"Final cluster: {labels[0]}")

def main():
    filename = 'input.csv'
    labels, distMat = readFile(filename)
    clusteringSingleLinkage(labels, distMat)

if __name__ == "__main__":
    main()
