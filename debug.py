# debug.py
from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
import os

DB_FILE = "magazine.db"

# Optional: Start fresh each run (delete DB file)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

def main():
    # Setup database tables
    create_tables()

    # Create author and magazine
    author = Author("Ann Gathoni")
    author.save()

    mag = Magazine("Tech Times", "Technology")
    mag.save()

    # Create and save an article
    article = author.add_article(mag, "The Rise of AI Automation")

    print("=== Article Info ===")
    print(f"Title: {article.title}")
    print(f"Author: {article.author.name}")
    print(f"Magazine: {article.magazine.name}\n")

    print("=== Magazines by Author ===")
    for m in author.magazines():
        print(f"- {m.name} ({m.category})")

    print("\n=== Articles in Magazine ===")
    for a in mag.articles():
        print(f"- {a.title}")

if __name__ == "__main__":
    main()
