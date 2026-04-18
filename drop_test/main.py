from pathlib import Path

def min_num_of_drops(n, h):
    if h == 0:
        return 0
    if n == 1:
        return h

    dp = [[0] * (n + 1) for _ in range(h + 1)]
    
    m = 0
    while dp[m][n] < h:
        m += 1
        for i in range(1, n + 1):
            dp[m][i] = dp[m-1][i-1] + 1 + dp[m-1][i]
            
    return m

def main():
    input_path = Path("input.txt")
    data = input_path.read_text(encoding="utf-8").splitlines()
    
    for line in data:
        parts = line.replace(',', ' ').split()
        if len(parts) == 2:
            n = int(parts[0])
            h = int(parts[1])
            result = min_num_of_drops(n, h)
            print(f"{result}")


if __name__ == "__main__":
    main()