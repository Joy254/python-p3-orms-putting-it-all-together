import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    DATABASE_NAME = 'dogs.db'

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  

    @classmethod
    def create_table(cls):
        with sqlite3.connect(cls.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS dogs (
                              id INTEGER PRIMARY KEY,
                              name TEXT,
                              breed TEXT
                              )''')

    @classmethod
    def drop_table(cls):
        with sqlite3.connect(cls.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('DROP TABLE IF EXISTS dogs')

    def save(self):
        with sqlite3.connect(self.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            if self.id is None:
                cursor.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)',
                               (self.name, self.breed))
                self.id = cursor.lastrowid
            else:
                cursor.execute('UPDATE dogs SET name=?, breed=? WHERE id=?',
                               (self.name, self.breed, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM dogs')
            rows = cursor.fetchall()
            return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect(cls.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM dogs WHERE name=?', (name,))
            row = cursor.fetchone()
            if row:
                return cls.new_from_db(row)
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        with sqlite3.connect(cls.DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM dogs WHERE id=?', (dog_id,))
            row = cursor.fetchone()
            if row:
                return cls.new_from_db(row)
            return None

    def update(self):
        self.save()

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    pass
