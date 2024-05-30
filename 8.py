import numpy as np
from colorama import Fore, Style


def show_step(t, h, R, counter, y, color=Fore.WHITE):
    print(color + "%6f\t%6f\t%6e\t%d\t%s\t" % (t, h, R, counter[0], '\t'.join('%6f' % y_i for y_i in y)))
    print(Style.RESET_ALL, end='')


def show_correct(S, color=Fore.GREEN):
    print(color + S + Style.RESET_ALL)


def extract_function(code_str):
    mini_namespace = {'np': np}
    initial_keys = set(mini_namespace.keys())
    initial_keys.add('__builtins__')

    exec(code_str, mini_namespace)

    new_keys = set(mini_namespace.keys()) - initial_keys

    if len(new_keys) == 1:
        new_key = new_keys.pop()
        if callable(mini_namespace[new_key]):
            return mini_namespace[new_key]
    return None


def read_input():
    t_0 = float(input())
    T = float(input())
    h_0 = float(input())
    N_x = int(input())
    eps = float(input())
    n = int(input())

    code_with_func = "\n".join([input() for i in range(n + 3)])
    foo = extract_function(code_with_func)
    initial_conditions = np.array(list(map(float, input().split())))

    return t_0, T, h_0, N_x, eps, foo, initial_conditions
def heun_step(rhs_func, t, y, h, counter):
    k1 = rhs_func(t, y, counter)
    k2 = rhs_func(t + h, y + h * k1, counter)
    return y + h/2 * (k1 + k2)


def solve_ode_heun(rhs_func, t_0, T, h_0, N_x, eps, initial_conditions):
    t = t_0
    y = initial_conditions
    h = h_0
    counter = [0]
    R = 0

    show_step(t, h, R, counter, y, Fore.RED)
    step_BUFFER = heun_step(rhs_func, t, y, h, counter)
    while t < T and counter[0] < N_x:
        full_step = step_BUFFER
        half_h = h/2
        half_step_1 = heun_step(rhs_func, t, y, half_h, counter)
        half_step_2 = heun_step(rhs_func, t + half_h, half_step_1, half_h, counter)

        R = np.linalg.norm(half_step_2 - full_step, ord=2) / 3
        if R < eps:
            t += h
            y = half_step_2
            show_step(t, h, R, counter, y, Fore.RED)
            if 64 * R < eps:
                h = min(2*h, T-t) # no more than remaining t
        else:
            h = max(h/2, 1e-15) # no less than reasonably small float
            step_BUFFER = half_step_1
    print(np.linalg.norm(y - np.array([0.693090,1.732764, 5.440465]), 2))


def main():
    t_0, T, h_0, N_x, eps, rhs_func, initial_conditions = read_input()
    solve_ode_heun(rhs_func, t_0, T, h_0, N_x, eps, initial_conditions)


if __name__ == "__main__":
    main()