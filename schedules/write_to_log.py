from datetime import datetime

curr_date = datetime.now()


with open('log.txt', 'a') as f:
    f.write(f'{curr_date}\n')
