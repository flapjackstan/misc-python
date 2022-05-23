import sys

def check_dev(dictionary):
    if '--test' in dictionary:
        return True
    else:
        return False

def append_table_designator(table,dictionary):
    dev_flag = check_dev(dictionary)
    
    if dev_flag:
        return 'dev_' + table
    else:
        return table

def main():
    try:
        docopt = {'--test':'True'}
        
        table = "lhj_all"
        
        table = append_table_designator(table,docopt)
        
        print(table)
                
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
          
        error_type = str(exc_type)
        line = exc_tb.tb_lineno
        word =  error_type + ' at Line '
        error = word+str(line)

        message = (error + ': ' + str(e))
        
        print(message)

if __name__ == '__main__':
    main()