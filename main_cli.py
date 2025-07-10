import database

# Main menu
def show_menu():
    print("\n==== Notify App ====")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes by title")
    print("4. View and manage a note")
    print("0. Exit")


# Main processing loop
def cli_loop():
    
    database.init_db()
    
    while True:
        show_menu()
        choice = input("Enter menu option: ").strip()

        if choice == '1':
            content = input("Enter note content: \n")
            database.create_note(content)

        elif choice == '2':
            database.read_notes()

        elif choice == '3':
            keyword = input("Enter keyword to search by title: ")
            database.search_note(keyword)

        elif choice == '4':
            try:
                note_id = int(input("Enter note number to modify: "))
                result = database.find_note_by_id(note_id)
                if result:
                    note_actions_menu(note_id)
            except ValueError:
                print("Invalid option. Try againg: ")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again: ")


# Menu to manage a note
def note_actions_menu(note_id):
    while True:
        print("\n==== Notify App ====")
        print("\n--- What would you like to do? ---")
        print("1. Modify note")
        print("2. Delete note")
        print("0. Back to main menu")

        choice = input("Enter menu option: ").strip()
        
        if choice == '1':
            new_content = input("Enter new content: \n")
            database.update_note(note_id, new_content)

        elif choice == '2':
            confirm = input("Are you sure you want to delete this note? (y/n): ")
            if confirm.lower() == 'y':
                database.delete_note_by_id(note_id)
                break
            else:
                print("Deletion cancelled.")

        elif choice == '0':
                break
        
        else:
            print("Invalid option. Try again.")


    
if __name__ == "__main__":
    cli_loop()