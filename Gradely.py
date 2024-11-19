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
import mysql.connector as sql
import bcrypt #for passwords

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
            
def dbconnect(cursor,database):
    cursor.execute('SHOW DATABASES')
    dbs=cursor.fetchall()
    for db in dbs:
        if 'gradely' in db:
            database.database='gradely'
        else:
            #I will add the required code later
            pass

def home():
    typewrite("Welcome to Gradely!\nPlease choose how you would like to login ('0' to exit):\n1. Admin\n2. Teacher\n> ",color='bold cyan',end='')

    usertype=valid_input(["0","1","2"],warning="Please choose from the given options only! (1/2)")

    while True:

        if usertype=='0':
            typewrite("Thanks for using our program!",color='bold green',end='')
            exit()

        if usertype=='1':

            typewrite("Please enter your username: ",end='') #CANT BE EMPTY
            inputun=input()
            typewrite("Please enter your password: ",end='')
            inputpw=pwinput(prompt='')

            #simulating checking password
            spinner(list=['','',''],start='Verifying credentials...',spincolor='yellow',startcolor='bold yellow')

            cur.execute("SELECT * FROM ADM")
            creds=cur.fetchall()
            for cred in creds:
                if cred[0]==inputun:
                    storedpw=cred[1]
                    if bcrypt.checkpw(inputpw.encode(), storedpw):
                        typewrite("Credentials verified.",color='bold green')
                        progress_bar(start='Logging in...',startcolor='bold green')
                        admin()
                        break
                    else:
                        typewrite("Incorrect username or password! Please try again!",color='bold red')

        else:

            typewrite("Please enter your ID: ",end='') #CANT BE EMPTY
            inputid=input()
            typewrite("Please enter your password: ",end='')
            inputpw=pwinput(prompt='')

            #simulating checking password
            spinner(list=['','',''],start='Verifying credentials...',spincolor='yellow',startcolor='bold yellow')

            cur.execute("SELECT * FROM CTS")
            creds=cur.fetchall()
            for cred in creds:
                if cred[0]==int(inputid):
                    storedpw=cred[2]
                    if bcrypt.checkpw(inputpw.encode(), storedpw):
                        typewrite("Credentials verified.",color='bold green')
                        progress_bar(start='Logging in...',startcolor='bold green')
                        cur.execute("SELECT DISTINCT CLASS FROM CTS,CLASS WHERE CLASS.CTID=%s",(cred[0],))
                        cls=cur.fetchone()[0]
                        ct(cred[1],cls)
                        break
                    else:
                        typewrite("Incorrect ID or password! Please try again!",color='bold red')


def admin():
    def report_card():
        pass
    def stream_toplist():
        pass
    def subject_toplist():
        pass
    def overall_toplist():
        pass
    def teacher_report():
        pass

