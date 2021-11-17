import pandas as pd
import random

adj = []
size = 0


def random_index(i):
    while True:
        ind = random.randint(0, size - 1)
        if adj[i][ind] == 1:
            return ind


def monte_carlo(N, S, E):
    visits = [0 for i in range(size)]
    visits[N] += 1
    neighbor = N
    for i in range(S):
        if random.uniform(0, 1) >= E:
            neighbor = random_index(neighbor)
            visits[neighbor] += 1
        if random.uniform(0, 1) <= E:
            neighbor = N
            visits[N] += 1
    for i in range(size):
        visits[i] /= S
    return visits


def main(N, S, E):
    n_type = []
    for i in range(size):
        if adj[N][i] == 1:
            n_type.append('current friend')
        elif i == N:
            n_type.append('node N')
        else:
            n_type.append('recommended friend')
    v = monte_carlo(N, S, E)
    x = [[i, v[i], n_type[i]] for i in range(size)]
    x.sort(key=lambda t: t[1], reverse=True)
    df = pd.DataFrame(data=x, columns=['node', 'score', 'node type']).head(10)
    print(df.to_string(index=False))
    print()


def create_adj():
    F = input("Adjacency matrix txt file: ")
    global size, adj
    adj = []
    with open(F) as file:
        for line in file:
            adj.append([int(i) for i in line.strip().split(' ')])
    size = adj[0][0]
    adj.pop(0)


create_adj()
while True:
    while True:
        n = input("Friend node to recommend: ")
        if int(n) < 0 or int(n) >= size:
            print("Error: Outside of matrix size!")
        else:
            break
    s = input("Number of steps for Monte Carlo walk: ")
    e = input(f"Probability of going back to node {n} at each step (decimal): ")
    main(int(n), int(s), float(e))
    if input("Find another friend recommendation? (y/n): ") == 'n':
        break
    if input("Use a different adjacency matrix? (y/n): ") == 'y':
        create_adj()
