import rich #this module makes python execution more attractive
from rich import print as rprint
import time #this module is for time related things

#typewriter function
def tw(string,sec=0.01,end='\n'):
    for i in string:
        print(i, end='',flush=True)
        '''If flush is set to false
        and if you print multiple lines quickly, 
        they may all be sent to the terminal 
        in a single operation rather than one at a time.
        so setting flush to false, prints it immediately'''
        time.sleep(sec)
        #time.sleep(time in seconds)>> this forces the system to pause execution for given seconds
    print(end=end)

#colored typewriter function
def tw_color(string,sec=0.01,color='bold cyan',end=' '):
    for i in string:
        rprint(f"[{color}]{i}[/{color}]", end='',flush=True)
        time.sleep(sec)
    print(end=end)


#INTRO

#printing the logo
with open (r'assets\ascii_image_new.txt') as file:
    for line in file.readlines():
        rprint(f"[cyan]{line}[/cyan]",end='')
        time.sleep(0.01)
    print()
    print()

tw_color("Welcome to Tracktive!\nPlease choose how you would like to login:\n1. Admin\n2. Teacher\n>",color='bold cyan',end='')

while True:
    usertype=input()
    if usertype!='1' and usertype!='2':
        tw_color("Please choose from the above options only! (1/2):\n>",end='')
    else:
        break

tw_color("Please enter your username: ")
un=input()
tw_color("Please enter your password: ")
pw=input()
    
