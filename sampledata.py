
import mysql.connector as sql
import random
from datetime import datetime, timedelta
import bcrypt
from rich.console import Console

db=sql.connect(host='localhost',user='root',password='yoursql',database='gradely')
cur=db.cursor()

console=Console()

def setupadm():
    dat={'admin1':'welcome','hamzah':'hamzahiisj'}
    for i in dat:
        password=dat[i]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        query = "INSERT INTO adm (username, hashed_pw) VALUES (%s, %s)"
        data = (i, hashed)
        cur.execute(query, data)
    db.commit()
#setupadm() #use this when creating sample for this table

def setupsubjects():
    subco= {
        'English': '301',
        'Physics': '042',
        'Chemistry': '043',
        'Biology': '044',
        'Mathematics': '041',
        'Marketing': '812',
        'Accounts': '055',
        'Business': '054',
        'Economics': '030',
        'PEd': '048',
        'Computer': '083',
        'IP': '065',
        'Arabic': '116',
        'Urdu': '303'
    }

    for subject in subco:
        cur.execute(f'insert into subjects(subid,subname) values ("{subco[subject]}","{subject}")')
        db.commit()
#setupsubjects() #use this when creating sample for this table

def setupexams():
    sub={'English':80,'Physics':70,'Chemistry':70,'Biology':70,'Mathematics':80,'Marketing':80,'Accounts':80,'Business':80,'Economics':80,'PEd':70,'Computer':70,'IP':70,'Arabic':80,'Urdu':80}
    exams=['Unit Test 1','Half Yearly Exam','Unit Test 2','Annual Exam']

    for subject in sub:

        cur.execute(f'SELECT subid FROM subjects WHERE subname = "{subject}"')
        subid = cur.fetchone()[0]

        for exam in exams:
            if 'Unit' in exam:
                temp=(exam,subid,25)
                cur.execute(f'insert into exams values{temp}')

            else:
                x=sub[subject]
                temp=(exam,subid,x)
                cur.execute(f'insert into exams values{temp}')
            
    db.commit()
#setupexams() #use this when creating sample for this table

def setupteachers():
    strs={'English':['Mrs. Farhana Khan','Mrs. Amena Khan','Mr. Alavi Said'],'Physics':['Mr. Mariadas Thomas'],'Chemistry':['Mrs. Sheenu Rajesh','Mr. Biju Anthony'],
            'Biology':['Dr. Javeed Iftekhar'],'Mathematics':['Mr. Hari Krishna','Mr. Javed Aslam'],'PEd':['Mr. Imran Khan','Mr. Aadil'],'Computer':['Mrs. Urooj Fatima','Mr. Qurban'],
            'Ip':['Mrs. Urooj Fatima','Mr. Qurban'],'Urdu':['Mr. Obaid Khan'],'Arabic':['Mr. Altaf Hussain'],'Business':['Mrs. Safa','Mrs. Shaniba','Mrs. Nasera'],
            'Accounts':['Mr. Akram','Mrs. Siddiqua Bano'],'Economics':['Mr. Sainuddeen','Mr. Feroz Kidwai'],'Marketing':['Mrs. Safa','Mrs. Nasera','Mrs. Siddiqua Bano']}
    used_tids = []

    # SQL query for inserting data
    insert_query = "INSERT INTO Teachers (TID, TName) VALUES (%s, %s)"
    l=[]
    for subject in strs:
        for teacher in strs[subject]:
            if teacher in l:
                continue
            l.append(teacher)
            # Generate a unique TID
            while True:
                tid = random.randint(10000, 99999)
                if tid not in used_tids:
                    used_tids.append(tid)
                    break

            # Execute the query
            try:
                cur.execute(insert_query, (tid, teacher))
            except sql.connector.Error as err:
                print(f"Error inserting {teacher}: {err}")

    # Commit changes to the database
    db.commit()
#setupteachers() #use this when creating sample for this table

