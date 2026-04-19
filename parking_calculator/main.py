import math
from datetime import datetime
from pathlib import Path

def calculate_parking_fee(entry_time, exit_time):
    duration = exit_time - entry_time
    total_seconds = duration.total_seconds()
    total_minutes = math.ceil(total_seconds / 60)
    
    if total_minutes >= 1440:
        days = total_minutes // 1440
        remaining_minutes = total_minutes % 1440
    
        if remaining_minutes == 0:
            return days * 10000
        else:

            return (days * 10000) + calculate_sub_24h_fee(remaining_minutes)

    return calculate_sub_24h_fee(total_minutes)

def calculate_sub_24h_fee(minutes):
    if minutes <= 30:
        return 0
    
    fee = 0
    if minutes < 180:
        fee = (minutes - 30) * 5
    else:
        fee = 900 + (minutes - 180) * (500 / 60)
        
    return math.ceil(fee)

def main():
    input_file = Path("input.txt")
    output_file = Path("parking_report.txt")
    
    if not input_file.exists():
        print("A forrásfájl nem található!")
        return

    results = []
    lines = input_file.read_text(encoding="utf-8").splitlines()

    for line in lines[1:]:
        if not line or "RENSZAM" in line or "=" in line:
            continue
            
        parts = line.split('\t')
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) == 3:
            rendszam = parts[0]
            entry = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S")
            exit = datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S")
            
            fee = calculate_parking_fee(entry, exit)
            
            if isinstance(fee, str):
                results.append(f"{rendszam}: {fee}")
            else:
                duration = exit - entry
                results.append(f"{fee} forint")


    output_text = "\n".join(results)
    output_file.write_text(output_text, encoding="utf-8")
    print(output_text)

if __name__ == "__main__":
    main()