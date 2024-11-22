import mysql.connector as sql
from rich.traceback import install #this will show errors beautifully
from rich import print as rprint
from rich.table import Table #this will display tables beautifully
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.progress import Progress, TextColumn, BarColumn #helps to create progress bars and spinners
import time #this module is for time related things
from pwinput import pwinput #this module will mask the password being entered as asterisk(*) on the screen
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Image ,Frame
import bcrypt #for passwords
from PIL import Image
import os



install() #calling the install function will overwrite the current error statement procedure and will show errors beautifully
console=Console()

#colored typewriter function
def typewrite(string,sec=0.01,color='bold cyan',end='\n'):
    for i in string:
        rprint(f"[{color}]{i}[/{color}]", end='',flush=True)        
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
            return True
        
    typewrite("Database not found! Exiting program...",color='bold red')
    return False

def home():
    while True:
        typewrite("Welcome to Gradely!\nPlease choose how you would like to login ('0' to exit):\n1. Admin\n2. Teacher\n> ",color='bold cyan',end='')

        usertype=valid_input(["0","1","2"],warning="Please choose from the given options only! (1/2)")

        while True:

            if usertype=='0':
                typewrite("Thanks for using Gradely!",color='bold green',end='')
                exit()

            if usertype=='1':

                typewrite("Please enter your username: ('0' for back)\n> ",end='') #CANT BE EMPTY
                inputun=input()
                if inputun=='0':
                    break

                typewrite("Please enter your password:\n> ",end='')
                inputpw=pwinput(prompt='')

                #simulating checking password
                spinner(list=['','',''],start='Verifying credentials...',spincolor='yellow',startcolor='bold yellow')

                cur.execute("SELECT * FROM ADM")
                creds=cur.fetchall()
                count=0
                flag=False
                for cred in creds:
                    count+=1
                    if cred[0]==inputun:
                        storedpw=cred[1]
                        if bcrypt.checkpw(inputpw.encode(), storedpw):
                            typewrite("Credentials verified.",color='bold green')
                            progress_bar(start='Logging in...',startcolor='bold green')
                            admin(cred[0],inputpw)
                            flag=True
                            break
                        else:
                            typewrite("Incorrect username or password! Please try again!",color='bold red')
                if count==len(creds) and not flag:
                    typewrite("Incorrect username or password! Please try again!",color='bold red')


            else:

                typewrite("Please enter your ID: ('0' for back)\n> ",end='') #CANT BE EMPTY
                inputid=input()
                if inputid=='0':
                    break
                typewrite("Please enter your password:\n> ",end='')
                inputpw=pwinput(prompt='')

                #simulating checking password
                spinner(list=['','',''],start='Verifying credentials...',spincolor='yellow',startcolor='bold yellow')

                cur.execute("SELECT * FROM CTS")
                creds=cur.fetchall()
                count=0
                flag=False
                for cred in creds:
                    count+=1
                    if str(cred[0])==inputid:
                        storedpw=cred[2]
                        if bcrypt.checkpw(inputpw.encode(), storedpw):
                            typewrite("Credentials verified.",color='bold green')
                            progress_bar(start='Logging in...',startcolor='bold green')
                            cur.execute("SELECT DISTINCT CLASS FROM CTS,CLASS WHERE CLASS.CTID=%s",(cred[0],))
                            cls=cur.fetchone()[0]
                            ct(cred[1],cls)
                            flag=True
                            break
                if count==len(creds) and not flag:
                    typewrite("Incorrect ID or password! Please try again!",color='bold red')

