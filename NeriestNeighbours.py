from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("winequality-red.csv", sep=";")
print(df.head())


quality = list(df["quality"])
data = df.drop("quality", 1)
data = normalize(data)
print(data)
row_count, column_count = data.shape


train_d, test_d, train_q, test_q = train_test_split(data, quality, train_size=0.8)
print(train_d.shape)
print(test_d.shape)
print(len(train_q))
print(len(test_q))

n_neighbours_uniform_l = []
n_neighbours_uniform_acc = []
n_neighbours_distance_l = []
n_neighbours_distance_acc = []

for n_neigh in range(1, 50):
    classifier = KNeighborsClassifier(n_neighbors=n_neigh, weights="uniform")
    classifier.fit(train_d, train_q)
    pred_q = classifier.predict(test_d)
    acc = accuracy_score(pred_q, test_q)
    n_neighbours_uniform_l.append(n_neigh)
    n_neighbours_uniform_acc.append(acc)
best_uniform_n_neigh = n_neighbours_uniform_l[n_neighbours_uniform_acc.index(max(n_neighbours_uniform_acc))]

for n_neigh in range(1, 50):
    classifier = KNeighborsClassifier(n_neighbors=n_neigh, weights="distance")
    classifier.fit(train_d, train_q)
    pred_q = classifier.predict(test_d)
    acc = accuracy_score(pred_q, test_q)
    n_neighbours_distance_l.append(n_neigh)
    n_neighbours_distance_acc.append(acc)
best_distance_n_neigh = n_neighbours_distance_l[n_neighbours_distance_acc.index(max(n_neighbours_distance_acc))]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(n_neighbours_uniform_l, n_neighbours_uniform_acc)
plt.scatter(best_uniform_n_neigh, max(n_neighbours_uniform_acc))
plt.title("best score for uniform weights is {}, for {}".format(max(n_neighbours_uniform_acc), best_uniform_n_neigh))
plt.xlabel("number of neighbors")
plt.ylabel("accuracy_score")
plt.subplot(1, 2, 2)
plt.plot(n_neighbours_distance_l, n_neighbours_distance_acc)
plt.scatter(best_distance_n_neigh, max(n_neighbours_distance_acc))
plt.title("best score for distance weights is {}, for {}".format(max(n_neighbours_distance_acc), best_distance_n_neigh))
plt.xlabel("number of neighbors")
plt.ylabel("accuracy_score")

plt.show()

