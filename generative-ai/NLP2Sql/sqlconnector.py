import sqlite3

def get_connection():
## Connectt to SQlite
    connection=sqlite3.connect("student.db")
    return connection


def create_table_and_insert_data():
    # Create a cursor object to insert record,create table
    connection = get_connection()
    cursor=connection.cursor()

    ## create the table
    table_info="""
    Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
    SECTION VARCHAR(25),MARKS INT);

    """
    cursor.execute(table_info)

    ## Insert Some more records

    cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
    cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
    cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
    cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
    cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')
    
    ## Commit your changes int he databse
    connection.commit()
    connection.close()

def display_data():
    ## Disspaly ALl the records
    connection = get_connection()
    cursor=connection.cursor()
    print("The isnerted records are")
    data=cursor.execute('''Select * from STUDENT''')
    for row in data:
        print(row)
    
    ## Commit your changes int he databse
    connection.commit()
    connection.close()



def main():
    print("Hello World!")
    # create_table_and_insert_data()
    display_data()


if __name__ == "__main__":
    main()