def setupteachersubjects():
    strs={'English':['Mrs. Farhana Khan','Mrs. Amena Khan','Mr. Alavi Said'],'Physics':['Mr. Mariadas Thomas'],'Chemistry':['Mrs. Sheenu Rajesh','Mr. Biju Anthony'],
            'Biology':['Dr. Javeed Iftekhar'],'Mathematics':['Mr. Hari Krishna','Mr. Javed Aslam'],'PEd':['Mr. Imran Khan','Mr. Aadil'],'Computer':['Mrs. Urooj Fatima','Mr. Qurban'],
            'Ip':['Mrs. Urooj Fatima','Mr. Qurban'],'Urdu':['Mr. Obaid Khan'],'Arabic':['Mr. Altaf Hussain'],'Business':['Mrs. Safa','Mrs. Shaniba','Mrs. Nasera'],
            'Accounts':['Mr. Akram','Mrs. Siddiqua Bano'],'Economics':['Mr. Sainuddeen','Mr. Feroz Kidwai'],'Marketing':['Mrs. Safa','Mrs. Nasera','Mrs. Siddiqua Bano']}

    for subject in strs:
        # Fetch SubID for the subject
        cur.execute("SELECT SubID FROM Subjects WHERE SubName = %s", (subject,))
        result = cur.fetchone()
        if result is None:
            print(f"Subject '{subject}' not found in database.")
            continue
        subid = result[0]

        # Loop through each teacher for the current subject
        for trs in strs[subject]:
            # Fetch TID for the teacher
            cur.execute("SELECT TID FROM Teachers WHERE TName = %s", (trs,))
            teacher_result = cur.fetchone()
            if teacher_result is None:
                print(f"Teacher '{trs}' not found in database.")
                continue
            tid = teacher_result[0]

            # Insert into TeacherSubjects if not already exists
            
            cur.execute("INSERT INTO TeacherSubjects (TID, SubID) VALUES (%s, %s)", (tid, subid))
    db.commit()
#setupteachersubjects() #use this when creating sample for this table

def setupcts():
    # CREATE TABLE CTs(
    # CTID INT PRIMARY KEY,
    # CTName VARCHAR(30),
    # Hashed_PW VARBINARY(60),
    # FOREIGN KEY(CTID) REFERENCES Teachers(TID) ON DELETE CASCADE
    # );
    classes={'12B01':'Mrs. Urooj Fatima','12B02':'Mrs. Shaniba','12B03':'Mrs. Nasera','12B04':'Mr. Sainuddeen','12B05':'Mrs. Sheenu Rajesh','12B06':'Mr. Alavi Said','12B07':'Mr. Javed Aslam'}

    for cl in classes:
        teacher_name = classes[cl]

        # Generate a password and hash it
        password = teacher_name.split()[1] + 'iisj'
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)

        # Fetch the TID
        cur.execute("SELECT TID FROM Teachers WHERE TName = %s", (teacher_name,))
        tid_result = cur.fetchone()
        if tid_result:
            tid = tid_result[0]
        else:
            print(f"Teacher '{teacher_name}' not found in database.")
            continue

        # Insert into CTs table
        cur.execute("INSERT INTO CTs (CTID, CTName, Hashed_PW) VALUES (%s, %s, %s)", (tid, teacher_name, hashed))
    db.commit()
#setupcts() #use this when creating sample for this table

def setupcls():
    # CREATE TABLE Class(
    # Class VARCHAR(15) PRIMARY KEY,
    # CTID INT,
    # CStream VARCHAR(15),
    # FOREIGN KEY(CTID) REFERENCES Teachers(TID) ON DELETE SET NULL
    # );

    classes={'12B01':'Mrs. Urooj Fatima','12B02':'Mrs. Shaniba','12B03':'Mrs. Nasera','12B04':'Mr. Sainuddeen','12B05':'Mrs. Sheenu Rajesh','12B06':'Mr. Alavi Said','12B07':'Mr. Javed Aslam'}

    for cl in classes:
        cls=cl
        cur.execute(f"select tid from teachers where tname='{classes[cl]}'")
        ctid=cur.fetchone()[0]
        if cl.endswith('1') or cl.endswith('2'):
            cstream='Commerce 1'
        elif cl.endswith('3') or cl.endswith('4'):
            cstream='Commerce 2'
        else:
            cstream='Science'
        cur.execute("insert into class values (%s,%s,%s)", (cls,ctid,cstream))

    db.commit()
#setupcls() #use this when creating sample for this table

