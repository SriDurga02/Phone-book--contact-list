import pymysql

def connect_db():
    """
    Define a function to connect to the database
    """
    return pymysql.connect(
        host='localhost',  # Change as per your MySQL server
        user='root',  # Change to your MySQL username
        password='Rahimmal@2024',  # Change to your MySQL password
        database='phonebook'  # Change to your database name
    )


def welcome():
    """
    Define a function to welcome the user and provide options
    """
    print("1. Display Your existing contacts")
    print("2. Create a New contact")
    print("3. Check an entry")
    print("4. Delete an entry")
    print("5. Exit")
    entry = int(input("Enter your entry here (1, 2, 3, 4, or 5): "))
    return entry


def display_contacts(connection):
    """
    Define a function to display all contacts from the database
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        if rows:
            for i, row in enumerate(rows):
                print(f"{i}.--> {row[1]}")
        else:
            print('You have an empty phonebook! Go back to the menu to add a new contact')

def create_contact(connection):
    """
    Define a function to create a new contact in the database
    """
    phone_number = input('Please Enter a number: ')
    contact_name = input('What would you like to save the name as? Enter in the format "FirstName,LastName": ')
    
    with connection.cursor() as cursor:
        # Check if the contact already exists
        cursor.execute("SELECT * FROM contacts WHERE phone_number = %s", (phone_number,))
        if cursor.fetchone() is None:
            # Insert new contact
            cursor.execute("INSERT INTO contacts (name, phone_number) VALUES (%s, %s)", (contact_name, phone_number))
            connection.commit()
            print('Contact successfully saved')
        else:
            print('That contact already exists in your Phonebook')


def check_entry(connection):
    """
    Define a function to check a specific contact entry
    """
    name = input('Enter the name of the contact details you wish to view: ')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM contacts WHERE name = %s", (name,))
        result = cursor.fetchone()
        if result:
            print(f"The contact is {result[0]}: {result[1]}")
        else:
            print('That contact does not exist! Return to the main menu to enter the contact')


def delete_contact(connection):
    """
    Define a function to delete a contact from the database
    """
    name = input('Enter the name of the contact you wish to delete: ')
    
    with connection.cursor() as cursor:
        # Check if the contact exists
        cursor.execute("SELECT * FROM contacts WHERE name = %s", (name,))
        result = cursor.fetchone()
        if result:
            confirm = input('Are you sure you wish to delete this contact? Yes/No: ')
            if confirm.capitalize() == 'Yes':
                # Delete the contact
                cursor.execute("DELETE FROM contacts WHERE name = %s", (name,))
                connection.commit()
                print('Contact deleted successfully')
            else:
                print('Return to Main Menu')
        else:
            print('That contact does not exist!')


def phonebook():
    """
    Define the main function Phonebook
    """
    connection = connect_db()

    while True:
        entry = welcome()

        if entry == 1:
            display_contacts(connection)
        elif entry == 2:
            create_contact(connection)
        elif entry == 3:
            check_entry(connection)
        elif entry == 4:
            delete_contact(connection)
        elif entry == 5:
            print('Thanks for using the Py Contact Book')
            connection.close()  # Close the database connection
            break
        else:
            print('Incorrect Entry!')


# Run the Phonebook Program
phonebook()