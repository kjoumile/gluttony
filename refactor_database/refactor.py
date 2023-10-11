file_black = open('E:/program/py/twitter_bot/refactor_database/black_acc.txt', 'r')
file_grey = open('E:/program/py/twitter_bot/refactor_database/grey_acc.txt', 'r')
file_proxy = open('E:/program/py/twitter_bot/refactor_database/proxy.txt', 'r')
black_account_data = open('E:/program/py/twitter_bot/database/black_account_data.txt', 'w')
grey_account_data = open('E:/program/py/twitter_bot/database/grey_account_data.txt', 'w')

black_lines = file_black.readlines()
grey_lines = file_grey.readlines()
proxy_lines = file_proxy.readlines()

for i in range(len(black_lines)):
    black_account_data.write(
        black_lines[i].split(':')[0]+
        ','+black_lines[i].split(':')[1]+
        ','+black_lines[i].split(':')[4]+
        ','+proxy_lines[i]
    )
for i in range(len(grey_lines)-1):
    grey_account_data.write(grey_lines[i].split(':')[0])
    grey_account_data.write(',')
    grey_account_data.write(grey_lines[i].split(':')[1])
    grey_account_data.write(',')
    grey_account_data.write(proxy_lines[len(black_lines)+i])

file_black.close()
file_grey.close()
file_proxy.close()
black_account_data.close()
grey_account_data.close()