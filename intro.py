import inquirer # type: ignore
import subprocess
import os

os.system('cls' if os.name == 'nt' else 'clear')
questions = [
    inquirer.List('choice',
                    message="Please select your desired C.A.T version",
                    choices=['C.A.T normal(v1)', 'C.A.T + (v2)', 'C.A.T EDU(v1.5)'],
                    carousel=True
                ),
]
print("C.A.T VERSION SELECTOR - robert19066 all rights reserved")
answer = inquirer.prompt(questions)
if answer['choice'] == 'C.A.T normal(v1)':
    subprocess.run(['python', 'v1.py'], capture_output=True, text=True)
elif answer['choice'] == 'C.A.T + (v2)':
    subprocess.run(['python', 'v2.py'], capture_output=True, text=True)
else:
    subprocess.run(['python', 'edu.py'], capture_output=True, text=True)
