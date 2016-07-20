import statistics
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

adjClose = []
periodicDailyReturn = []

csvfile = open('Data/table.csv', 'r')
for row in list(csvfile)[1:]:
	cells = row.split(",")
	adjClose.append(float(cells[6][:-1]))
csvfile.close()

futurePrice = [adjClose[0]]
tradingVolume = []
rsi6 = [0, 0, 0, 0, 0, 0]
rsi12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
profit = buy = 0

for i in range(len(adjClose) - 1):
	periodicDailyReturn.append(math.log1p(adjClose[i] / adjClose[i + 1] - 1))

average = statistics.mean(periodicDailyReturn)
variance = statistics.pvariance(periodicDailyReturn)
stdev = statistics.pstdev(periodicDailyReturn)
drift = average - variance / 2

plt.xlabel("Time Line")
plt.ylabel("NASDAQ Future Index")

for i in range(200):
    futurePrice.append(futurePrice[i] * math.pow(math.e, drift + stdev * norm.ppf(random.uniform(0, 1))))
    tradingVolume.append(1000 * np.abs(futurePrice[i + 1] - futurePrice[i]))
    if i > 4:
        increase = decrease = 0
        for j in range(6):
            diff = futurePrice[i - j + 1] - futurePrice[i - j]
            if diff > 0:
                increase += diff
            else:
                decrease -= diff
            rsi6_temp = increase / (increase + decrease)
        rsi6.append(rsi6_temp)
    if i > 10:
        increase = decrease = 0
        for j in range(12):
            diff = futurePrice[i - j + 1] - futurePrice[i - j]
            if diff > 0:
                increase += diff
            else:
                decrease -= diff
            rsi12_temp = increase / (increase + decrease)
        rsi12.append(rsi12_temp)
    if rsi6[i] > rsi12[i] and rsi12[i - 1] > rsi6[i - 1]:
        buy = futurePrice[i]
    if rsi6[i] < rsi12[i] and rsi12[i - 1] < rsi6[i - 1] and buy != 0:
        profit += futurePrice[i] - buy
    plt.subplot(3, 1, 1)
    plt.plot(futurePrice, color="green")
    plt.subplot(3, 1, 2)
    plt.plot(rsi6, color="blue")
    plt.plot(rsi12, color="yellow")
    plt.subplot(3, 1, 3)
    plt.bar(range(i + 1), tradingVolume, 0.6, color="blue")
    plt.draw()
    plt.pause(0.1)
    plt.clf()

print('Profit: ', profit)
plt.show()