from grammarHash import grammarHash

NTs= list(grammarHash.keys())

prods= [i.split("|") for i in grammarHash.values()]

#print(NTs)

#print(prods)
result = {}
for nonT in NTs:
    result[nonT]= {}
    prods= grammarHash[nonT]
    prod_strings= prods.split("|")
    for i in prod_strings:
        prod_first_element= i.split(" ")[0]
        result[nonT][prod_first_element]= "$$$$"

print(result)