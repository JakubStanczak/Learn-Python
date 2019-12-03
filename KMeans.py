from matplotlib import pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


def normalize(lst):
    return [(l - min(lst))/(max(lst)-min(lst)) for l in lst]


df = pd.read_csv("winequality-red.csv", sep=";")
print(df.info())
f1 = "fixed acidity"
f2 = "residual sugar"

test_df = df.iloc[:1000]

points = list(zip(test_df[f1], test_df[f2]))

model = KMeans(n_clusters=5)
model.fit(points)
centers = model.cluster_centers_
pred = model.predict(points)

cx = []
cy = []
for c in centers:
    cx.append(c[0])
    cy.append(c[1])


qua_norm = normalize(list(test_df["quality"]))

print(list(test_df["quality"]))
print(qua_norm)

plt.scatter(test_df[f1], test_df[f2], alpha=0.2, marker="o", c=pred)
plt.xlabel(f1)
plt.ylabel(f2)
plt.scatter(cx, cy, marker="v", c="r")


plt.show()
