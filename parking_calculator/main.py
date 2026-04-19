from pathlib import Path
from datetime import datetime
import math


def Parsing(arrival, departure):
    format_string = "%Y-%m-%d %H:%M:%S"

    d1 = datetime.strptime(arrival, format_string)
    d2 = datetime.strptime(departure, format_string)

    if d1 > d2:
        return
    
    difference = d2-d1
    return difference.total_seconds() / 60

def FeeCalculation(timeSpent):
    fee = 0

    if timeSpent <= 30:
        return 0
    
    days = timeSpent // 1440
    remainingMinutes = timeSpent % 1440
    fee += days * 10000

    if remainingMinutes >= 30:
        remainingMinutes -= 30
    else:
        return int(round(fee))
    
    if remainingMinutes > 180:
        remainingMinutes -= 180
        fee += math.ceil(180 / 60) * 300 
        fee += math.ceil(remainingMinutes/60) * 500
    else:
        fee += math.ceil(remainingMinutes/60) * 300
        
    return int(round(fee))

def main():
    file_path = Path("input.txt")
    
    if not file_path.exists():
        print("Hiba: A(z) \"input.txt\" fájl nem található!")
        return

    content = file_path.read_text(encoding="utf-8").splitlines()
    dataRows = content[2:]
    results = []

    for row in dataRows:
        if not row.strip():
            continue
            
        data = row.split()
        
        if len(data) == 5:
            licensePlate = data[0]
            arrival = f"{data[1]} {data[2]}"
            departure = f"{data[3]} {data[4]}"
            
            total_minutes = Parsing(arrival, departure)

            if total_minutes is not None:
                
                fee = FeeCalculation(total_minutes)
                results.append(f"{licensePlate}\t\t{fee}")
                print(f"{licensePlate}\t\t{fee}")
            else:
                results.append(f"{licensePlate}: hibás időpontok")

    Path("parking_report.txt").write_text(f"\n".join(results), encoding="utf-8")

if __name__ == "__main__":
    main()