def setupstudents():
    # CREATE TABLE Students(
    # GRNo INT PRIMARY KEY,
    # Name VARCHAR(30),
    # Father VARCHAR(30),
    # Mother VARCHAR(30),
    # DOB DATE,
    # Class VARCHAR(15) DEFAULT NULL,
    # Roll INT DEFAULT NULL,
    # FOREIGN KEY(Class) REFERENCES Class(Class) ON DELETE SET NULL
    # );
    muslim_male_names = [
        "Muhammad", "Ahmed", "Ali", "Umar", "Hassan", "Hussain", "Abdullah", "Ibrahim", "Yusuf", "Adam",
        "Mustafa", "Abdul Rahman", "Amir", "Ismail", "Salman", "Bilal", "Khalid", "Zaid", "Ayaan", "Mujahid",
        "Imran", "Ammar", "Farhan", "Suleiman", "Usman", "Tariq", "Fahad", "Musa", "Harun", "Rashid",
        "Saad", "Kareem", "Rayyan", "Aziz", "Mahmoud", "Jawad", "Sami", "Adeel", "Rafi", "Sameer",
        "Faisal", "Shahid", "Shakir", "Qasim", "Hakeem", "Jabir", "Zubair", "Yahya", "Anwar", "Zain",
        "Majid", "Younus", "Bashir", "Nadeem", "Ashraf", "Dawood", "Taha", "Adnan", "Anas", "Shafiq",
        "Faizan", "Latif", "Waleed", "Ayman", "Saif", "Shaheer", "Farooq", "Basim", "Zaki", "Saqib",
        "Naveed", "Sohail", "Tamim", "Zeeshan", "Idrees", "Yasir", "Abbas", "Mehdi", "Nauman", "Maaz",
        "Qais", "Luay", "Ihsan", "Tahsin", "Nasir", "Habib", "Murtaza", "Muaz", "Suhail", "Shaaban",
        "Mahdi", "Riyad", "Mujeeb", "Samir", "Marwan", "Iskander", "Baqar", "Raza", "Badr", "Asad",
        "Ihsan", "Hashim", "Azhar", "Jameel", "Tasnim", "Mujtaba", "Sajid", "Arif", "Aadil", "Majeed",
        "Athar", "Ilyas", "Kamran", "Aslam", "Naseem", "Jamal", "Mazin", "Samiullah", "Tanveer", "Wajid",
        "Fadil", "Ghulam", "Noman", "Rizwan", "Zaheer", "Firoz", "Bashar", "Raheem", "Anwar", "Rasheed",
        "Shabbir", "Ikram", "Nayef", "Hadi", "Danish", "Yamin", "Moin", "Kais", "Najib", "Raed",
        "Azam", "Burhan", "Siraj", "Rauf", "Hameed", "Shamsi", "Salah", "Qamar", "Kamran", "Asif",
        "Hashir", "Tabish", "Danyal", "Saleem", "Zameer", "Alam", "Numan", "Sajjad", "Tauqeer", "Fahim",
        "Nabil", "Irfan", "Sarfraz", "Hanif", "Moinuddin", "Sohail", "Waris", "Aadil", "Yunus", "Naseer",
        "Ahmad", "Qamar", "Shamim", "Waqas", "Rameez", "Sadiq", "Azeem", "Hammad", "Adil", "Shahbaz",
        "Shuaib", "Faiz", "Arsalan", "Azeez", "Qadeer", "Umar", "Shaban", "Naasiruddin", "Junaid", "Imtiaz",
        "Alam", "Tasleem", "Shuaib", "Jawed", "Aariz", "Saad", "Ubaid", "Subhan", "Waseem", "Shaheen",
        "Zafar", "Mazhar", "Shaikh", "Naim", "Siddiq", "Nawaz", "Wahid", "Ehtesham", "Saleh", "Shahnawaz",
        "Anees", "Mushtaq", "Javed", "Asghar", "Farhatullah", "Sufyan", "Najm", "Aaqib", "Khizar", "Naeem"
    ]

    muslim_female_names = [
        "Aaliyah", "Aaminah", "Abeer", "Afreen", "Ahlam", "Aisha", "Aleena", "Alia", "Alina", "Amara",
        "Amira", "Anam", "Anisa", "Areeba", "Asma", "Ayat", "Ayisha", "Aziza", "Basma", "Benazir",
        "Bushra", "Daliyah", "Dana", "Durra", "Eimaan", "Eman", "Esma", "Fareeha", "Farida", "Farrah",
        "Faryal", "Fatema", "Fatima", "Fawzia", "Fiza", "Ghazal", "Gulnaz", "Habiba", "Hadiya", "Hafsa",
        "Hala", "Hanan", "Haneen", "Hawa", "Haya", "Hidaya", "Humaira", "Inaya", "Iqra", "Isra",
        "Jamila", "Jannah", "Jawahir", "Jihan", "Kainat", "Khadija", "Khansa", "Kulthum", "Laila", "Lamis",
        "Lamya", "Lina", "Lubna", "Lujain", "Luna", "Maha", "Mahnoor", "Malak", "Mariam", "Marwa",
        "Mashaal", "Khatoon", "Maya", "Meher", "Maryam", "Misbah", "Munira", "Nada", "Nadia", "Nadine",
        "Nafisa", "Naima", "Najat", "Naseem", "Nashwa", "Nasreen", "Nazli", "Neha", "Nida", "Nihal",
        "Nimra", "Noor", "Nour", "Nuha", "Nura", "Nusaybah", "Omaima", "Parveen", "Qamar", "Qudsia",
        "Rabia", "Rahma", "Rania", "Ranya", "Rasha", "Razan", "Reem", "Rida", "Rihana", "Rimsha",
        "Roohina", "Rowaida", "Ruba", "Ruqayya", "Saadia", "Sabah", "Sabeen", "Sadaf", "Sadia", "Sahar",
        "Salma", "Samar", "Sameeha", "Samira", "Sara", "Sarah", "Sarina", "Shabana", "Shadia", "Shaista",
        "Shama", "Shazia", "Sobia", "Suhaila", "Sumaira", "Sumaya", "Tahira", "Tala", "Talia", "Tamara",
        "Tasneem", "Wafa", "Warda", "Yasmin", "Yumna", "Zahra", "Zainab", "Zaira", "Zakia", "Zain",
        "Zaina", "Zainah", "Zakiyah", "Zara", "Zarifa", "Zeba", "Zehra", "Zehraa", "Zia", "Zoya",
        "Zuleikha", "Abida", "Aasiya", "Aasifa", "Aisha", "Asra", "Ayesha", "Azka", "Benish", "Dilshad",
        "Elaf", "Fahmida", "Fajr", "Farah", "Farzana", "Ghazala", "Gulzar", "Haleema", "Hania", "Heer",
        "Hira", "Iqbal", "Irsa", "Jaida", "Jehan", "Juhi", "Kashifa", "Mahira", "Maliha", "Meherun",
        "Mehr", "Mehwish", "Munazza", "Muntaha", "Nabila", "Nabiha", "Nargis", "Nashita", "Nayab",
        "Nazish", "Rabea", "Rabia", "Raheela", "Rahima", "Rayya", "Rimsha", "Rubina", "Saima", "Saniya",
        "Sanober", "Shagufta", "Sobia", "Tanveer", "Tayyaba", "Uzma", "Safa", "Wahida", "Zahara",
        "Zarina", "Zinat", "Zohra"
    ]

    def generate_random_dob(min_age=17, max_age=19):
        # Get the current date
        current_date = datetime.now()
        
        # Calculate the oldest and youngest dates of birth
        max_dob = current_date - timedelta(days=(min_age * 365))
        min_dob = current_date - timedelta(days=(max_age * 365))

        # Generate a random date within the range
        random_dob = min_dob + (max_dob - min_dob) * random.random()
        
        # Format the date in SQL format
        return random_dob.strftime('%Y-%m-%d')

    classes={'12B01':'Mrs. Urooj Fatima','12B02':'Mrs. Shaniba','12B03':'Mrs. Nasera','12B04':'Mr. Sainuddeen','12B05':'Mrs. Sheenu Rajesh','12B06':'Mr. Alavi Said','12B07':'Mr. Javed Aslam'}
    grnos=[]
    for cl in classes:
        strength=random.randrange(40,50)
        for i in range(strength):
            grno=random.randrange(45000,59999)
            while grno in grnos:
                grno=random.randrange(45000,59999)
            grnos.append(grno)
            fatherfirst=random.choice(muslim_male_names)
            fatherlast=random.choice(muslim_male_names)
            son=random.choice(muslim_male_names)
            motherfirst=random.choice(muslim_female_names)
            motherlast=random.choice(muslim_female_names)
            father=fatherfirst+' '+fatherlast
            name=son+' '+fatherfirst
            mother=motherfirst+' '+motherlast
            dob=generate_random_dob()
            roll=i+1
            tup=(grno,name,father,mother,dob,cl,roll)
            cur.execute("insert into students values(%s,%s,%s,%s,%s,%s,%s)",tup)
            
    db.commit()
