from pathlib import Path


def next_magic_num(num):
    strNum = str(num)
    numLen = len(strNum)

    if strNum == "9" * numLen:
        return num + 2
    
    if numLen % 2 == 0:
        middle = numLen // 2
    else:
        middle = (numLen // 2) + 1

    nums = list(strNum)

    for i in range(middle):
        nums[numLen-1-i] = nums[i]
    
    mirroredNum = "".join(nums)

    if mirroredNum <= strNum:
        left = str(int(strNum[:middle])+1)
        if numLen % 2 == 0:
            return int(left + left[::-1])
        else:
            return int(left + left[:-1][::-1])
        
    return int(mirroredNum)


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    print(data, end="")

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        if '^' in line:
            left_side, right_side = line.split('^')
            num = pow(int(left_side), int(right_side))
        else:
            num = int(line)
        print(next_magic_num(num))

if __name__ == "__main__":
    main()
