# Gradely
### "Effortless Report Cards, Optimized Results."


**This project is being created for CBSE Class 12 2024-25 Computer Science Practical Exam**


## Instructions:
*To clone this project run the following command through the command prompt (make sure you have git installed in your PC and your working directory is Desktop for better access):

	git clone https://github.com/Mohammad-Hamzah/Gradely
	
* To install the database, execute the following command in the command prompt after cloning the project (make sure your working directory is 'Gradely'):

	`mysql -u root -p gradely < gradely_dump.sql`

* Install the required packages by executing the following command in the command prompt (make sure your working directory is 'Gradely'):

	`pip install -r requirements.txt`
	
* The main code is stored in `Gradely.py`
* You can use the script `sampledata.py` to create tables with random data.
* If issues found, please raise them in the "Issues" tab of this project.
* Suggest ideas, if any, in the "Discussions" tab of this project.

## To use the program:
* To log in as an admin, use Username and Password as admin1-welcom or hamzah-hamzahiisj.
* To log in as teachers, select TID from the table below.
```
+-------+--------------------+-------+
| ID    | TName              | Class |
+-------+--------------------+-------+
| 39387 | Mrs. Urooj Fatima  | 12B01 |
| 89435 | Mrs. Shaniba       | 12B02 |
| 96631 | Mrs. Nasera        | 12B03 |
| 21023 | Mr. Sainuddeen     | 12B04 |
| 45869 | Mrs. Sheenu Rajesh | 12B05 |
| 42997 | Mr. Alavi Said     | 12B06 |
| 22762 | Mr. Javed Aslam    | 12B07 |
+-------+--------------------+-------+
```
* The Password will be the first name followed by 'iisj'. Make sure first letter of name is uppercase. For eg. password for tid=21023 will be 'Sainuddeeniisj'.
* Please note that a teacher can update marks for students belonging to their class only.
* To see data for all students, run the following command in MySQL Client:
  
  `select * from students;`
  
  You may select any Gr No. from here for testing purposes (Make sure you are logged in as the class teacher of the selected student's class).
  For seeing data of students beloning to a specific class:
  
  `select * from students where class=(replace this bracket with the class enclosed in strings(quotes))`
  
  
## Special Thanks:
1. [Zaman](https://github.com/infrared-o8/) for ideas and debugging.
2. Atif Malik for helping in collecting the data for the project.
