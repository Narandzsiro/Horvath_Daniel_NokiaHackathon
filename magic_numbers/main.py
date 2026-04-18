import sys
from pathlib import Path

def next_magic_num(num):
    strNum = str(num)
    numLen = len(strNum)
    
    if num < 9:
        return num + 1
        
    half_idx = (numLen + 1) // 2
    left_part = strNum[:half_idx]
    
    def make_pali(left_str):
        if numLen % 2 == 0:
            return left_str + left_str[::-1]
        else:
            return left_str + left_str[:-1][::-1]

    candidate_str = make_pali(left_part)
    candidate_int = int(candidate_str)
    
    if candidate_int > num:
        return candidate_int
    
    new_left_int = int(left_part) + 1
    new_left_str = str(new_left_int)
    
    if len(new_left_str) > len(left_part):
        return 10**numLen + 1
    
    return int(make_pali(new_left_str))

def main():
    path = Path("input.txt")
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")
    results = []

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if '^' in line:
            base_str, exp_str = line.split('^', 1)
            num = pow(int(base_str), int(exp_str))
        else:
            num = int(line)
        
        results.append(str(next_magic_num(num)))

    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()