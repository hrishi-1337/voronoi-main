import pickle
from sympy.geometry import *
import random
import os
import time
import pandas as pd
import naive
import dnq
import fortune
import numpy as np
import matplotlib.pyplot as plt

def main():
    bound = 1000
    naive_dict, dnq_dict, fortune_dict = {}, {}, {}
    # n = [2, 5, 10, 15]
    n = [2, 5, 10, 20, 30, 40, 60, 80]
    # # gen(n)
    # points = read(10, 1)
    # naive.voronoi(points, bound)
    # dnq.voronoi(points, bound)
    # v = fortune.Voronoi(points, bound)
    # v.compute()
    
    for i in n:
        runtime1, runtime2, runtime3 = [], [], []
        for j in range(1):
            if j%10 == 0:
                print("Running size "+str(i)+" Iteration "+str(j))
            points = read(i, j)
    #         # begin1 = time.time()
            naive.voronoi(points, bound)
    #         # end1 = time.time()
              # runtime1.append(end1 - begin1)
            # begin2 = time.time()
            try:
                dnq.voronoi(points, bound)
            except:
                continue
            # end2 = time.time()
            # runtime2.append(end2 - begin2)
    #         begin3 = time.time()
            v = fortune.Voronoi(points, bound)
            v.compute()
            # end3 = time.time()
            # runtime3.append(end3 - begin3)
        # naive_dict[i] = runtime1
        # dnq_dict[i] = runtime2
        # fortune_dict[i] = runtime3
    # df1 = pd.DataFrame(naive_dict.items()) 
    # df2 = pd.DataFrame(dnq_dict.items()) 
    # df3 = pd.DataFrame(fortune_dict.items()) 
    # writer = pd.ExcelWriter("output/Runtime.xlsx")
    # df1.to_excel(writer, "naive_runtime")
    # df2.to_excel(writer, "dnq_runtime")
    # df3.to_excel(writer, "fortune_runtime")
    # writer.save()
    path = os.path.join('output', "dnq.data")
    with open(path, 'wb') as f:
        pickle.dump(dnq_dict, f)

def plot():
    path = os.path.join('output', "naive_1.data")
    with open(path, 'rb') as f:
        naive_dict = pickle.load(f)
    path = os.path.join('output', "dnq.data")
    with open(path, 'rb') as f:
        dnq_dict = pickle.load(f)
    path = os.path.join('output', "fortune_1.data")
    with open(path, 'rb') as f:
        fortune_dict = (pickle.load(f))
    fig, ax = plt.subplots()
    x_positions = range(1, len(naive_dict) + 1)
    n = [2, 5, 10, 20, 30, 40, 60, 80]

    # for i, key in enumerate(naive_dict):
    #     bplot1 = ax.boxplot(naive_dict[n[i]], positions=[x_positions[i]], patch_artist=True)
    
    for i, key in enumerate(dnq_dict):
        bplot2 = ax.boxplot(dnq_dict[n[i]], positions=[x_positions[i]], patch_artist=True)
    
    for i, key in enumerate(fortune_dict):
        bplot3 = ax.boxplot(fortune_dict[n[i]], positions=[x_positions[i]], patch_artist=True)

    # for patch in bplot1['boxes']:
    #     patch.set_facecolor('red')

    for patch in bplot2['boxes']:
        patch.set_facecolor('yellow')

    for patch in bplot3['boxes']:
        patch.set_facecolor('blue')

    y_axis = [0, 25, 50, 75, 100, 125, 150, 175, 2]
    ax.set_xticks(x_positions)
    ax.set_xticklabels(sorted(dnq_dict.keys()))
    ax.set_yticklabels(y_axis)
    
    ax.set_title('Divide \& Conquer and Fortune\'s algorithm Runtime Comparison')
    ax.set_xlabel('Number of sites')
    ax.set_ylabel('Time (seconds)')
    fig.savefig('plot/dnq_fortune_boxplot.png')
    plt.show()

def gen(n):
    for i in n:  
        for j in range(30):
            x_values = random.sample(range(2, 998), i)
            y_values = random.sample(range(2, 998), i)
            points = [Point(x, y) for x, y in zip(x_values, y_values)]
            path = os.path.join('data', str(i)+"_"+str(j)+".data")
            with open(path, 'wb') as f:
                pickle.dump(points, f)

def read(i, j):
    path = os.path.join('data', str(i)+"_"+str(j)+".data")
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

if __name__ == "__main__":
    main()
    # gen([15, 19])
    # plot()