currencies = ["PZ", "WR", "SB", "SC"]

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
 
    list = [] # empty list that will store current permutation
 
    for i in lst:
        for j in lst:
            for k in lst:
                for l in lst:
                    list.append(["SC",i,j,k,l,"SC"])

    return list

def process_perms(perms):
    for perm in perms:
        if perm[-1] != "SC":
            perms.remove(perm)
    return perms

def calculate_exchange(trades, exchange_rate):
    trades_with_rate = []
    for trade in trades:
        rate = 1
        i=0
        j=1
        while i <len(trade)-1:
            rate = rate*(exchange_rate.get(trade[i]).get(trade[j]))
            trades_with_rate.append({trade:rate})
    return trades_with_rate

currency_perms = calculate_exchange(permutation(currencies), exchange_rates)

for perm in currency_perms:
    print(perm)
print("Total:" + str(len(currency_perms)))