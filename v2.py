import os
import fnmatch
import string
import subprocess
import shlex
import getpass
import socket

def getInput():
    # Get the username
    username = getpass.getuser()

    # Get the hostname
    hostname = socket.gethostname()

    # Get the current working directory
    cwd = os.getcwd()

    # Replace the home directory path with '~'
    home_dir = os.path.expanduser("~")
    if cwd.startswith(home_dir):
        cwd = cwd.replace(home_dir, "~", 1)

    # Create the styled input prompt
    prompt = f"{username}@{hostname}: {cwd}$ "

    
    user_input = input(prompt)

    return user_input



print("lib imported succesfully!")

debugMode = False

showSplashScreen = True


#Aliases:


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
    
    if main_command == 'copyFile' or main_command == 'cf' and len(parts) >= 3:
        filename = parts[1]
        destination_path = parts[2]

        if filename == '?' or destination_path == '?':
            print("""
                    copyFile(or cf) [source_file] [destination_path] - Copy the file to the specified path.
                  """)
            return ""

        copy(filename, destination_path)
    elif main_command == 'goto' or main_command == 'gt' and len(parts) >= 2:
        path = parts[1]

        if path == '?':
            print("""
                    goto(or gt) [path] - Change the working directory to the specified path.
                  """)
            return os.getcwd()
        changedir(path)
    elif main_command == "list" or main_command == "lst":
        if len(parts) > 1 and parts[1] == "?":  # Check if there are enough parts and if the second part is '?'
            print("""
        lst - List directory contents.
        lst -struct - List directory contents in a tree structure.
            """)
        else:
            listdir()  # List directory contents normally if not '?'

    elif main_command == "struct":
        if len(parts) > 1 and parts[1] == "?":  # Check if there are enough parts and if the second part is '?'
            print("""
        struct = windows tree yes
            """)

        tree()
    elif main_command == "commit" and len(parts) >= 2:
        message = parts[1]
        if message == '?':
            print("""
                    commit [message] - Commit changes to the git repository with the specified message.
                  """)
        commit(message)
    elif main_command == "search" or main_command == "sc" and len(parts) >= 2:
        if parts[1] == "-all":
            filename = parts[2]
            searchAll(filename)
        else:
            folder = parts[1]
            filename = parts[2]

            if folder == '?' or filename == '?':
                print("""
                        search(or sc) [folder] [filename] - Search for a file with the specified name in the specified folder.
                        Use it with the -all atrirbute to search in all drives.
                      """)
                return ""

            search(folder, filename)
    elif main_command == "exec" and len(parts) >= 2:
        command = parts[1]
        if command == '?':
            print("""
                    exec [command] - Run the specified command in the shell(windows).
                  """)
        run(command)
    elif main_command == "help" or main_command == "?":
        help()
    elif main_command == "clear" or main_command == "cls" or main_command == "c" and len(parts) >= 3:
        if parts[1] == "?":
            print("""
                    clear - Clear the screen.
                  """)
        else:
            clear()
    elif main_command == "mkFol" or main_command == "mf" and len(parts) >= 2:
        name = parts[1]
        if name == '?':
            print("""
                    mkFol(or mf) [name] - Create a new directory(or folder is the) with the specified name.
                  """)
            return ""
        mkdir(name)
    elif main_command == "rmFol" or main_command == "rf" and len(parts) >= 2:
        if parts[1] == "-force":
            name = parts[2]
            rmdirForce(name)
        elif parts[1] == "?":
            print("""
                    rmFol(or rf) [name] - Remove the directory with the specified name.
                    rmFol(or rf) -force [name] - Remove the directory with the specified name and all its contents.
                  """)
            return ""
        else:
            name = parts[1]
            rmdir(name)
    elif main_command == "mkFile" or main_command == "mkf" and len(parts) >= 3:
        name = parts[1]
        type = parts[2]

        if name == '?' or type == '?':
            print("""
                    mkFile(or mkf) [name] [type] - Create a new file with the specified name and type.
                    Example: mkFile test txt
                  """)
            return ""
        mkfile(name, type)
    elif main_command == "opnFile" or main_command == "opf" and len(parts) >= 2:
        name = parts[1]
        if name == '?':
            print("""
                    opnFile(or opf) [name] - Open the file with the specified name in the default text editor.
                  """)
            return ""
        openfile(name)

    elif main_command == "changelog" or main_command == "chlog":
        print("""
            Changelog:

            Removed aliases
            Inproved the code
            Bug fixes
            New input prompt(looks better)
            Version selection menu
            Educative edition(more detail,easier commands)
            New command: struct(lst -struct was broken so i made a new command)
            PS: Edcuative edition is still in development
            PS2: educative edition is just v2 but more detailed.
        """)
    elif main_command == "readexec" and len(parts) >= 2:
        file_path = parts[1]
        if file_path == '?':
            print("""
                    readexec [file_path] - Read and execute commands from the specified file.
                    IT MUST BE A .CAT FILE
                  """)
            return ""
        execute_commands_from_file(file_path)
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


