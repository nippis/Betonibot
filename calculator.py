import re

def calculator(calcInput):
    factors = re.findall('[0-9]+', calcInput)
    if re.search('=\s*[0-9]+\s*\+\s*[0-9]+', calcInput):
        return int(factors[0])+int(factors[1])
    elif re.search('=\s*[0-9]+\s*-\s*[0-9]+', calcInput):
        return int(factors[0])-int(factors[1])
    elif re.search('=\s*[0-9]+\s*\*\s*[0-9]+', calcInput):
        return int(factors[0])*int(factors[1])
    elif re.search('=\s*[0-9]+\s*/\s*[0-9]+', calcInput):
        return int(factors[0])/int(factors[1])