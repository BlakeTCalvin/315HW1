import itertools
import numpy as np

# dictionaries to hold item and values
itemCounts = {}
frequentItemCounts = {}
pairCounts = {}
frequentPairCounts = {}
pairConfidenceValues = {}
tripleCounts = {}
frequentTripleCounts = {}
tripleConfidenceValues = {}

# our support threshold
supportThreshold = 8

# finding the frequency of all items
# marketBasketData = open("inputfiles/browsing-data.txt", "r")
marketBasketData = open("inputfiles/browsingdata_50baskets.txt", "r")
for line in marketBasketData:
    basket = line.strip().split(' ')
    for item in basket:
        if item in itemCounts.keys():
            itemCounts[item] += 1
        else:
            itemCounts[item] = 1
marketBasketData.close()

# saving the frequent items to a new dictionary
for item in itemCounts:
    if itemCounts[item] >= supportThreshold:
        frequentItemCounts[item] = itemCounts[item] 

# generating all possible pairs from the frequent items
allFrequentPairs = list(itertools.combinations(frequentItemCounts.keys(), 2))

# checking frequency of pairs
# marketBasketData = open("inputfiles/browsing-data.txt", "r")
marketBasketData = open("inputfiles/browsingdata_50baskets.txt", "r")
for line in marketBasketData:
    basket = line.strip().split(' ')
    for pair in allFrequentPairs:
        if pair[0] in basket:
            if pair[1] in basket:
                if pair in pairCounts.keys():
                    pairCounts[pair] += 1
                else:
                    pairCounts[pair] = 1
marketBasketData.close()

# saving the frequent pairs to a new dictionary
for pair in pairCounts:
    if pairCounts[pair] >= supportThreshold:
        frequentPairCounts[pair] = pairCounts[pair] 

# checking the confidences of x to y and also y to x for pairs
for pair in frequentPairCounts:
    # calcualtes the pair frequency and divides it by x frequency to find the confidence for each pair of x => y
    pairConfidenceValues[(pair[0], pair[1])] = frequentPairCounts[pair] / frequentItemCounts[pair[0]]
    
    # calcualtes the pair frequency and divides it by y frequency to find the confidence for each pair of y => x
    pairConfidenceValues[(pair[1], pair[0])] = frequentPairCounts[pair] / frequentItemCounts[pair[1]]

# sorting our confidence values
pairConfidenceValues = dict(sorted(pairConfidenceValues.items(), key = lambda item: item[1], reverse=True))

# finding our frequent items for triples and then setting the triples 
allTripleItemsFromPairs = set(itertools.chain.from_iterable(frequentPairCounts))
allTriplesCombinations = list(itertools.combinations(allTripleItemsFromPairs, 3))

# checking frequency of triples
# marketBasketData = open("inputfiles/browsing-data.txt", "r")
marketBasketData = open("inputfiles/browsingdata_50baskets.txt", "r")
for line in marketBasketData:
    basket = line.strip().split(' ')
    for triple in allTriplesCombinations:
        if triple[0] in basket:
            if triple[1] in basket:
                if triple[2] in basket:
                    if triple in tripleCounts.keys():
                        tripleCounts[triple] += 1
                    else:
                        tripleCounts[triple] = 1
marketBasketData.close()

# saving the frequent triples to a new dictionary
for triple in tripleCounts:
    if tripleCounts[triple] >= supportThreshold:
        frequentTripleCounts[triple] = tripleCounts[triple] 

# checking the confidences of (x,y) to z, (x,z) to y, and (y,z) to x.
for triple in frequentTripleCounts:
    # calcualtes the pair frequency and divides it by x frequency to find the confidence for each pair of (x,y) => z
    tripleConfidenceValues[(triple[0], triple[1], triple[2])] = frequentTripleCounts[triple] / frequentItemCounts[(triple[2])]
    
    # calcualtes the pair frequency and divides it by x frequency to find the confidence for each pair of (x,z) => y
    tripleConfidenceValues[(triple[0], triple[2], triple[1])] = frequentTripleCounts[triple] / frequentItemCounts[(triple[1])]
    
    # calcualtes the pair frequency and divides it by x frequency to find the confidence for each pair of (y,z) => x
    tripleConfidenceValues[(triple[1], triple[2], triple[0])] = frequentTripleCounts[triple] / frequentItemCounts[(triple[0])]

# sorting our confidence values
tripleConfidenceValues = dict(sorted(tripleConfidenceValues.items(), key = lambda item: item[1], reverse=True))

# printing the output
# output A
count = 0
print("OUTPUT A")
for key, value in pairConfidenceValues.items():
    if count == 5:
        break
    print(key[0], key[1], value)
    count += 1
    
# output B
count = 0
print("OUTPUT B")
for key, value in tripleConfidenceValues.items():
    if count == 5:
        break
    print(key[0], key[1], key[2], value)
    count += 1