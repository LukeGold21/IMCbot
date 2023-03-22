import sys, glob, os


total_buy = 0
count_buy = 0
total_sell = 0
count_sell = 0

list_of_files = glob.glob('../IMCBot/logs/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


f = open(latest_file, 'r')
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
