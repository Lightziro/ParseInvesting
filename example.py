from parseInvesting import ParseQuotation
import mysql.connector

mydb = mysql.connector.connect(
  host="141.8.192.93",
  user="a0507369_shop",
  password="Logan02022002",
  database="a0507369_shop"
)

cursor = mydb.cursor()
cursor.execute('SELECT * FROM User')
result = cursor.fetchall()

print(result)


# # Get stock quotes in the MOEX index
# result = ParseQuotation.getQuotationsMOEX()
# print(result)
#
# # Get stock quotes in the S&P500 index
# result = ParseQuotation.getQuotationSP500()
# print(result)
#
# # Get stock quotes in the NASDAQ100 index
# result = ParseQuotation.getQuotationsNasdaq100()
# print(result)
#
# # Get stock quotes in the Dow Jones index
# result = ParseQuotation.getQuotationsDowJones()
# print(result)
#
# # Get stock quotes in the RTS index
# result = ParseQuotation.getQuotationsRTS()
# print(result)
#
# # Getting a gold futures quote
# print(ParseQuotation.getQuotationByName('Золото'))
#
# # Getting a quote for the Sberbank stock
# print(ParseQuotation.getQuotationByName('Сбербанк'))
