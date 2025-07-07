import database

#database.create_note("Grocery: milk, bread, cheese, juice, bananas")
#database.create_note("ToDo: shopping, haircut, doctor appointment")
#database.create_note("I love this world")

database.read_notes()

database.search_note('shop')

database.close_connection()