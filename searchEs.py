#coding=utf-8
#from ESDK import ES
#S = ES()
import sys,re,time
if sys.platform == 'win32':
    import msvcrt
    getch = msvcrt.getch
else:
    from getch import getch

#these code from 10 line fuzzy 
collection = ['django_migrations.py',
                'django_admin_log.py',
                'main_generator.py',
                'migrations.py',
                'api_user.doc',
                'user_group.doc',
                'accounts.txt',]

def fuzzy(user_input,collection):
    suggestions = []
    pattern = '.*?'.join(user_input)    # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)      # Compiles a regex.
    for item in collection:
        match = regex.search(item)   # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]
#print fuzzy("user",collection)

def read():
    def readline():
        if sys.platform == 'win32':
            backspace = 8 
        else:
            backspace = 127
        tabkey = 9
        sys.stdout.flush()
        tmp = ''
        char = '_'
        changed = False
        result = [ ]
        sys.stdout.write ('\r>> ')
        sys.stdout.flush()
        while ord(char) != 13 :
            char = getch() #print ord(char)
            if changed :
                try:
                    result = fuzzy(tmp,collection)
                except:
                    pass
            #    #result = S.search (tmp) # if back search then need search temp 
            #    #if len(result) > 6:
            #    #    result = result[0:6]
            #    #result = '\n'.join(result)
            #    #result = "\n" + result
            #if ord(char) == 224:
            #    temp = ord(getch())
            #    if temp in [72,75,77,80]:
            #        sys.stdout.flush()
            if ord(char) == tabkey:
                #result = S.search (tmp) # if back search then need search temp 
                #if len(result) > 6:
                #    result = result[0:6]
                if result:
                    show = ' , '.join(result)
                    sys.stdout.write("\r" + "=> " + show + "\n")
                else:
                    sys.stdout.write("\r" + "=> " + "No found result." + "\n")
            if char.isalnum() or char in """ <>,.*/:;'\"[]()|\\~-_+`=!@#$%^&?{}""":
                #ord(char) != 8 and ord(char) != 9 :
                tmp += char
                changed = True#True
            if ord(char) == backspace:
                sys.stdout.write("\b ")
                sys.stdout.flush()
                tmp= tmp[0:-1]
                changed = False
            sys.stdout.write("\r>> " + tmp ) #  return put enter key
            sys.stdout.flush()
        return tmp
    result = readline()
    sys.stdout.write('\r\b' + ' ' *  ( len(result) + len('\r>> ') ) + '\n')
    sys.stdout.flush()
    return result

def repl() :
    import os
    #context = read()
    while 1:
        #sys.stdout.write('\r\b' + ' ' *  len(context))
        #sys.stdout.flush()
        context = read()
        print "$",context
        if context == ':q':
            break
        elif context :
            sys.stdout.write("\n")
            os.system(context)
if __name__ == '__main__':        
    repl()
    #context = read()
    #print list(context)
