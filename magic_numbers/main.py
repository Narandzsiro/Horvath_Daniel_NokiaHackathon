from pathlib import Path


def next_magic_num(num):
    strNum = str(num)
    numLen = len(strNum)

    if strNum == "9" * numLen:
        return num + 2
    
    half = (numLen + 1) // 2
    left = strNum[:half]

    if numLen % 2 == 0:
        mirroredNum = left + left[::-1]
    else:
        mirroredNum = left + left[-2::-1]
    if mirroredNum <= strNum:
        left = str(int(left) + 1)
        if numLen % 2 == 0:
            return int(left + left[::-1])
        else:
            return int(left + left[-2::-1])
    return int(mirroredNum)

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        if '^' in line:
            base, exp = line.split('^', 1)
            num = pow(int(base), int(exp))
        else:
            num = int(line)
        print(next_magic_num(num))

if __name__ == "__main__":
    main()