#setupstudents() #use this when creating sample for this table

def setupstudentsubjects():
    # CREATE TABLE StudentSubjects(
    # GRNo INT,
    # SubID CHAR(3),
    # PRIMARY KEY (GRNo, SubID),
    # FOREIGN KEY (GRNo) REFERENCES Students(GRNo) ON DELETE CASCADE,
    # FOREIGN KEY (SubID) REFERENCES Subjects(SubID) ON DELETE CASCADE
    # );

    # Fetch all GR numbers
    cur.execute("SELECT grno FROM students")
    grnolist = cur.fetchall()

    # Subject lists
    c1comp = ['English', 'Marketing', 'IP', 'Business']
    c1opt = ['PEd', 'Urdu', 'Arabic']
    c2comp = ['English', 'Accounts', 'Business', 'Economics']
    c2opt = ['Mathematics', 'IP', 'Marketing', 'PEd', 'Urdu', 'Arabic']
    scomp = ['English', 'Physics', 'Chemistry']
    sopt1 = ['Mathematics', 'Biology']
    sopt2 = ['Biology', 'Computer', 'PEd', 'Urdu', 'Arabic']

    for grno in grnolist:
        # Fetch the stream for the student
        cur.execute(
            "SELECT cstream FROM class JOIN students ON students.class = class.class WHERE grno = %s",
            (grno[0],)
        )
        cstream = cur.fetchone()[0]

        # Determine subjects based on stream
        if cstream == 'Commerce 1':
            sub = c1comp + [random.choice(c1opt)]
        elif cstream == 'Commerce 2':
            sub = c2comp + [random.choice(c2opt)]
        else:  # Science stream
            s4 = random.choice(sopt1)
            s5 = random.choice([opt for opt in sopt2 if opt != s4])
            sub = scomp + [s4, s5]

        # Map subjects to subid and insert into studentsubjects
        for s in sub:
            cur.execute("SELECT subid FROM subjects WHERE subname = %s", (s,))
            subid_result = cur.fetchone()
            if subid_result:  # Check if subject exists
                subid = subid_result[0]
                cur.execute("INSERT INTO studentsubjects VALUES (%s, %s)", (grno[0], subid))

    # Commit the transaction
    db.commit()
    #select subjects.subid,subjects.subname from subjects join studentsubjects on subjects.subid=studentsubjects.subid where grno=49869;
