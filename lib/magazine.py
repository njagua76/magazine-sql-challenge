
from .database_utils import get_connection

class Magazine:
    def __init__(self, name, category):
        if not isinstance(name, str) or len(name.strip()) < 2:                  #Initialize a magazine object..validates that a name is atleast 2 x-ters & also validates that category is a non empty string                                                                      
         raise ValueError("Magazine name must be at least 2 characters.")
        if not isinstance(category, str) or len(category.strip()) == 0:
            raise ValueError("Category must be a non-empty string.")
        self.name = name.strip()
        self.category = category.strip()
        self.id = None   #to be assigned when saved to the database

    @classmethod
    def new_from_db(cls, row):
        mag = cls(row[1], row[2])
        mag.id = row[0]
        return mag

    def save(self):
        conn = get_connection()
        cur = conn.cursor()

        if self.id is None:
            cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)",
                        (self.name, self.category))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE magazines SET name=?, category=? WHERE id=?",
                        (self.name, self.category, self.id))

        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM magazines WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None

    def articles(self):
        from .article import Article
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?;
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM articles WHERE magazine_id=?", (self.id,))
        titles = [row[0] for row in cur.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        """Authors with more than 2 articles in this magazine."""
        from .author import Author
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, COUNT(ar.id) AS article_count
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2;
        """, (self.id,))
        rows = cur.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]

    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT magazine_id, COUNT(id) AS total
            FROM articles
            GROUP BY magazine_id
            ORDER BY total DESC
            LIMIT 1;
        """)
        row = cur.fetchone()
        conn.close()
        return cls.find_by_id(row[0]) if row else None
