import os


def get_open_drive():
    '''Iterates from A-Z checking if an established drive is mapped to coresponding letter

    Parameters
    ----------
    None

    Returns
    ----------
    drive : str
        First unmapped drive letter
    '''
    for i in range(ord('A'), ord('Z') + 1):
        drive = chr(i) + ':'

        try:
            os.scandir(drive)
        except FileNotFoundError:
            return drive

def main():
    drive = get_open_drive()
    print(drive)


if __name__ == '__main__':
    main()
