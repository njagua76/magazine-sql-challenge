
from .database_utils import get_connection

class Article:
    def __init__(self, title, author, magazine):
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Article title must be a non-empty string.")
        self.title = title.strip()
        self.author = author  # Author instance
        self.magazine = magazine  # Magazine instance
        self.id = None

    @classmethod
    def new_from_db(cls, row):
        from .author import Author
        from .magazine import Magazine

        article = cls(row[1], Author.find_by_id(row[2]), Magazine.find_by_id(row[3]))
        article.id = row[0]
        return article

    def save(self):
        """Insert or update the article in the DB."""
        conn = get_connection()
        cur = conn.cursor()

        if self.id is None:
            cur.execute("""
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES (?, ?, ?)
            """, (self.title, self.author.id, self.magazine.id))
            self.id = cur.lastrowid
        else:
            cur.execute("""
                UPDATE articles
                SET title=?, author_id=?, magazine_id=?
                WHERE id=?
            """, (self.title, self.author.id, self.magazine.id, self.id))

        conn.commit()
        conn.close()
