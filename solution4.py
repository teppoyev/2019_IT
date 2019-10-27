import numpy as np
import matplotlib.pyplot as plt

def check_if_pareto_efficiency(index, X, functions):
    for j in range(X.shape[0]):
        if np.all(functions(X[j]) <= functions(X[index])) & np.any(functions(X[j]) < functions(X[index])):
            return False
    return True

def get_pareto_indices(X):
    for i in range(X.shape[1]):
        if check_if_pareto_efficiency(i, X, f):
            yield i

def get_pareto_vectors(X):
    for i, col in enumerate(X):
        if check_if_pareto_efficiency(i, X, f):
            yield col

def get_not_pareto_vectors(X):
    for i, col in enumerate(X):
        if not check_if_pareto_efficiency(i, X, f):
            yield col

if __name__ == "__main__":
    #n = np.random.randint(5, 20, 2)[0]
    #m = np.random.randint(3, 10, 1)[0]
    n = 3
    m = 3
    X = np.random.randint(20, size=(n, m))

    print(n)
    print(m)
    print(X)
    print()

    k = m
    def funs(i):
        def fun(x):
            if i < len(x):
                return x[i]
            else:
                print("Error: ", x, i)
        return fun
    def f(x):
        funcs = [funs(i) for i in range(k)]
        return np.array([funcs[j](x) for j in range(k)])

    for i, col in enumerate(X):
        if check_if_pareto_efficiency(i, X, f):
            print(col)

    vec_pareto = get_pareto_vectors(X)
    vec_nopareto = get_not_pareto_vectors(X)

    fig = plt.figure(figsize=[10, 10])
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.yaxis.grid(True)
    ax.set_yticks((5, 10, 15, 20))
    plt.thetagrids(np.arange(0, 360, 360.0 / m), labels=np.arange(0, m, 1))

    x = 2 * np.pi / m * np.arange(0, m, 1)
    x = np.append(x, 0)

    for vec in vec_nopareto:
        y = np.append(vec, vec[0])
        ax.plot(x, y, color="green")

    for vec in vec_pareto:
        y = np.append(vec, vec[0])
        ax.plot(x, y, color="red")

    plt.show()