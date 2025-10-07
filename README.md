# Object Relations Code Challenge - Articles
This project is a full implementation of the **Object Relations Code Challenge** using Python classes and raw SQL with **SQLite3**.  
It models a magazine publishing system with three core entities:

- **Author** – Represents a writer who creates articles.  
- **Magazine** – Represents a publication with a name and category.  
- **Article** – Represents a written piece, linked to both an author and a magazine.

All objects interact with a relational SQLite database (`magazine.db`) using direct SQL commands 

# Features Implemented

 Full CRUD operations for all classes  
 Validations for all properties (non-empty strings, correct types, etc.)  
 Relationships:
- `Author → Articles`
- `Author → Magazines` (via Articles)
- `Magazine → Articles`
- `Magazine → Contributors (Authors)`
 Aggregate methods:
- `Author.topic_areas()`
- `Magazine.article_titles()`
- `Magazine.contributing_authors()`
- `Magazine.top_publisher()`
 Automatic SQLite table creation with foreign key constraints

Project Structure

python-magazine-sql-challenge/
├── lib/
│   ├── __init__.py
│   ├── author.py
│   ├── magazine.py
│   ├── article.py
│   └── database_utils.py
├── tests/
│   ├── __init__.py
│   └── test_relations.py
├── debug.py
├── requirements.txt
└── README.md