def execute_commands_from_file(file_path):
    # Check if the file has the correct extension (.cmdlist)
    if not file_path.endswith('.cat'):
        print(f"Error: File must be a '.cat' file. You provided: {file_path}")
        return
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace or newline
        if line:  # Skip empty lines
            print(f"Executing command: {line}")
            parse_and_execute_command(line)

# Example of calling the function
execute_commands_from_file('commands.cmdlist')


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

        goto [path] - Change directory to the specified path.The .. works as well.

        =============================================================================================================================

        lst - List directory contents.Works like the dir command in windows,or ls in unix-like systems.

        =============================================================================================================================

        commit [message] - Commit changes to the git repository with the specified message.

        =============================================================================================================================

        search [folder] [filename]  - Search for a file with the specified name in the specified folder.Use it with the -all atrirbute to search in all drives.

        =============================================================================================================================

        Note:
            if you run search with the all attribute,failes,try to replace the function at line 80,to a list of your dirvers
            Ex: ['C:','D:','E:']
        =============================================================================================================================

        execute [command] - Run the specified command in the shell(windows).

        =============================================================================================================================

        copy [path] [filepath] - Copy the file to the specified path.is xcopy from windows btw.

        =============================================================================================================================

        changelog - Show the changelog of the current version.
        or chlog

        =============================================================================================================================

        clear - Clear the screen.

        ============================================================================================================================

        readexec [file_path] - Read and execute commands from the specified file.
        IT MUST BE A .CAT FILE

        ============================================================================================================================

        struct - List directory contents in a tree structure.

        ============================================================================================================================
        yea that's it for now
"""
    )

print("functions created succesfully!")
print("prompt.py loaded succesfully!")
print("Booting C.A.T")


os.system('cls')

if showSplashScreen:print(r"""

 
                                      ,----,                                   
                                    ,/   .`|                                   
  ,----..          ,---,          ,`   .'  :                          ,----,   
 /   /   \        '  .' \       ;    ;     /               ,---.    .'   .' \  
|   :     :      /  ;    '.   .'___,/    ,'               /__./|  ,----,'    | 
.   |  ;. /     :  :       \  |    :     |           ,---.;  ; |  |    :  .  ; 
.   ; /--`      :  |   /\   \ ;    |.';  ;          /___/ \  | |  ;    |.'  /  
;   | ;         |  :  ' ;.   :`----'  |  |          \   ;  \ ' |  `----'/  ;   
|   : |         |  |  ;/  \   \   '   :  ;           \   \  \: |    /  ;  /    
.   | '___      '  :  | \  \ ,'   |   |  '            ;   \  ' .   ;  /  /-,   
'   ; : .'|     |  |  '  '--'     '   :  |             \   \   '  /  /  /.`|   
'   | '/  :___  |  :  : ___       ;   |.'               \   `  ;./__;      :   
|   :    //  .\ |  | ,'/  .\      '---'                  :   \ ||   :    .'    
 \   \ .' \  ; |`--''  \  ; |                             '---" ;   | .'       
  `---`    `--"         `--"                                    `---'          
                                                                               

      
                                   Welcome to WinC.A.T (Windows Comand Execution Tool) V2.0
      
""")
else:
    print("                        Welcome to WinC.A.T (Windows Comand Execution Tool) V2.0"        )

while True:
    parse_and_execute_command(getInput())