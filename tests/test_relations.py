
import os
import pytest
from lib.database_utils import create_tables, get_connection
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

DB_FILE = "magazine.db"


@pytest.fixture(autouse=True)
def setup_database():
    """Recreate database before each test."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    create_tables()
    yield
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)


def test_author_creation_and_save():
    author = Author("Ann Gathoni")
    author.save()
    assert author.id is not None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM authors WHERE id=?", (author.id,))
    result = cur.fetchone()
    conn.close()

    assert result[0] == "Ann Gathoni"


def test_magazine_creation_and_save():
    mag = Magazine("Tech Times", "Technology")
    mag.save()
    assert mag.id is not None

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, category FROM magazines WHERE id=?", (mag.id,))
    result = cur.fetchone()
    conn.close()

    assert result == ("Tech Times", "Technology")


def test_article_creation_and_relationships():
    author = Author("Ann Gathoni")
    author.save()
    mag = Magazine("Tech Times", "Technology")
    mag.save()

    article = author.add_article(mag, "The Rise of AI Automation")

    # Test saved
    assert article.id is not None
    assert article.author.id == author.id
    assert article.magazine.id == mag.id

    # Verify article in database
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT title FROM articles WHERE id=?", (article.id,))
    result = cur.fetchone()
    conn.close()
    assert result[0] == "The Rise of AI Automation"


def test_author_magazines_and_articles_methods():
    author = Author("Ann Gathoni")
    author.save()
    mag = Magazine("Tech Times", "Technology")
    mag.save()

    a1 = author.add_article(mag, "AI Revolution")
    a2 = author.add_article(mag, "Quantum Future")

    mags = author.magazines()
    arts = author.articles()

    assert len(mags) == 1
    assert mags[0].name == "Tech Times"
    assert len(arts) == 2
    assert {a.title for a in arts} == {"AI Revolution", "Quantum Future"}


def test_magazine_contributors_and_article_titles():
    author1 = Author("Ann Gathoni")
    author1.save()
    author2 = Author("John Doe")
    author2.save()

    mag = Magazine("Tech Times", "Technology")
    mag.save()

    author1.add_article(mag, "AI Revolution")
    author2.add_article(mag, "Cybersecurity Future")

    contributors = mag.contributors()
    titles = mag.article_titles()

    assert len(contributors) == 2
    assert "AI Revolution" in titles
    assert "Cybersecurity Future" in titles


def test_contributing_authors_more_than_two_articles():
    author = Author("Ann Gathoni")
    author.save()
    mag = Magazine("Tech Times", "Technology")
    mag.save()

    # 3 articles by the same author
    author.add_article(mag, "AI 1")
    author.add_article(mag, "AI 2")
    author.add_article(mag, "AI 3")

    top_contributors = mag.contributing_authors()
    assert len(top_contributors) == 1
    assert top_contributors[0].name == "Ann Gathoni"


def test_top_publisher():
    author = Author("Ann Gathoni")
    author.save()

    mag1 = Magazine("Tech Times", "Technology")
    mag1.save()
    mag2 = Magazine("Health Weekly", "Health")
    mag2.save()

    # Add articles
    author.add_article(mag1, "AI in Healthcare")
    author.add_article(mag1, "Automation Future")
    author.add_article(mag2, "Mental Health Awareness")

    # Tech Times has 2 articles, should be top publisher
    top = Magazine.top_publisher()
    assert top.name == "Tech Times"
