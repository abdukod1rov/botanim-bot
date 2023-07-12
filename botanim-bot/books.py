from dataclasses import dataclass
from datetime import datetime
import config

import aiosqlite


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@dataclass
class Book:
    id: int
    name: str
    category_name: str
    read_start: datetime
    read_end: datetime


@dataclass
class Category:
    id: int
    books: list[Book]


async def get_all_books(chunk_size: int) -> list[Category]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
        SELECT 
    b.id as book_id,
        b.name as book_name,
        c.id as category_id,
        c.name as category_name,
        b.read_start, b.read_end
    FROM book as b
    LEFT JOIN book_category c on c.id=b.category_id
    ORDER BY c."ordering", b."ordering"  
        """) as cursor:
            async for row in cursor:
                books.append(
                    Book(
                        id=row['book_id'],
                        name=row['book_name'],
                        category_name=row['category_name'],
                        read_start=row['read_start'],
                        read_end=row['read_end']

                    ))
    return _chunks(books, chunk_size)
