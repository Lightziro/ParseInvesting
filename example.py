import parseInvesting

# Creating a class object
investing = parseInvesting.ParseInvesting()

# Get index quotes for link = https://ru.investing.com/indices/major-indices
result = investing.getQuotation({'type': 'major-indices', 'typeStats': 'indices'})
print(result)

# Get quotes of Russian stocks for link = https://ru.investing.com/equities/russia
result = investing.getQuotation({'type': 'russia', 'typeStats': 'equities'})
print(result)

# Get quotes of USA stocks for link = https://ru.investing.com/equities/americas
result = investing.getQuotation({'type': 'americas', 'typeStats': 'equities'})
print(result)