def ct(tname,cls):
    while True:
        typewrite(f"Welcome back, {tname}!\nPlease choose from the given options:\n1. Update Marks\n2. Logout\n3. Exit\n> ",color='bold cyan',end='')
        mainchoice=valid_input(['1','2','3'])
        if mainchoice=='1':
            typewrite("Please choose how you would like to update marks (enter '0' for home):\n1. Single Student\n2. Bulk Update\n> ",color='bold cyan',end='')
            choice=valid_input(['0','1','2'])
            if choice=='1':
                while True:
                    typewrite("Please enter the student's Grno. (enter '0' for home):\n> ",color='bold cyan',end='')
                    grno=int(input())
                    if grno==0:
                        break
                    else:
                        cur.execute("SELECT * FROM STUDENTS WHERE GRNO=%s AND CLASS=%s",(grno,cls))
                        stddata=cur.fetchone()
                        if stddata==None:
                            typewrite("Data not found! Please try again!:\n> ",color='bold red',end='')
                        else:
                            cur.execute("SELECT SUBJECTS.SUBNAME FROM STUDENTSUBJECTS,SUBJECTS WHERE GRNO=%s AND STUDENTSUBJECTS.SUBID=SUBJECTS.SUBID;",(grno,))
                            subjects=cur.fetchall()
                            cur.execute("SELECT DISTINCT EXAM FROM EXAMS ORDER BY EXAM")
                            exams=cur.fetchall()
                            s1,s2,s3,s4,s5=subjects[0][0],subjects[1][0],subjects[2][0],subjects[3][0],subjects[4][0]
                            ae,hy,ut1,ut2=exams[0][0],exams[1][0],exams[2][0],exams[3][0]
                            name=stddata[1]
                            father=stddata[2]
                            mother=stddata[3]
                            dob=stddata[4]
                            cl=stddata[5]
                            roll=stddata[6]
                            typewrite(f"Student found...\nGR no.: {grno}\nName: {name}\nRoll no.: {roll}\n",color='bold green',end='')
                            typewrite(f"Please choose the exam (enter '0' for home):\n1. {ut1}\n2. {hy}\n3. {ut2}\n4. {ae}\n> ",color='bold cyan',end='')
                            
                            chosenexam=valid_input(['0','1','2','3','4'])
                            if chosenexam=='0':
                                break
                            else:
                                if chosenexam=='1':
                                    chosenexam=ut1
                                if chosenexam=='2':
                                    chosenexam=hy
                                if chosenexam=='3':
                                    chosenexam=ut2
                                if chosenexam=='4':
                                    chosenexam=ae
                            typewrite(f"Please choose the subject (enter '0' for home):\n1. {s1}\n2. {s2}\n3. {s3}\n4. {s4}\n5. {s5}\n> ",color='bold cyan',end='')
                            chosensub=valid_input(['0','1','2','3','4','5'])
                            if chosensub=='0':
                                break
                            else:
                                if chosensub=='1':
                                    chosensub=s1
                                if chosensub=='2':
                                    chosensub=s2
                                if chosensub=='3':
                                    chosensub=s3
                                if chosensub=='4':
                                    chosensub=s4
                                if chosensub=='5':
                                    chosensub=s5
                                
                            typewrite("Please enter new marks (enter '0' for home):\n> ",color='bold cyan',end='')
                            newmarks=int(input())
                            if newmarks==0:
                                break
                            else:
                                cur.execute("UPDATE MARKS SET MARKS = %s WHERE GRNO = %s AND SUBID = (SELECT SUBID FROM SUBJECTS WHERE SUBNAME = %s) AND EXAM = %s",(newmarks,grno,chosensub,chosenexam))
                                db.commit()
                                typewrite("Marks updated successfully... Returning to home...\n> ",color='bold green',end='')
                                break

            if choice=='2':
                while True:
                    cur.execute("SELECT DISTINCT EXAM FROM EXAMS ORDER BY EXAM")
                    exams=cur.fetchall()
                    ae,hy,ut1,ut2=exams[0][0],exams[1][0],exams[2][0],exams[3][0]

                    cur.execute("SELECT DISTINCT SUBNAME FROM STUDENTSUBJECTS,STUDENTS,SUBJECTS WHERE CLASS=%s AND STUDENTS.GRNO=STUDENTSUBJECTS.GRNO AND SUBJECTS.SUBID=STUDENTSUBJECTS.SUBID",(cls,))
                    subjects=cur.fetchall()
                    s1,s2,s3,s4,s5=subjects[0][0],subjects[1][0],subjects[2][0],subjects[3][0],subjects[4][0]


                    typewrite(f"Please choose the exam for bulk entry (enter '0' for home):\n1. {ut1}\n2. {hy}\n3. {ut2}\n4. {ae}\n> ",color='bold cyan',end='')
             
                    chosenexam=valid_input(['0','1','2','3','4'])
                    if chosenexam=='0':
                        break
                    else:
                        if chosenexam=='1':
                            chosenexam=ut1
                        if chosenexam=='2':
                            chosenexam=hy
                        if chosenexam=='3':
                            chosenexam=ut2
                        if chosenexam=='4':
                            chosenexam=ae

                    typewrite(f"Please choose the subject for bulk entry (enter '0' for back):\n",end='')
                    count=1

                    for subject in subjects:
                        typewrite(f"{count}. {subject[0]}\n",color='bold cyan',end='')
                        count+=1
                    typewrite("> ",color='bold cyan',end='')
                    chosensub=input()

                    if chosensub=='0':
                        break
                    else:
                        while not (chosensub.isdigit() and 1 <= int(chosensub) <= len(subjects)):
                            typewrite("Please choose from the given options only!\n> ", color='bold yellow', end='')
                            chosensub=input()
                            
                                
                    chosensub=subjects[int(chosensub)-1][0]
                    print(chosensub)
                    cur.execute("SELECT STUDENTS.GRNO FROM STUDENTS WHERE CLASS=%s AND SUBNORDER BY ROLL",(cls,))
                    stddata=cur.fetchall()
                    cnt=0
                    for std in stddata:
                        grno=std[0]
                        name=std[1]
                        father=std[2]
                        mother=std[3]
                        dob=std[4]
                        cl=std[5]
                        roll=std[6]

                        typewrite(f"GR no.: {grno}\nName: {name}\nRoll no.: {roll}\nEnter Marks ('0' for back): \n> ",color='bold cyan',end='')
                        newmarks=int(input())
                    
                        if newmarks==0:
                            if cnt>0:
                                typewrite("Save data entered till now? (Y/N)\n> ",color='bold red',end='')
                                inp=valid_input(['Y','y','N','n'])
                                if inp.lower()=='y':
                                    db.commit()
                                    typewrite("Changes Saved!",color='bold green',end='')
                            break
                        else:
                            cur.execute("UPDATE MARKS SET MARKS = %s WHERE GRNO = %s AND SUBID = (SELECT SUBID FROM SUBJECTS WHERE SUBNAME = %s) AND EXAM = %s",(newmarks,grno,chosensub,chosenexam))
                            cnt+=1

                    if count==len(stddata):
                        typewrite("Marks entered for all students!\nUpdate marks to the database? (Y/N)\n> ",color='bold yellow',end='')
                        inp=valid_input(['Y','y','N','n'])
                        if inp.lower()=='y':
                            db.commit()
                            typewrite("Marks updated for all students successfully... Returning home!",color='bold green',end='')
                        

        if mainchoice=='2':
            return
        if mainchoice=='3':
            typewrite("Thanks for using our program!",color='bold green',end='')
            exit()
#INTRO

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='yoursql',
    database='gradely'
)
cur=db.cursor()
ct('Mrs. Sheenu Rajesh','12b05')

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
            cur=db.cursor()
            dbconnect(cur,db)
            break

    except mysql.connector.Error as e:
        if e.errno==1045:
            typewrite("Incorrect username or password... Please try again!",color='bold red')
        else:
            typewrite(f"Encountered {e}... Please try again!",color='bold red')


        
progress_bar()

home()

db.close()