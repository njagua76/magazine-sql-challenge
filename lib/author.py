# lib/author.py
from .database_utils import get_connection  # help to connect the SQlite db

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:             #Initialize a new author instance ...also the name must be a string and not empty
            raise ValueError("Author name must be a non-empty string.")
        self.name = name.strip()   #clear any white space 
        self.id = None          #set this later once the author is saved in the db

    @classmethod                     #this class method takes a db row(tuple) and turns it into an author instance
    def new_from_db(cls, row):
        """Instantiate Author from DB row."""
        author = cls(row[1])
        author.id = row[0]
        return author

    def save(self):
        """Insert or update an Author."""
        conn = get_connection()
        cur = conn.cursor()

        if self.id is None:
            cur.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))

        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):      #look for an author from the db by Id if found, return author instance
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM authors WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def articles(self):
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE author_id=?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?;
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]

    def add_article(self, magazine, title):
        from .article import Article
        article = Article(title, self, magazine)
        article.save()
        return article

    def topic_areas(self):
        """Return unique categories from the author's magazines."""
        return list({mag.category for mag in self.magazines()})
