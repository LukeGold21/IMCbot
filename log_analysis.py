import sys


total_buy = 0
count_buy = 0
total_sell = 0
count_sell = 0
f = open("logs/"+sys.argv[1], 'r')
contents = f.readlines()

for line in contents:
    splitline = line.split(" ")
    if "BUY" in splitline:
        count_buy += 1
        total_buy = total_buy + int(splitline[-1])
    elif "SELL" in splitline:
        count_sell += 1
        total_sell =  total_sell + int(splitline[-1])

print("no Sell:" + str(count_sell))
print("no Buy:" + str(count_buy))
print("pnl:" + str(total_sell-total_buy))
