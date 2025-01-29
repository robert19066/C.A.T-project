import os
import fnmatch
import string
import subprocess
import shlex


print("lib imported succesfully!")

debugMode = False

showSplashScreen = True


#Aliases:

change_directory_alias = 'goto' #done

list_directory_alias = 'lst' #done
list_directory_tree_alias_attrb = '-struct' #done

git_commit_alias = 'commit' #done

search_file_alias = 'search' #done
search_file_all_attirbute_alias = '-all' #done

run_command_alias = 'execute' #done
copy_file_alias = 'copy'#done
help_alias = 'help' #done
comand_insert_char = '>' #done
clear_alias = 'clear' #done

mkdir_alias = 'makeFol' #done
mkdir_alias2 = 'ml' #done

rmdir_force_alias_attrb = '-force' #done
rmdir_alias = 'removeFol' #done
rmdir_alias2 = 'rl' #done

mkfile_alias = 'makeFile' #done
mkfile_alias2 = 'mf' #done

openfile_alias = 'openFile' #done
openfile_alias2 = 'opn' #done

def printDebug(message):
    if debugMode:
        print(message)



printDebug("aliases imported succesfully!")


def parse_and_execute_command(command):
    parts = shlex.split(command)
    
    if not parts:
        printDebug("Null token inserted")
        return
    
    main_command = parts[0].lower()
    
    if main_command == copy_file_alias and len(parts) >= 3:
        filename = parts[1]
        destination_path = parts[2]
        copy(filename, destination_path)
    elif main_command == change_directory_alias and len(parts) >= 2:
        path = parts[1]
        changedir(path)
    elif main_command == list_directory_alias and len(parts) >= 2:
        if parts[1] == list_directory_tree_alias_attrb:
            tree()
        elif parts[1] == None:
            listdir()
    elif main_command == git_commit_alias and len(parts) >= 2:
        message = parts[1]
        commit(message)
    elif main_command == search_file_alias and len(parts) >= 2:
        if parts[1] == search_file_all_attirbute_alias:
            filename = parts[2]
            searchAll(filename)
        else:
            folder = parts[1]
            filename = parts[2]
            search(folder, filename)
    elif main_command == run_command_alias and len(parts) >= 2:
        command = parts[1]
        run(command)
    elif main_command == help_alias:
        help()
    elif main_command == clear_alias:
        clear()
    elif main_command == mkdir_alias or main_command == mkdir_alias2 and len(parts) >= 2:
        name = parts[1]
        mkdir(name)
    elif main_command == rmdir_alias or main_command == rmdir_alias2 and len(parts) >= 2:
        name = parts[1]
    elif main_command == rmdir_alias or main_command == rmdir_alias2 and len(parts) >= 2:
        if parts[1] == rmdir_force_alias_attrb:
            name = parts[2]
            rmdirForce(name)
        else:
            name = parts[1]
            rmdir(name)
    elif main_command == mkdir_alias or main_command == mkdir_alias2 and len(parts) >= 2:
        name = parts[1]
        mkdir(name)

    elif main_command == mkfile_alias or main_command == mkfile_alias2 and len(parts) >= 3:
        name = parts[1]
        type = parts[2]
        mkfile(name, type)
    elif main_command == openfile_alias or main_command == openfile_alias2 and len(parts) >= 2:
        name = parts[1]
        openfile(name)
    else:
        print(f"Unknown command: {main_command}")

printDebug("parsing setup function created succesfully!")

def detect_drives():
    drives = []
    for drive in string.ascii_uppercase:
        if os.path.exists(f'{drive}:\\'):
            drives.append(f'{drive}:\\')
    printDebug(f"Detected drives: {drives}")
    return drives


