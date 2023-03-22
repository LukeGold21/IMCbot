currencies = ["PZ", "WR", "SB", "SC"]
my_currency = "SC"

exchange_rates = {"PZ":{"PZ":1, "WR":0.5, "SB":1.45, "SC":0.75},
                  "WR":{"PZ":1.95, "WR":1, "SB":3.1, "SC":1.49},
                  "SB":{"PZ":0.67, "WR":0.31, "SB":1, "SC":0.48},
                  "SC":{"PZ":1.34, "WR":0.64, "SB":1.98, "SC":1}}


# Python function to print permutations of a given list
def permutation(lst):
 
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
 
    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]
 
    # Find the permutations for lst if there are
    # more than 1 characters
 
    ls = [] # empty list that will store current permutation
 
    for i in lst:
        for j in lst:
            for k in lst:
                for l in lst:
                    ls.append([my_currency,i,j,k,l,my_currency])

    return ls

def process_perms(perms):
    ok_perms = []
    for perm in perms:
        remove = False
        for i in range(0, len(perm)-1):
            if str(perm[i]) == str(perm[i+1]):
                remove = True
        if not remove:
            ok_perms.append(perm)        
    return ok_perms

def calculate_exchange(trades, exchange_rate):
    trades_with_rate = []
    for trade in trades:
        rate = 1
        i=0
        #print("\n" + str(trade), end = '')
        while i <len(trade)-1:
            #print("  " + str(exchange_rate.get(trade[i]).get(trade[i + 1])), end = '')
            rate = rate*(exchange_rate.get(trade[i]).get(trade[i+1]))
            i += 1
        trades_with_rate.append((trade, rate))
    return trades_with_rate

currency_perms = sorted((calculate_exchange(permutation(currencies), exchange_rates)), key=lambda x: x[1])

for perm in currency_perms:
    print(perm)
print("Total:" + str(len(currency_perms)))