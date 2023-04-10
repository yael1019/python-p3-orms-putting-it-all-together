import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None) -> None:
        self.id = None
        self.name = name
        self.breed = breed 
    
    def __repr__(self):
        return f'< Dog id={self.id} name={self.name} breed={self.breed} >'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, [self.name, self.breed])
        CONN.commit()
        self.id = CURSOR.execute('SELECT * FROM dogs ORDER BY id DESC LIMIT 1').fetchone()[0]

    @classmethod
    def new_from_db(cls, row):
        dog = Dog(
            name = row[1],
            breed = row[2],
            id = row[0]
        )
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        list_of_all = [Dog(data[1], data[2], data[0]) for data in all]
        return list_of_all