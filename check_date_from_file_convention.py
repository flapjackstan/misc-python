'''
Usage:
    check_date_from_file_convention.py (-i <path>)

Options:
    -i path         Input file path.

cair_pm_hosp_geocoded_040722.csv



'''

import docopt
import shutil

from docopt import docopt
from datetime import datetime


def main(opts):
    file = opts['-i']
    split_file = file.split('_')
    date_str = split_file[4][:-4]

    date = datetime.strptime(date_str, "%m%d%y")

    day_of_week = date.strftime('%A')
    
    print(day_of_week)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.4.0')
    main(arguments)