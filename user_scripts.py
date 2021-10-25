import os
import sys

def check_user():
    user = os.environ.get('USERNAME')
    return user
    
def is_server():
    username = check_user()

    if username == 'Server':
        return True
    else:
        return False

def main():
    try:
        server_flag = is_server()        
        print(server_flag)
                
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