def commit(commit_message):
    try:
        # Stage all changes
        subprocess.check_call(['git', 'add', '.'])
        
        # Commit changes
        subprocess.check_call(['git', 'commit', '-m', commit_message])
        
        print("Changes committed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def searchAll(filename):
    printDebug(f"""
            Searching ALL dirs for file: {filename}
               """)
    drive_letters = detect_drives() # Add more if needed
    for drive in drive_letters:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if fnmatch.fnmatch(file, filename):
                    print(os.path.join(root, file))


def search(folder, filename):
    printDebug(f"""

            Searching in folder: {folder} for file: {filename}
""")
    for root, dirs, files in os.walk(folder):
        for file in files:
            if fnmatch.fnmatch(file, filename):
                print(os.path.join(root, file))


def changedir(path):
    try:
        # Check if path is ".." to go up one level
        if path == "..":
            # Go to the parent directory
            os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
            printDebug(f"Changed directory to:{os.getcwd()}")
        else:
            # Change directory to the provided path
            os.chdir(path)
            printDebug("Changed directory to:{os.getcwd()}")
    except Exception as e:
        print(f"Error: {e}")

def clear():
    os.system('cls')

def mkdir(name):
    run(f"mkdir {name}")

def rmdir(name):
    run(f"rmdir {name}")

def tree():
    run("tree /a")

def rmdirForce(name):
    run(f"rmdir /s /q {name}")

def mkfile(name, type):
    run(f"copy con {name}.{type}")

def openfile(name):
    run(f"notepad {name}")

def listdir():
    try:
        # List directory contents
        print("Directory contents:")
        print("=====================================")
        for file in os.listdir():
            print(file)
    except Exception as e:
        print(f"Error: {e}")

def run(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def copy(path, filepath):
    try:
        # Copy file to specified path
        run(f"xcopy {filepath} {path}")
        print("File copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def help():
    print(
        f"""
        btw if you change the commands's aliases you can see them with they're new aliases here
        Available commands:

        {change_directory_alias}(originaly goto) [path] - Change directory to the specified path.The .. works as well.
        {list_directory_alias}(originaly lst) - List directory contents.Works like the dir command in windows,or ls in unix-like systems.
        {git_commit_alias}(originaly commit) [message] - Commit changes to the git repository with the specified message.
        {search_file_alias}(originaly search) [folder] [filename]  - Search for a file with the specified name in the specified folder.Use it with the {search_file_all_attirbute_alias}(originaly -all) atrirbute to search in all drives.
        Note: If you see the {search_file_alias}(originaly search) with the {search_file_all_attirbute_alias}(originaly -all) attribute,failes,try to replace the function at line 80,to a list of your dirvers
        Ex: ['C:','D:','E:']

        {run_command_alias}(originaly execute) [command] - Run the specified command in the shell(windows).
        {copy_file_alias}(originaly copy) [path] [filepath] - Copy the file to the specified path.is xcopy from windows btw.

        yea that's it for now
"""
    )

print("functions created succesfully!")
print("prompt.py loaded succesfully!")
print("Booting C.A.T")
os.system('cls')

if showSplashScreen:print(r"""

    
          _____                    _____                _____          
         /\    \                  /\    \              /\    \           
        /::\    \                /::\    \            /::\    \        
       /::::\    \              /::::\    \           \:::\    \       
      /::::::\    \            /::::::\    \           \:::\    \      
     /:::/\:::\    \          /:::/\:::\    \           \:::\    \     
    /:::/  \:::\    \        /:::/__\:::\    \           \:::\    \    
   /:::/    \:::\    \      /::::\   \:::\    \          /::::\    \   
  /:::/    / \:::\    \    /::::::\   \:::\    \        /::::::\    \  
 /:::/    /   \:::\    \  /:::/\:::\   \:::\    \      /:::/\:::\    \ 
/:::/____/     \:::\____\/:::/  \:::\   \:::\____\    /:::/  \:::\____\
\:::\    \      \::/    /\::/    \:::\  /:::/    /   /:::/    \::/    /
 \:::\    \      \/____/  \/____/ \:::\/:::/    /   /:::/    / \/____/ 
  \:::\    \                       \::::::/    /   /:::/    /          
   \:::\    \                       \::::/    /   /:::/    /           
    \:::\    \                      /:::/    /    \::/    /            
     \:::\    \                    /:::/    /      \/____/             
      \:::\    \                  /:::/    /                           
       \:::\____\                /:::/    /                            
        \::/    /                \::/    /                             
         \/____/                  \/____/                              
                                                                       

      


                                                            /\_____/\
                                                           /  o   o  \
                                                          ( ==  ^  == )
                                                           )         (
                                                          (           )
                                                         ( (  )   (  ) )
                                                        (__(__)___(__)__)
   ___                                _     __                     _   _               _____ _     _             
  / __\___  _ __ ___   __ _ _ __   __| |   /__\_  _____  ___ _   _| |_(_) ___  _ __   /__   \ |__ (_)_ __   __ _ 
 / /  / _ \| '_ ` _ \ / _` | '_ \ / _` |  /_\ \ \/ / _ \/ __| | | | __| |/ _ \| '_ \    / /\/ '_ \| | '_ \ / _` |
/ /__| (_) | | | | | | (_| | | | | (_| | //__  >  <  __/ (__| |_| | |_| | (_) | | | |  / /  | | | | | | | | (_| |
\____/\___/|_| |_| |_|\__,_|_| |_|\__,_| \__/ /_/\_\___|\___|\__,_|\__|_|\___/|_| |_|  \/   |_| |_|_|_| |_|\__, |
                                                                                                           |___/ 

      
                                   Welcome to WinC.A.T (Windows Comand Execution Tool) V1.0
      
""")
else:
    print("                        Welcome to WinC.A.T (Comand Execution Tool) V1.0"        )

while True:
    cwd = os.getcwd()
    command = input(f"{cwd}{copy_file_alias}\n> ")
    parse_and_execute_command(command)