def hash_pw(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def info(grno):
    
    cur.execute("SELECT * FROM STUDENTS WHERE GRNO=%s",(grno,))
    stddata=cur.fetchall()
    name,father,mother,dob,cl,roll=stddata[0][1],stddata[0][2],stddata[0][3],stddata[0][4],stddata[0][5],stddata[0][6]
    cur.execute("SELECT SUBNAME FROM SUBJECTS,STUDENTSUBJECTS WHERE SUBJECTS.SUBID=STUDENTSUBJECTS.SUBID AND GRNO=%s",(grno,))
    subdata=cur.fetchall()
    s1,s2,s3,s4,s5=subdata[0][0],subdata[1][0],subdata[2][0],subdata[3][0],subdata[4][0]
    maxs1,maxs2,maxs3,maxs4,maxs5,MAXS1,MAXS2,MAXS3,MAXS4,MAXS5=0,0,0,0,0,0,0,0,0,0

    ms1ut1,ms1hy,ms1ut2,ms1ae=0,0,0,0
    ms2ut1,ms2hy,ms2ut2,ms2ae=0,0,0,0
    ms3ut1,ms3hy,ms3ut2,ms3ae=0,0,0,0
    ms4ut1,ms4hy,ms4ut2,ms4ae=0,0,0,0
    ms5ut1,ms5hy,ms5ut2,ms5ae=0,0,0,0


    count=0
    for subject in subdata:
        cur.execute("SELECT DISTINCT MAXMARKS FROM EXAMS WHERE SUBID=(SELECT SUBID FROM SUBJECTS WHERE SUBNAME=%s) ORDER BY MAXMARKS",(subject[0],))
        maxmarks=cur.fetchall()
        cur.execute("SELECT EXAM,MARKS FROM MARKS WHERE GRNO=%s  AND SUBID=(SELECT SUBID FROM SUBJECTS WHERE SUBNAME=%s) ORDER BY EXAM",(grno,subject[0]))
        obtmarks=cur.fetchall()

        if count==0:
            maxs1,MAXS1=maxmarks[0][0],maxmarks[1][0]
            
        if count==1:
            maxs2,MAXS2=maxmarks[0][0],maxmarks[1][0]
            
        if count==2:
            maxs3,MAXS3=maxmarks[0][0],maxmarks[1][0]
            
        if count==3:
            maxs4,MAXS4=maxmarks[0][0],maxmarks[1][0]
            
        if count==4:
            maxs5,MAXS5=maxmarks[0][0],maxmarks[1][0]


        if obtmarks !=None:
            
            if count==0:
                ms1ae,ms1hy,ms1ut1,ms1ut2=obtmarks[0][1],obtmarks[1][1],obtmarks[2][1],obtmarks[3][1]
                count+=1
            
            elif count==1:
                ms2ae,ms2hy,ms2ut1,ms2ut2=obtmarks[0][1],obtmarks[1][1],obtmarks[2][1],obtmarks[3][1]
                count+=1

            elif count==2:
                ms3ae,ms3hy,ms3ut1,ms3ut2=obtmarks[0][1],obtmarks[1][1],obtmarks[2][1],obtmarks[3][1]
                count+=1
            elif count==3:
                ms4ae,ms4hy,ms4ut1,ms4ut2=obtmarks[0][1],obtmarks[1][1],obtmarks[2][1],obtmarks[3][1]
                count+=1
            elif count==4:
                ms5ae,ms5hy,ms5ut1,ms5ut2=obtmarks[0][1],obtmarks[1][1],obtmarks[2][1],obtmarks[3][1]
                
                
    return [name,father,mother,dob,cl,roll],[s1,s2,s3,s4,s5],[maxs1,maxs2,maxs3,maxs4,maxs5,MAXS1,MAXS2,MAXS3,MAXS4,MAXS5],[ms1ut1,ms1hy,ms1ut2,ms1ae],[ms2ut1,ms2hy,ms2ut2,ms2ae],[ms3ut1,ms3hy,ms3ut2,ms3ae],[ms4ut1,ms4hy,ms4ut2,ms4ae],[ms5ut1,ms5hy,ms5ut2,ms5ae]





def admin(adm,storedpw):
    def new_acadyear():
        tables = ["Marks", "StudentSubjects", "ClassSubjects", "Students", "Subjects", "Exams", "Teachers", "TeacherSubjects", "Class"]
        
        try:
            # Add spinner for archiving process
            with console.status("[yellow]Archiving data, please wait...[/]", spinner="dots",) as status:
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")  # Disable foreign key checks
                for table in tables:
                    archive_table = f"{table}archive"
                    
                    # Archive data with academic year
                    cur.execute(f"INSERT INTO {archive_table} SELECT *, '{acadyear}' FROM {table}")
                    cur.execute(f"TRUNCATE TABLE {table}")  # Clear the original table
                    console.log(f"[green]Archived and cleared data for {table}[/]")

                # Update academic year
                new_acadyearstart = int(yeardata[0]) + 1
                new_acadyearend = int(yeardata[1]) + 1
                cur.execute("TRUNCATE TABLE ACADYEAR")
                cur.execute("INSERT INTO ACADYEAR VALUES (%s, %s)", (new_acadyearstart, new_acadyearend))

                cur.execute("SET FOREIGN_KEY_CHECKS = 1")  # Re-enable foreign key checks
                db.commit()
            console.print("[green]Archiving process completed successfully! [/]")

                
            typewrite("Returning home...\n", color='bold green')
            return

        except sql.Error as e:
            typewrite(f"Error during archiving: {e}...\nOperation Terminated, Returning home...\n", color='bold red')
            db.rollback()
            return

    def minor_report(grno,exam,folder=''):

        if folder!='':
            directory_name = f'results/{folder.rstrip('/')}'
        try:
            os.makedirs(directory_name,exist_ok=True)
        except:
            typewrite("Some Error Occured!",color='bold red')


        stddata,subdata,maxmarks,ms1,ms2,ms3,ms4,ms5=info(grno)
        name,father,mother,dob,cl,roll=stddata[0],stddata[1],stddata[2],stddata[3],stddata[4],stddata[5]
        s1,s2,s3,s4,s5=subdata[0],subdata[1],subdata[2],subdata[3],subdata[4]
        maxs1,maxs2,maxs3,maxs4,maxs5=maxmarks[0],maxmarks[1],maxmarks[2],maxmarks[3],maxmarks[4]
        examshort,examname = '',''
        ms1ut = ms2ut = ms3ut = ms4ut = ms5ut = 0
        if exam==1:
            examname='Unit Test 1'
            examshort='UT1'
            ms1ut=ms1[0]
            ms2ut=ms2[0]
            ms3ut=ms3[0]
            ms4ut=ms4[0]
            ms5ut=ms5[0]
        elif exam==2:
            examname='Unit Test 2'
            examshort='UT2'
            ms1ut=ms1[2]
            ms2ut=ms2[2]
            ms3ut=ms3[2]
            ms4ut=ms4[2]
            ms5ut=ms5[2]


        # Set up the PDF document and canvas
        scale_factor = 2  # Scale up by 2x for higher resolution
        a4_width, a4_height = A4
        high_res_width = int(a4_width * scale_factor)
        high_res_height = int(a4_height * scale_factor)
        
        c = canvas.Canvas(f"results/{folder}{grno}_{examshort}.pdf", pagesize=(high_res_width, high_res_height))
        # width, height = A4  # Get dimensions of the A4 page
        with Image.open(r"assets\header_image.png") as img1:
            image_width, image_height = img1.size  # Get the width and height of the image

        c.drawImage(r"assets\header_image.png", x=0, y=high_res_height - image_height, width=image_width, height=image_height)


        with Image.open(r"assets\principal_stamp.png") as img2:
            image_width, image_height = img2.size  # Get the width and height of the image

        c.drawImage(r"assets\principal_stamp.png", x=852, y=242, width=image_width, height=image_height)


        with Image.open(r"assets\school_stamp.png") as img3:
            image_width, image_height = img3.size  # Get the width and height of the image

        c.drawImage(r"assets\school_stamp.png", x=468, y=164, width=image_width, height=image_height)


        c.setFont("Helvetica-Bold", 37)  # Font and size
        c.drawString(390, 1430, f"Academic Year {acadyear}")  # x, y, and text
        c.drawString(331, 1390, "Performance Report for Class XII")  # x, y, and text

        c.setFont("Helvetica-Bold", 22)  # Font and size
        c.drawString(53, 1280, f"GR No.: {grno}")  # x, y, and text
        c.drawString(483, 1280, f"Class and Section: {cl}")  # x, y, and text
        c.drawString(913, 1280, f"Roll no.: {roll}")  # x, y, and text
        c.drawString(53, 1231, f"Student's Name: {name}")  # x, y, and text
        c.drawString(483, 1231, f"DOB: {dob}")  # x, y, and text
        c.drawString(53, 1183, f"Father's Name: {father}")  # x, y, and text
        c.drawString(483, 1183, f"Mother's Name: {mother}")  # x, y, and text

        c.setFont("Times-Bold", 27)  # Font and size
        c.drawString(171, 248, "Class Teacher")  # x, y, and text

        data=[
            ['Subject',f'{examname}',''],
            ['','Max.','Obt.'],
            [s1,maxs1,ms1ut],
            [s2,maxs2,ms2ut],
            [s3,maxs3,ms3ut],
            [s4,maxs4,ms4ut],
            [s5,maxs5,ms5ut]
        ]

        row_heights = [70] + [50] * len(data[1:])  # Set specific row heights
        table_width = 1100  # Fixed total width in points
        num_columns = len(data[0])  # Number of columns
        column_width = table_width / num_columns  # Calculate width per column


        table = Table(data, colWidths=[column_width] * num_columns,rowHeights=row_heights)  # Column widths

        style = TableStyle([

            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (2, 0)), 
            
            # Center align all text
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Set bold font
            ('FONTSIZE', (0, 0), (-1, -1), 23),  # Increased font size
            # Add grid lines
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding for better readability
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        frame = Frame(53, 438, 1086, 700)  # x, y, width, height
        frame.addFromList([table], c)

        c.showPage()

        c.save()


    def hy_report(grno,folder=''):


        if folder!='':
            directory_name = f'results/{folder.rstrip('/')}'
        try:
            os.makedirs(directory_name,exist_ok=True)
        except:
            typewrite("Some Error Occured!",color='bold red')


        stddata,subdata,maxmarks,ms1,ms2,ms3,ms4,ms5=info(grno)
        name,father,mother,dob,cl,roll=stddata[0],stddata[1],stddata[2],stddata[3],stddata[4],stddata[5]
        s1,s2,s3,s4,s5=subdata[0],subdata[1],subdata[2],subdata[3],subdata[4]
        maxs1,maxs2,maxs3,maxs4,maxs5,MAXS1,MAXS2,MAXS3,MAXS4,MAXS5=maxmarks[0],maxmarks[1],maxmarks[2],maxmarks[3],maxmarks[4],maxmarks[5],maxmarks[6],maxmarks[7],maxmarks[8],maxmarks[9]
        ms1ut1,ms1hy=ms1[0],ms1[1]
        ms2ut1,ms2hy=ms2[0],ms2[1]
        ms3ut1,ms3hy=ms3[0],ms3[1]
        ms4ut1,ms4hy=ms4[0],ms4[1]
        ms5ut1,ms5hy=ms5[0],ms5[1]

        # Set up the PDF document and canvas
        scale_factor = 2  # Scale up by 2x for higher resolution
        a4_width, a4_height = A4
        high_res_width = int(a4_width * scale_factor)
        high_res_height = int(a4_height * scale_factor)
        
        c = canvas.Canvas(f"results/{folder}{grno}_HY.pdf", pagesize=(high_res_width, high_res_height))
        # width, height = A4  # Get dimensions of the A4 page
        with Image.open(r"assets\header_image.png") as img1:
            image_width, image_height = img1.size  # Get the width and height of the image

        c.drawImage(r"assets\header_image.png", x=0, y=high_res_height - image_height, width=image_width, height=image_height)


        with Image.open(r"assets\principal_stamp.png") as img2:
            image_width, image_height = img2.size  # Get the width and height of the image

        c.drawImage(r"assets\principal_stamp.png", x=852, y=242, width=image_width, height=image_height)


        with Image.open(r"assets\school_stamp.png") as img3:
            image_width, image_height = img3.size  # Get the width and height of the image

        c.drawImage(r"assets\school_stamp.png", x=468, y=164, width=image_width, height=image_height)


        c.setFont("Helvetica-Bold", 37)  # Font and size
        c.drawString(390, 1430, f"Academic Year {acadyear}")  # x, y, and text
        c.drawString(331, 1390, "Performance Report for Class XII")  # x, y, and text

        c.setFont("Helvetica-Bold", 22)  # Font and size
        c.drawString(53, 1280, f"GR No.: {grno}")  # x, y, and text
        c.drawString(483, 1280, f"Class and Section: {cl}")  # x, y, and text
        c.drawString(913, 1280, f"Roll no.: {roll}")  # x, y, and text
        c.drawString(53, 1231, f"Student's Name: {name}")  # x, y, and text
        c.drawString(483, 1231, f"DOB: {dob}")  # x, y, and text
        c.drawString(53, 1183, f"Father's Name: {father}")  # x, y, and text
        c.drawString(483, 1183, f"Mother's Name: {mother}")  # x, y, and text

        c.setFont("Times-Bold", 27)  # Font and size
        c.drawString(171, 248, "Class Teacher")  # x, y, and text

        data=[
            ['Subject','Unit Test 1','','Half Yearly Exam',''],
            ['','Max.','Obt.','Max.','Obt.'],
            [s1,maxs1,ms1ut1,MAXS1,ms1hy],
            [s2,maxs2,ms2ut1,MAXS2,ms2hy],
            [s3,maxs3,ms3ut1,MAXS3,ms3hy],
            [s4,maxs4,ms4ut1,MAXS4,ms4hy],
            [s5,maxs5,ms5ut1,MAXS5,ms5hy]
        ]

        row_heights = [70] + [50] * len(data[1:])  # Set specific row heights
        table_width = 1100  # Fixed total width in points
        num_columns = len(data[0])  # Number of columns
        column_width = table_width / num_columns  # Calculate width per column


        table = Table(data, colWidths=[column_width] * num_columns,rowHeights=row_heights)  # Column widths

        style = TableStyle([

            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (2, 0)),  
            ('SPAN', (3, 0), (4, 0)), 
            
            # Center align all text
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Set bold font
            ('FONTSIZE', (0, 0), (-1, -1), 23),  # Increased font size
            # Add grid lines
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding for better readability
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        frame = Frame(53, 438, 1086, 700)  # x, y, width, height
        frame.addFromList([table], c)

        c.showPage()

        c.save()



    def ae_report(grno,folder=''):


        if folder!='':
            directory_name = f'results/{folder.rstrip('/')}'
        try:
            os.makedirs(directory_name,exist_ok=True)
        except:
            typewrite("Some Error Occured!",color='bold red')


        stddata,subdata,maxmarks,ms1,ms2,ms3,ms4,ms5=info(grno)
        name,father,mother,dob,cl,roll=stddata[0],stddata[1],stddata[2],stddata[3],stddata[4],stddata[5]
        s1,s2,s3,s4,s5=subdata[0],subdata[1],subdata[2],subdata[3],subdata[4]
        maxs1,maxs2,maxs3,maxs4,maxs5,MAXS1,MAXS2,MAXS3,MAXS4,MAXS5=maxmarks[0],maxmarks[1],maxmarks[2],maxmarks[3],maxmarks[4],maxmarks[5],maxmarks[6],maxmarks[7],maxmarks[8],maxmarks[9]
        ms1ut1,ms1hy,ms1ut2,ms1ae=ms1[0],ms1[1],ms1[2],ms1[3]
        ms2ut1,ms2hy,ms2ut2,ms2ae=ms2[0],ms2[1],ms2[2],ms2[3]
        ms3ut1,ms3hy,ms3ut2,ms3ae=ms3[0],ms3[1],ms3[2],ms3[3]
        ms4ut1,ms4hy,ms4ut2,ms4ae=ms4[0],ms4[1],ms4[2],ms4[3]
        ms5ut1,ms5hy,ms5ut2,ms5ae=ms5[0],ms5[1],ms5[2],ms5[3]

        # Set up the PDF document and canvas
        scale_factor = 2  # Scale up by 2x for higher resolution
        a4_width, a4_height = A4
        high_res_width = int(a4_width * scale_factor)
        high_res_height = int(a4_height * scale_factor)
        
        c = canvas.Canvas(f"results/{folder}{grno}_AE.pdf", pagesize=(high_res_width, high_res_height))
        # width, height = A4  # Get dimensions of the A4 page
        with Image.open(r"assets\header_image.png") as img1:
            image_width, image_height = img1.size  # Get the width and height of the image

        c.drawImage(r"assets\header_image.png", x=0, y=high_res_height - image_height, width=image_width, height=image_height)


        with Image.open(r"assets\principal_stamp.png") as img2:
            image_width, image_height = img2.size  # Get the width and height of the image

        c.drawImage(r"assets\principal_stamp.png", x=852, y=242, width=image_width, height=image_height)


        with Image.open(r"assets\school_stamp.png") as img3:
            image_width, image_height = img3.size  # Get the width and height of the image

        c.drawImage(r"assets\school_stamp.png", x=468, y=164, width=image_width, height=image_height)


        c.setFont("Helvetica-Bold", 37)  # Font and size
        c.drawString(390, 1430, f"Academic Year {acadyear}")  # x, y, and text
        c.drawString(331, 1390, "Performance Report for Class XII")  # x, y, and text

        c.setFont("Helvetica-Bold", 22)  # Font and size
        c.drawString(53, 1280, f"GR No.: {grno}")  # x, y, and text
        c.drawString(483, 1280, f"Class and Section: {cl}")  # x, y, and text
        c.drawString(913, 1280, f"Roll no.: {roll}")  # x, y, and text
        c.drawString(53, 1231, f"Student's Name: {name}")  # x, y, and text
        c.drawString(483, 1231, f"DOB: {dob}")  # x, y, and text
        c.drawString(53, 1183, f"Father's Name: {father}")  # x, y, and text
        c.drawString(483, 1183, f"Mother's Name: {mother}")  # x, y, and text

        c.setFont("Times-Bold", 27)  # Font and size
        c.drawString(171, 248, "Class Teacher")  # x, y, and text

        data=[
            ['Subject','Unit Test 1','','Half Yearly Exam','','Unit Test 2','','Annual Exam',''],
            ['','Max.','Obt.','Max.','Obt.','Max.','Obt.','Max.','Obt.'],
            [s1,maxs1,ms1ut1,MAXS1,ms1hy,maxs1,ms1ut2,MAXS1,ms1ae],
            [s2,maxs2,ms2ut1,MAXS2,ms2hy,maxs2,ms2ut2,MAXS2,ms2ae],
            [s3,maxs3,ms3ut1,MAXS3,ms3hy,maxs3,ms3ut2,MAXS3,ms3ae],
            [s4,maxs4,ms4ut1,MAXS4,ms4hy,maxs4,ms4ut2,MAXS4,ms4ae],
            [s5,maxs5,ms5ut1,MAXS5,ms5hy,maxs5,ms5ut2,MAXS5,ms5ae]
        ]

        row_heights = [70] + [50] * len(data[1:])  # Set specific row heights
        table = Table(data, colWidths=[200,110,110,110,110,110,110,110,110,110,110],rowHeights=row_heights)  # Column widths

        style = TableStyle([

            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (2, 0)),
            ('SPAN', (3, 0), (4, 0)), 
            ('SPAN', (5, 0), (6, 0)),  
            ('SPAN', (7, 0), (8, 0)), 
            
            # Center align all text
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Set bold font
            ('FONTSIZE', (0, 0), (-1, -1), 23),  # Increased font size
            # Add grid lines
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding for better readability
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        frame = Frame(53, 438, 1086, 700)  # x, y, width, height
        frame.addFromList([table], c)

        c.showPage()

        c.save()

    #admin function content starts here
    while True:
        typewrite(f"Welcome back, {adm}!\nPlease choose from the given options:\n1. Generate Report Card\n2. Start New Academic Year\n3. Change Password\n4. Logout\n5. Exit\n> ",color='bold cyan',end='')
        mainchoice=valid_input(['1','2','3','4','5'])
        if mainchoice=='1':
            typewrite("Please choose how you would like to generate report cards (enter '0' for home):\n1. Single Student\n2. Bulk Generation\n> ",color='bold cyan',end='')
            choice=valid_input(['0','1','2'])
            if choice=='1':
                while True:
                    typewrite("Please enter the student's Grno. (enter '0' for home):\n> ",color='bold cyan',end='')
                    grno=int(input())
                    if grno==0:
                        break
                    else:
                        cur.execute("SELECT * FROM STUDENTS WHERE GRNO=%s",(grno,))
                        stddata=cur.fetchone()
                        if stddata==None:
                            typewrite("Data not found! Please try again!:\n> ",color='bold red',end='')
                        else:
                            typewrite("Please choose the exam (enter '0' for home):\n1. Unit Test 1\n2. Half Yearly Exam\n3. Unit Test 2\n4. Annual Exam\n> ",color='bold cyan',end='')
                            
                            chosenexam=valid_input(['0','1','2','3','4'])
                            if chosenexam=='0':
                                break
                            else:
                                if chosenexam=='1':
                                    minor_report(grno,1)
                                    typewrite("Report generation started... Returning to home...",color='bold green')
                                    break
                                elif chosenexam=='2':
                                    hy_report(grno)
                                    typewrite("Report generation started... Returning to home...",color='bold green')
                                    break
                                elif chosenexam=='3':
                                    minor_report(grno,2)
                                    typewrite("Report generation started... Returning to home...",color='bold green')
                                    break
                                elif chosenexam=='4':
                                    ae_report(grno)
                                    typewrite("Report generation started... Returning to home...",color='bold green')
                                    break

            elif choice=='2':
                
                cur.execute("SELECT CLASS FROM CLASS ORDER BY CLASS")
                cldata=cur.fetchall()
                typewrite("Please chose the class ('0' for home):")
                count=1
                for cl in cldata:
                    typewrite(f"{count}. {cl[0]}")   
                    count+=1                     
                typewrite('> ',end='')
                clinput=int(input())
                while clinput not in range(0,len(cldata)+1):
                    typewrite("Please choose from the given options only!\n> ", color='bold yellow', end='')
                    clinput=int(input())
                
                chosenclass=cldata[clinput-1][0]

                typewrite("Please choose the exam (enter '0' for home):\n1. Unit Test 1\n2. Half Yearly Exam\n3. Unit Test 2\n4. Annual Exam\n> ",color='bold cyan',end='')
                
                chosenexam=valid_input(['0','1','2','3','4'])
                if chosenexam=='0':
                    break
                else:
                    cur.execute("SELECT GRNO FROM STUDENTS WHERE CLASS=%s",(chosenclass,))
                    grnos=cur.fetchall()
                    typewrite("Report generation started...",color='bold green')
                    # Convert grnos (list of tuples) to list of values
                    tasks = [grno[0] for grno in grnos]

                    # Spinner to display progress
                    with console.status(f"[yellow]Generating Reports...", spinner="dots", spinner_style="yellow") as status:
                        for grno in tasks:
                            # Simulate report generation
                            if chosenexam == '1':
                                minor_report(grno, 1, folder=f'{chosenclass}_UT1/')
                            elif chosenexam == '2':
                                hy_report(grno, folder=f'{chosenclass}_HY/')
                            elif chosenexam == '3':
                                minor_report(grno, 2, folder=f'{chosenclass}_UT2/')
                            elif chosenexam == '4':
                                ae_report(grno, folder=f'{chosenclass}_AE/')
                            
                            # Log progress
                            console.log(f"[green]Report for GRNo {grno} generated...[/]")

                    typewrite("Successfully generated all reports. Returning home...", color="bold green")

        if mainchoice=='2':
            typewrite("ARE YOU SURE ABOUT THAT? IF YOU PROCEED YOU WILL BE SOLELY REPONSIBLE FOR THIS! (Y/N)\n> ",color='bold red',end='')
            admchoice=valid_input(['Y','y','N','n'])
            if admchoice.lower()=='y':
                flag=False
                while not flag:
                    typewrite("Enter your password ('0' for home):\n> ",color='bold yellow',end='')
                    p1=pwinput(prompt='')
                    if p1=='0':
                        break
                    typewrite("Enter your password once again ('0' for home):\n> ",color='bold yellow',end='')
                    p2=pwinput(prompt='')
                    if p2=='0':
                        break
                    if p1==p2==storedpw:
                        new_acadyear()
                        flag=True
                    else:
                        typewrite("Passwords incorrect or do not match. Please try again...",color='bold red')

            elif admchoice.lower()=='n':
                typewrite("Returning Home...",color='bold yellow')


        if mainchoice=='3':
            flag=False
            while not flag:
                typewrite("Enter new password ('0' for home):\n> ",color='bold yellow',end='')
                p1=pwinput(prompt='')
                if p1=='0':
                    break
                typewrite("Enter new password once again ('0' for home):\n> ",color='bold yellow',end='')
                p2=pwinput(prompt='')
                if p2=='0':
                    break
                if p1==p2:
                    hashed_pw=hash_pw(p1)
                    cur.execute("UPDATE ADM SET HASHED_PW=%s WHERE USERNAME=%s",(hashed_pw,adm))
                    db.commit()
                    typewrite("Password updated successfully! Returning to home...",color='bold green')
                    flag=True
                else:
                    typewrite("Passwords don't match. Please try again...",color='bold red')
        if mainchoice=='4':
            return
        if mainchoice=='5':
            typewrite("Thanks for using Gradely!",color='bold green',end='')
            exit()




def ct(tname,cls):
    while True:
        typewrite(f"Welcome back, {tname}!\nPlease choose from the given options:\n1. Display Marks\n2. Update Marks\n3. Update Password\n4. Logout\n5. Exit\n> ",color='bold cyan',end='')
        mainchoice=valid_input(['1','2','3','4','5'])
        if mainchoice=='1':
            while True:
                typewrite("Please choose the exam (enter '0' for home):\n1. Unit Test 1\n2. Half Yearly Exam\n3. Unit Test 2\n4. Annual Exam\n> ",color='bold cyan',end='')
                
                chosenexam=valid_input(['0','1','2','3','4'])
                if chosenexam=='0':
                    break
                else:
                    if chosenexam=='1':
                        chosenexam='Unit Test 1'
                    if chosenexam=='2':
                        chosenexam='Half Yearly Exam'
                    if chosenexam=='3':
                        chosenexam='Unit Test 2'
                    if chosenexam=='4':
                        chosenexam='Annual Exam'

                cur.execute("SELECT DISTINCT SUBNAME FROM STUDENTSUBJECTS,STUDENTS,SUBJECTS WHERE STUDENTSUBJECTS.GRNO=STUDENTS.GRNO AND SUBJECTS.SUBID=STUDENTSUBJECTS.SUBID AND STUDENTS.CLASS=%s",(cls,))
                subjects=cur.fetchall()

                        
                typewrite(f"Please choose the subject (enter '0' for back): ")
                count=1
                for subject in subjects:
                    typewrite(f"{count}. {subject[0]}",color='bold cyan')
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

                cur.execute("SELECT ROLL,NAME,MARKS FROM STUDENTS,MARKS WHERE STUDENTS.GRNO=MARKS.GRNO AND CLASS=%s AND SUBID=(SELECT SUBID FROM SUBJECTS WHERE SUBNAME=%s) AND EXAM=%s ORDER BY ROLL",(cls,chosensub,chosenexam))
                stddata=cur.fetchall()
                for std in stddata:
                    roll=std[0]
                    name=std[1]
                    marks=std[2]

                    typewrite(f"Roll no.: {roll}\nName: {name}\nMarks obtained in {chosensub} in {chosenexam}: {marks}",color='bold cyan')
                    print()
                    
                typewrite("Done displaying results... Returning home...",color='bold green')
                print()
                break



        elif mainchoice=='2':
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
                            typewrite(f"Student found...\nGR no.: {grno}\nName: {name}\nRoll no.: {roll}",color='bold green')
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
                                typewrite("Marks updated successfully... Returning to home...",color='bold green')
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

                    typewrite(f"Please choose the subject for bulk entry (enter '0' for back): ")
                    count=1

                    for subject in subjects:
                        typewrite(f"{count}. {subject[0]}",color='bold cyan')
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
                    cur.execute("SELECT STUDENTS.GRNO,STUDENTS.NAME,STUDENTS.ROLL FROM STUDENTS,STUDENTSUBJECTS WHERE STUDENTS.GRNO=STUDENTSUBJECTS.GRNO AND CLASS=%s AND STUDENTSUBJECTS.SUBID=(SELECT SUBID FROM SUBJECTS WHERE SUBNAME=%s) ORDER BY ROLL",(cls,chosensub))
                    stddata=cur.fetchall()
                    cnt=0
                    for std in stddata:
                        grno=std[0]
                        name=std[1]
                        roll=std[2]

                        typewrite(f"GR no.: {grno}\nName: {name}\nRoll no.: {roll}\nEnter Marks ('0' for back): \n> ",color='bold cyan',end='')
                        newmarks=int(input())
                    
                        if newmarks==0:
                            if cnt>0:
                                typewrite("Save data entered till now? (Y/N)\n> ",color='bold red',end='')
                                inp=valid_input(['Y','y','N','n'])
                                if inp.lower()=='y':
                                    db.commit()
                                    typewrite("Changes Saved! Returning back...",color='bold green')
                                
                            break
                        else:
                            cur.execute("UPDATE MARKS SET MARKS = %s WHERE GRNO = %s AND SUBID = (SELECT SUBID FROM SUBJECTS WHERE SUBNAME = %s) AND EXAM = %s",(newmarks,grno,chosensub,chosenexam))
                            cnt+=1

                    if cnt==len(stddata):
                        typewrite("Marks entered for all students!\nUpdate marks to the database? (Y/N)\n> ",color='bold yellow',end='')
                        inp=valid_input(['Y','y','N','n'])
                        if inp.lower()=='y':
                            db.commit()
                            typewrite("Marks updated for all students successfully... Returning to home!",color='bold green')
                            break
                        
        elif mainchoice=='3':
            flag=False
            while not flag:
                typewrite("Enter new password ('0' for home):\n> ",color='bold yellow',end='')
                p1=pwinput(prompt='')
                if p1=='0':
                    break
                typewrite("Enter new password once again ('0' for home):\n> ",color='bold yellow',end='')
                p2=pwinput(prompt='')
                if p2=='0':
                    break
                if p1==p2:
                    hashed_pw=hash_pw(p1)
                    cur.execute("UPDATE CTS SET HASHED_PW=%s WHERE CTID=(SELECT TID FROM TEACHERS WHERE TNAME=%s)",(hashed_pw,tname))
                    db.commit()
                    typewrite("Password updated successfully! Returning to home...",color='bold green')
                    flag=True
                else:
                    typewrite("Passwords don't match. Please try again...",color='bold red')
        elif mainchoice=='4':
            return
        elif mainchoice=='5':
            typewrite("Thanks for using Gradely!",color='bold green',end='')
            exit()
#INTRO

#asking for sql password and username
while True:
    typewrite("Please enter your SQL username (default=root):\n> ",end='')
    sqlu=input()
    typewrite("Please enter your SQL password:\n> ",end='')
    sqlpw=pwinput(prompt='')

    #simulating loading the app
    spinner(list=['','',''],start='Establishing secure connection...',spincolor='yellow',startcolor='bold yellow')

    try:
        # Try to connect to the database
        db = sql.connect(
            host='localhost',
            user=sqlu,
            passwd=sqlpw
        )

        if db.is_connected():
            typewrite("Connected!",color='bold green')
            progress_bar()
            cur=db.cursor()

            isdb=dbconnect(cur,db)
            break

    except sql.Error as e:
        if e.errno==1045:
            typewrite("Incorrect username or password... Please try again!",color='bold red')
        else:
            typewrite(f"Encountered {e}... Please try again!",color='bold red')

if isdb:
    cur.execute("SELECT STARTYEAR,ENDYEAR FROM ACADYEAR")
    global yeardata
    yeardata=cur.fetchone()
    acadyear=str(yeardata[0])+'-'+str(yeardata[1])
    home()

db.close()