import database

database.init_db
#database.create_note("Grocery: milk, bread, cheese, juice, bananas")
#database.create_note("ToDo: shopping, haircut, doctor appointment")
#database.create_note("I love this world")

#database.read_notes()

#database.search_note('shop')

print("By id:")
database.find_note_by_id(7)

#database.update_note(7, 'I still love this stupid world!')


database.close_connection()