#setupstudentsubjects() #use this when creating sample for this table

def setupmarks():
    # CREATE TABLE Marks(
    # GRNo INT,
    # SubID CHAR(3),
    # Exam VARCHAR(30),
    # Marks INT,
    # PRIMARY KEY (GRNo, SubID, Exam),
    # FOREIGN KEY (GRNo) REFERENCES Students(GRNo) ON DELETE CASCADE,
    # FOREIGN KEY (SubID) REFERENCES Subjects(SubID) ON DELETE CASCADE,
    # FOREIGN KEY (Exam, SubID) REFERENCES Exams(Exam, SubID) ON DELETE CASCADE
    # );

    def generate_marks(maxmarks,choice):
        if choice=='low':
            percentage=random.randrange(10,40)/100
            marks=int(percentage*maxmarks)
        elif choice=='med':
            percentage=random.randrange(40,70)/100
            marks=int(percentage*maxmarks)
        else:
            percentage=random.randrange(70,95)/100
            marks=int(percentage*maxmarks)
        return marks
    # Fetch all GRNos
    cur.execute("SELECT GRNo FROM Students")
    grno_list = cur.fetchall()

    # Fetch exams
    cur.execute("SELECT DISTINCT Exam FROM Exams")
    exam_list = cur.fetchall()

    # Iterate through students
    for grno in grno_list:
        # Fetch subjects specific to this student
        cur.execute("SELECT SubID FROM StudentSubjects WHERE GRNo = %s", (grno[0],))
        subject_list = cur.fetchall()
        prob=['low','med','med','med','med','med','med','high','high']
        choice=random.choice(prob)
        # Assign marks for each subject and exam
        for subid in subject_list:
            for exam in exam_list:
                cur.execute("select maxmarks from exams where exam= %s", exam)
                maxmarks=cur.fetchall()[0][0]
                marks = generate_marks(maxmarks,choice)  # Use the function to generate marks
                cur.execute(
                    "INSERT INTO Marks (GRNo, SubID, Exam, Marks) VALUES (%s, %s, %s, %s)",
                    (grno[0], subid[0], exam[0], marks)
                )

    db.commit()
