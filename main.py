from binascii import hexlify
import sys, os

# Save the parsing data to a file.
def parsing(filename,f,endian):
    try:
        stdout = sys.stdout # Saves the output value in cmd
        print (os.path.splitext(filename)[-2] + '.txt')
        sys.stdout = open(os.path.splitext(filename)[-2] + '.txt', 'w')
        print (endian)
        ffd8 = hexlify(f.read(2)).upper().decode()
        
        print ('[+] marker : 0x%s'%ffd8) # parsered 0xFFD8
        print ('[+] M_ID marker : 0x%s'%(hexlify(f.read(2)).upper()).decode())
        length = int((hexlify(f.read(2)).upper()).decode(),16)
        print ('  - Length : %s' %length)
        print ()

        length += 4
        f.seek(length) # Moved by the size of the length
        print ('[+] marker : 0x%s'%(hexlify(f.read(2)).upper()).decode())
        print ('  - Offset : %s' %(hex(length))) # offset calculation
        length2 = int((hexlify(f.read(2)).upper()).decode(),16)
        print ('  - Length : %s' %length2)
        print ()

        total_len = 0
        length3 = 0
        flag = False
        # parsing through loop
        while True:
            length3 +=2
            total_len += length3
            f.seek(length+length2+total_len)
            marker = f.read(2)
            print ('[+] marker : 0x%s'%(hexlify(marker).upper()).decode())
            print ('  - Offset : %s' %(hex(length+length2+total_len)))
            if marker == b'\xff\xda': # if 0xFFDA, Run next loop
                print ('  - Length : %s' %int((hexlify(f.read(2)).upper()).decode(),16))
                while True:
                    marker2 = f.read(1) 
                    if marker2 == b'\xff': # Find 0xFFD9 by byte
                        marker3 = f.read(1)
                        if marker3 == b'\xd9':
                            fin_offset = (f.tell())
                            fin_offset2 = fin_offset-2
                            f.seek(fin_offset2)
                            marker4 = f.read(2)
                            print ()
                            print ('[+] marker : 0x%s'%(hexlify(marker4).upper()).decode())
                            print ('  - Offset : %s' %(hex(fin_offset2)))
                            print ('  - End Signature')
                            print ()
                            flag = True # Flag Set
                            break
            if flag == True: # Flag check
                break
            length3 = int((hexlify(f.read(2)).upper()).decode(),16)
            print ('  - Length : %s' %length3)
            print ()

        sys.stdout.close()
        sys.stdout = stdout
            
    except Exception as e:
        print ('Error!! %s' %e)

# Function for output
# Same function as 'parsing' function
def print_out(f,endian):
        print (endian)
        ffd8 = hexlify(f.read(2)).upper().decode()
        
        print ('[+] marker : 0x%s'%ffd8)
        print ('[+] M_ID marker : 0x%s'%(hexlify(f.read(2)).upper()).decode())
        length = int((hexlify(f.read(2)).upper()).decode(),16)
        print ('  - Length : %s' %length)
        print ()

        length += 4
        f.seek(length)
        print ('[+] marker : 0x%s'%(hexlify(f.read(2)).upper()).decode())
        print ('  - Offset : %s' %(hex(length)))
        length2 = int((hexlify(f.read(2)).upper()).decode(),16)
        print ('  - Length : %s' %length2)
        print ()

        total_len = 0
        length3 = 0
        flag = False
        while True:
            length3 +=2
            total_len += length3
            f.seek(length+length2+total_len)
            marker = f.read(2)
            print ('[+] marker : 0x%s'%(hexlify(marker).upper()).decode())
            print ('  - Offset : %s' %(hex(length+length2+total_len)))
            if marker == b'\xff\xda':
                print ('  - Length : %s' %int((hexlify(f.read(2)).upper()).decode(),16))
                while True:
                    marker2 = f.read(1)
                    if marker2 == b'\xff':
                        marker3 = f.read(1)
                        if marker3 == b'\xd9':
                            fin_offset = (f.tell())
                            fin_offset2 = fin_offset-2
                            f.seek(fin_offset2)
                            marker4 = f.read(2)
                            print ()
                            print ('[+] marker : 0x%s'%(hexlify(marker4).upper()).decode())
                            print ('  - Offset : %s' %(hex(fin_offset2)))
                            print ('  - End Signature')
                            print ('----------------------------------------------')
                            print ()
                            flag = True
                            break
            if flag == True:
                break
            length3 = int((hexlify(f.read(2)).upper()).decode(),16)
            print ('  - Length : %s' %length3)
            print ()

# Check Endian
def align(f):
    i = 0
    while i<51:
        tmp = f.read(2)
        if tmp == b'\x49\x49':
            return 0
        if tmp == b'\x4D\x4D':
            return 1
        if i == 50:
            return 2
        i+=2

if __name__ == "__main__":
    print ('Hello, world!')
    try:
        var1 = sys.argv[1] # receive argument
        jpegs = []
        if os.path.isdir(var1):
            for path, dir, files in os.walk(var1): # Navigating inside a folder 
                for jpeg in files:
                    jpegs.append(os.path.join(path, jpeg))
        else:
            jpegs.append(var1)
        for full_path in jpegs:
            filename = os.path.basename(full_path)
            ext = os.path.splitext(filename)[-1]
            if ext == '.jpg' or ext == '.jpeg': # Extension check
                print ('[+] File Name : %s' %filename,end='')

                try:
                    with open(full_path,'rb') as f:
                        if f.read(2) == b'\xff\xd8':
                            f.seek(0)
                            align2 = align(f) # Check Endian
                            if align2 == 0:
                                endian =  ('[+] byte align : little endian')
                                print ()
                                f.seek(0)
                                parsing(filename,f,endian)
                                f.seek(0)
                                print_out(f,endian)
                            if align2 == 1:
                                endian =  ('[+] byte align : Big endian')
                                print ()
                                f.seek(0)
                                parsing(filename,f,endian)
                                f.seek(0)
                                print_out(f,endian)
                            if align2 == 2:
                                endian = ('[+] byte align : Unknown')
                                print ()
                                f.seek(0)
                                parsing(filename,f,endian)
                                f.seek(0)
                                print_out(f,endian)
                        else :
                            print ('It\'s not jpeg file')

                            print ()
                            sys.exit(1)
                except Exception as e:
                    print (e)
            else:
                print ()
                print (path)
                print ('There is no \'.jpg\' or \'.jpeg\' in the Directory.')
                print ()
    except Exception:
        print ()
        print ('      -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
        print ('[*] Please input argument. ex) $jpeg_parsing.exe sample.jpeg')
        print ('      -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
