from parseInvesting import ParseQuotation

# Get stock quotes in the MOEX index
result = ParseQuotation.getQuotationsMOEX()
print(result)

# Get stock quotes in the S&P500 index
result = ParseQuotation.getQuotationSP500()
print(result)

# Get stock quotes in the NASDAQ100 index
result = ParseQuotation.getQuotationsNasdaq100()
print(result)

# Get stock quotes in the Dow Jones index
result = ParseQuotation.getQuotationsDowJones()
print(result)

# Get stock quotes in the RTS index
result = ParseQuotation.getQuotationsRTS()
print(result)

# Getting a gold futures quote
print(ParseQuotation.getQuotationByName('Золото'))

# Getting a quote for the Sberbank stock
print(ParseQuotation.getQuotationByName('Сбербанк'))
