def collatz_steps(n):
    def inner(n, steps):
        return steps if n <= 1 else inner(
            3 * n + 1 if n % 2 else n / 2, steps + 1)
    return inner(n, 0)


assert collatz_steps(0) == 0
assert collatz_steps(1) == 0
assert collatz_steps(16) == 4
assert collatz_steps(12) == 9
assert collatz_steps(1000000) == 152
