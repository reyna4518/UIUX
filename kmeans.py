import csv
import random
def readFile(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            data.append([x, y])
    return data

def writeFile(filename, data, centroids, labels):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Point_x", "Point_y", "Cluster"])
        for i in range(len(data)):
            writer.writerow([f"{data[i][0]:.2f}", f"{data[i][1]:.2f}", labels[i]])
        writer.writerow([])
        writer.writerow(["Centroid_x", "Centroid_y"])
        for c in centroids:
            writer.writerow([f"{c[0]:.2f}", f"{c[1]:.2f}"])

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def calculateDistances(data, centroids):
    distances = []
    for i in range(len(data)):
        point_distances = []
        for j in range(len(centroids)):
            dist = distance(data[i][0], data[i][1], centroids[j][0], centroids[j][1])
            point_distances.append(dist)
        distances.append(point_distances)
    return distances

def assignCluster(distances):
    labels = []
    for dist_list in distances:
        min_index = 0
        min_dist = dist_list[0]
        for j in range(1, len(dist_list)):
            if dist_list[j] < min_dist:
                min_dist = dist_list[j]
                min_index = j
        labels.append(min_index)
    return labels

def updateCentroids(data, labels, k):
    clusters = [[] for _ in range(k)]
    for i in range(len(data)):
        clusterIndex = labels[i]
        clusters[clusterIndex].append(data[i])
    new_centroids = []
    for cluster in clusters:
        if not cluster:
            new_centroids.append([0.00, 0.00])
        else:
            x_avg = sum(point[0] for point in cluster) / len(cluster)
            y_avg = sum(point[1] for point in cluster) / len(cluster)
            new_centroids.append([round(x_avg, 2), round(y_avg, 2)])
    return new_centroids

def printDistanceMatrix(data, centroids):
    print("Distance Matrix:")
    for i in range(len(data)):
        for j in range(len(centroids)):
            dist = distance(data[i][0], data[i][1], centroids[j][0], centroids[j][1])
            print(f"{dist:.2f}", end="  ")
        print()

def kmeans(data, centroids, maxIterations=100):
    for i in range(maxIterations):
        formatted_centroids = [[f"{coord:.2f}" for coord in centroid] for centroid in centroids]
        print(f"Iteration {i + 1}: Centroids: {formatted_centroids}")
        distances = calculateDistances(data, centroids)
        labels = assignCluster(distances)
        new_centroids = updateCentroids(data, labels, len(centroids))
        if centroids == new_centroids:
            print(f"Converged at iteration {i + 1}")
            printDistanceMatrix(data, centroids)
            break
        printDistanceMatrix(data, centroids)
        centroids = new_centroids
    final_centroids = [[f"{coord:.2f}" for coord in centroid] for centroid in centroids]
    print(f"Final Centroids: {final_centroids}")
    return centroids, labels

data = readFile('ip.csv')
k = int(input("Enter the number of clusters (k): "))
initial_centroids = random.sample(data,k)
final_centroids, labels = kmeans(data, initial_centroids)
writeFile('output.csv', data, final_centroids, labels)
