def sum_of_list(l):
    """
    Sum all elements in the list
    """
    if len(l) == 0:
        return 0
    else:
        return sum_of_list(l[:-1]) + l[-1]

sum_of_list([1, 1, 1, 1, 1])

# %%
def sum_all(l):
    """
    Sum all elements in the list
    including nested lists
    """
    if len(l) == 0:
        return 0
    elif isinstance(l[-1], int):
        return sum_all(l[:-1]) + l[-1]
    elif isinstance(l[-1], list):
        return sum_all(l[:-1]) + sum_all(l[-1])

for test in [
    [1, 1, 2, 2],
    [[1, 1], [2, 2]],
    [1, [1], [2, 2]],
    [1, [1], [2, [2]]],
    [1, 2, [3,4], [5,6]]
]:
    print(test, sum_all(test))


# %%
def factorial(x):
    if x == 0:
        return 1
    elif x > 0:
        return factorial(x-1)*x
    else:
        return 'Undefined'

factorial(3)


# %%
def fibonacci(N):
    if N > 2:
        return fibonacci(N-1) + fibonacci(N-2)
    elif N == 2:
        return 1
    elif N == 1:
        return 0
    else:
        raise Exception('N must be > 0')


[fibonacci(N) for N in range(1, 11)]


# %%
def sum_digits(number):
    """
    Sum all the digits of an input integer
    """
    if not isinstance(number, int):
        raise Exception('Input must be an integer')
    l = str(number)
    if len(l) == 1:
        return int(l)
    else:
        return sum_digits(int(l[1:])) + int(l[0])


# %%
def sum_positive_integers_in_2(n):
    """
    Write a Python program to calculate
    the sum of the positive integers of
    n+(n-2)+(n-4)... (until n-x =< 0)
    using recursion
    """
    if n < 0:
        return 0
    else:
        return n + sum_positive_integers_in_2(n-2)

sum_positive_integers_in_2(6)
sum_positive_integers_in_2(10)

# %%
def sum_harmonic(n):
    if n == 1:
        return 1
    else:
        return 1/n + sum_harmonic(n-1)

sum_harmonic(4)


# %%
def power(a, b):
    """
    Computes recursively a^b.
    """
    _b = abs(b)
    if _b == 0:
        return 1
    elif b > 0:
        return a*power(a, _b-1)
    elif b < 0:
        return 1/a/power(a, _b-1)
