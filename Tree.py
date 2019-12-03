from matplotlib import pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


df = pd.read_csv("winequality-red.csv", sep=";")
print(df.info())

quality = df["quality"]
data = df.drop("quality", 1)


train_d, test_d, train_q, test_q = train_test_split(data, quality, train_size=0.8)
# print(train_d)
# print(test_d)
# print(train_q)
# print(test_q)

est_l = []
max_d_l = []
max_f_l = []
score_e_l = []
score_d_l = []
score_f_l = []

for estimators in range(200, 1000, 50):
    classifier = RandomForestClassifier(n_estimators=estimators)
    classifier.fit(train_d, train_q)
    prediction = classifier.predict(test_d)
    acc = accuracy_score(test_q, prediction)
    score_e_l.append(acc)
    est_l.append(estimators)

best_est = est_l[score_e_l.index(max(score_e_l))]
print(best_est)

for max_f in range(3, 10):
    classifier = RandomForestClassifier(n_estimators=best_est, max_features=max_f)
    classifier.fit(train_d, train_q)
    prediction = classifier.predict(test_d)
    acc = accuracy_score(test_q, prediction)
    score_f_l.append(acc)
    max_f_l.append(max_f)

best_max_f = max_f_l[score_f_l.index(max(score_f_l))]
print(best_max_f)

for max_d in range(1, 30):
    classifier = RandomForestClassifier(n_estimators=best_est, max_features=best_max_f, max_depth=max_d)
    classifier.fit(train_d, train_q)
    prediction = classifier.predict(test_d)
    acc = accuracy_score(test_q, prediction)
    score_d_l.append(acc)
    max_d_l.append(max_d)

best_depth = max_d_l[score_d_l.index(max(score_d_l))]
print(best_depth)


plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(est_l, score_e_l)
plt.scatter(best_est, max(score_e_l))
plt.title("Best score: {}, for {}".format(max(score_e_l), best_est))
plt.xlabel("n_estimators")
plt.ylabel("score")
plt.subplot(1, 3, 2)
plt.plot(max_f_l, score_f_l)
plt.scatter(best_max_f, max(score_f_l))
plt.title("Best score: {}, for {}".format(max(score_f_l), best_max_f))
plt.xlabel("max_features")
plt.ylabel("score")
plt.subplot(1, 3, 3)
plt.plot(max_d_l, score_d_l)
plt.scatter(best_depth, max(score_d_l))
plt.title("Best score: {}, for {}".format(max(score_d_l), best_depth))
plt.xlabel("max_depth")
plt.ylabel("score")
plt.show()





