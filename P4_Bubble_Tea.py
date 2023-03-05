from sys import setrecursionlimit
setrecursionlimit(10 ** 5)

def dp(i: int, memo: list) -> int:
    if memo[i]:
        return memo[i]
    elif i < 0:
        memo[i] = 0
        return memo[i]
    elif i == 0:
        memo[i] = l[i]
        return memo[i]
    elif i == 1:
        option1 = l[i] + l[i - 1]
        option2 = l[i] + l[i - 1] - min(l[i], l[i - 1]) * 0.25
        memo[i] = min(option1, option2)
        return memo[i]
    else:
        option1 = l[i]+ dp(i=i - 1, memo=memo)
        option2 = l[i] + l[i - 1] - (min(l[i], l[i - 1]) * 0.25) + dp(i=i - 2, memo=memo)
        option3 = l[i] + l[i - 1] + l[i - 2] - (min(l[i], l[i - 1], l[i - 2]) * 0.5) + dp(i=i - 3, memo=memo)
        memo[i] = min(option1, option2, option3)
        return memo[i]

n = int(input())
l = [int(input()) for i in range(n)]
memo = [None for i in range(n)]

for i in range(n):
    dp(i=i, memo=memo)

print(round(dp(i=n - 1, memo=memo)))