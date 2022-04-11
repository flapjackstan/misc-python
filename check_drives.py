import os


def get_open_drive():
    for i in range(ord('A'), ord('Z') + 1):

        drive = chr(i) + ':'
        print('Trying drive: ' + drive)

        try:
            os.scandir(drive)
        except FileNotFoundError:
            print("Drive is Empty")
            return drive


def main():
    drive = get_open_drive()
    print(drive)


if __name__ == '__main__':
    main()