#setupmarks() #use this when creating sample for this table

def setupclasssubjects():
    # CREATE TABLE ClassSubjects(
    # Class VARCHAR(15),
    # SubID CHAR(3),
    # TID INT,
    # PRIMARY KEY (Class, SubID),
    # FOREIGN KEY (Class) REFERENCES Class(Class) ON DELETE CASCADE,
    # FOREIGN KEY (SubID) REFERENCES Subjects(SubID) ON DELETE CASCADE,
    # FOREIGN KEY (TID) REFERENCES Teachers(TID) ON DELETE SET NULL
    # );

    strs={'English':[['Mrs. Farhana Khan','Mrs. Amena Khan','Mr. Alavi Said'],['12b01','12b02','12b03','12b04','12b05','12b06','12b07']],
        'Physics':[['Mr. Mariadas Thomas'],['12b05','12b06','12b07']],
        'Chemistry':[['Mrs. Sheenu Rajesh','Mr. Biju Anthony'],['12b05','12b06','12b07']],
                'Biology':[['Dr. Javeed Iftekhar'],['12b05','12b06','12b07']],
                'Mathematics':[['Mr. Hari Krishna','Mr. Javed Aslam'],['12b03','12b04','12b05','12b06','12b07']],
                'PEd':[['Mr. Imran Khan','Mr. Aadil'],['12b01','12b02','12b03','12b04','12b05','12b06','12b07']],
                'Computer':[['Mrs. Urooj Fatima','Mr. Qurban'],['12b05','12b06','12b07']],
                'Ip':[['Mrs. Urooj Fatima','Mr. Qurban'],['12b01','12b02','12b03','12b04']],
                'Urdu':[['Mr. Obaid Khan'],['12b01','12b02','12b03','12b04','12b05','12b06','12b07']],
                'Arabic':[['Mr. Altaf Hussain'],['12b01','12b02','12b03','12b04','12b05','12b06','12b07']],
                'Business':[['Mrs. Safa','Mrs. Shaniba','Mrs. Nasera'],['12b01','12b02','12b03','12b04']],
                'Accounts':[['Mr. Akram','Mrs. Siddiqua Bano'],['12b03','12b04']],
                'Economics':[['Mr. Sainuddeen','Mr. Feroz Kidwai'],['12b03','12b04']],
                'Marketing':[['Mrs. Safa','Mrs. Nasera','Mrs. Siddiqua Bano'],['12b01','12b02','12b03','12b04']]}
        
    for subject in strs:
        cur.execute("select subid from subjects where subname = %s",(subject,))
        subid=cur.fetchone()[0]
        classes=strs[subject][1]
        teachers=strs[subject][0]
        tids=[]
        for teacher in teachers:
            cur.execute("select tid from teachers where tname = %s",(teacher,))
            temp=cur.fetchone()[0]
            tids.append(temp)
        nc=len(classes)
        nt=len(teachers)
        x=nc//nt
        r=nc%nt
        count=0
        random.shuffle(tids)
        for tid in tids:
            for _ in range(x):
                cls=classes[count]
                cur.execute("insert into classsubjects values (%s,%s,%s)",(cls,subid,tid))
                count+=1
        for _ in range(r):
            cls=classes[count]
            tid=random.choice(tids)
            cur.execute("insert into classsubjects values (%s,%s,%s)",(cls,subid,tid))
            count+=1

    db.commit()
#setupclasssubjects() #use this when creating sample for this table


def newacadyear(): 
    with console.status("[yellow]Archiving data, please wait...[/]", spinner="dots") as status:
        setupsubjects()
        console.print("[green]Inserted new sample data for subjects table.[/]")
        setupexams()
        console.print("[green]Inserted new sample data for exams table.[/]")
        setupteachers()
        console.print("[green]Inserted new sample data for teachers table.[/]")
        setupteachersubjects()
        console.print("[green]Inserted new sample data for teachersubjects table.[/]")
        setupcls()
        console.print("[green]Inserted new sample data for class table.[/]")
        setupstudents() 
        console.print("[green]Inserted new sample data for students table.[/]")
        setupstudentsubjects()
        console.print("[green]Inserted new sample data for studentsubjects table.[/]")
        setupmarks()
        console.print("[green]Inserted new sample data for marks table.[/]")
        setupclasssubjects()
        console.print("[green]Inserted new sample data for classsubjects table.[/]")
    
newacadyear() # use this after creating new acadyear

db.close()