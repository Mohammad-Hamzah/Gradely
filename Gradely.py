import mysql.connector
from rich.traceback import install #this will show errors beautifully
from rich import print as rprint
from rich.table import Table #this will display tables beautifully
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn #helps to create progress bars and spinners
import time #this module is for time related things
from pwinput import pwinput #this module will mask the password being entered as asterisk(*) on the screen
import mysql.connector

install() #calling the install function will overwrite the current error statement procedure and will show errors beautifully
console=Console()

#colored typewriter function
def typewrite(string,sec=0.01,color='bold cyan',end='\n'):
    for i in string:
        rprint(f"[{color}]{i}[/{color}]", end='',flush=True)
        '''If flush is set to false
        and if you print multiple lines quickly, 
        they may all be sent to the terminal 
        in a single operation rather than one at a time.
        so setting flush to false, prints it immediately,
        also here console.print() was giving unexpected results (colored slashes and numbers differently) so using rprint'''
        
        time.sleep(sec)
    print(end=end)

#textbox function
def textbox(text,border='cyan',style=box.SQUARE):
    box = Panel(f"{text}", border_style=border, box=style,expand=False)
    console.print(box)

#progress bar function
def progress_bar(start='Loading...',end='Loading...',sec=2,startcolor='bold yellow',endcolor='bold green'):
    sleep=sec/100
    with Progress(
    TextColumn("{task.description}"),  # Task description in bold blue
    BarColumn(complete_style=startcolor, finished_style=endcolor),  # Default bar style
    ) as progress:
        task = progress.add_task(f"[{startcolor}]{start}", total=100)

        while not progress.finished:
            time.sleep(sleep)
            progress.update(task, advance=1)
        

        progress.update(task, description=f"[{endcolor}]{end}")
            
        time.sleep(0.5)

#spinner function
def spinner(list=['','',''],start='Loading...',end=None,startcolor='bold yellow',endcolor='bold green',type='dots',spincolor='bold yellow'):
    tasks = list 
    # Start the status spinner with a message
    with console.status(f"[{startcolor}]{start}",spinner=type,spinner_style=spincolor) as status:
        while tasks:
            # Get the first task from the list and remove it
            task = tasks.pop(0)

            # Simulate doing some work with sleep
            time.sleep(1)
            if task!='':
                # Print the completion of the task
                console.print(f"[{endcolor}]{task}[/]")
    if end:
        console.print(f"[{endcolor}]{end}")
    time.sleep(0.5)

def valid_input(list,warning='Please choose from the given options only!'):
    
    while True:
        var=input()
        if var in list:
            return var
        else:
            typewrite(f"{warning}:\n> ",color='bold yellow',end='')
            
#INTRO

#asking for sql password and username
while True:
    typewrite("Please enter your SQL username (default=root): ",end='')
    sqlu=input()
    typewrite("Please enter your SQL password: ",end='')
    sqlpw=pwinput(prompt='')

    #simulating loading the app
    spinner(list=['','',''],start='Establishing secure connection...',spincolor='yellow',startcolor='bold yellow')

    try:
        # Try to connect to the database
        db = mysql.connector.connect(
            host='localhost',
            user=sqlu,
            passwd=sqlpw
        )

        if db.is_connected():
            typewrite("Connected!",color='bold green')
            break

    except mysql.connector.Error as e:
        if e.errno==1045:
            typewrite("Incorrect username or password... Please try again!",color='bold red')
        else:
            typewrite(f"Encountered {e}... Please try again!",color='bold red')


        
progress_bar()

#printing the logo
with open (r'assets\ascii_image_new.txt') as file:
    for line in file.readlines():
        console.print(line,end='',style='cyan')
        time.sleep(0.01)
    print()
    print()

typewrite("Welcome to TrackEd!\nPlease choose how you would like to login:\n1. Admin\n2. Teacher\n3. Student\n> ",color='bold cyan',end='')

usertype=valid_input(["1","2","3"],warning="Please choose from the given options only! (1,2,3)")

typewrite("Please enter your username: ",end='') #CANT BE EMPTY
un=input()
typewrite("Please enter your password: ",end='')
pw=pwinput(prompt='')

#simulating checking password
spinner(list=['','',''],start='Verifying credentials...',spincolor='yellow',startcolor='bold yellow')
