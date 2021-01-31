import parseInvesting

# Creating a class object
investing = parseInvesting.ParseInvesting()

# Get stock quotes in the MOEX index
result = investing.getQuotationsMOEX()
print(result)

# Get stock quotes in the S&P500 index
result = investing.getQuotationSP500()
print(result)

# Get stock quotes in the NASDAQ100 index
result = investing.getQuotationsNasdaq100()
print(result)

# Get stock quotes in the Dow Jones index
result = investing.getQuotationsDowJones()
print(result)

# Get stock quotes in the RTS index
result = investing.getQuotationsRTS()
print(result)

# Getting a gold futures quote
print(investing.getQuotationByName('Золото'))

# Getting a quote for the Sberbank stock
print(investing.getQuotationByName('Сбербанк'))
