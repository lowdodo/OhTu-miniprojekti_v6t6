from sqlalchemy import text
from config import db
from entities.article import Article
from entities.book import Book



def get_all_references():
    articles_res = db.session.execute(
        text(
            "SELECT r.id, STRING_AGG(a.author, ' & ') AS authors, r.title, r.journal, r.year, r.volume, \
            r.number, r.pages, r.month, r.note FROM referencetable r INNER JOIN authors a ON r.id = a.reference_id WHERE r.reftype = 'article' GROUP BY r.id"
        )
    )
    articles = articles_res.fetchall()

    books_res = db.session.execute(
        text(
            "SELECT r.id, STRING_AGG(a.author, ' & ') AS authors, r.editor, r.title, r.publisher, r.year, \
            r.volume, r.number, r.pages, r.month, r.note FROM referencetable r INNER JOIN authors a ON r.id = a.reference_id WHERE r.reftype = 'book' GROUP BY r.id"
        )
    )
    books = books_res.fetchall()

    return [Article(*row) for row in articles] + [Book(*row) for row in books]



def get_reference_by_id(ref_id, type):
    result = db.session.execute(
        text("SELECT * FROM referencetable WHERE id = :id"), {"id": ref_id}
    )
    contents = result.fetchall()
    columns = result.keys()
    reference = [dict(zip(columns, row)) for row in contents][0]
    reference["type"] = type
    return reference



def get_authors_by_reference_id(ref_id):
    result = db.session.execute(
        text("SELECT author FROM authors WHERE reference_id = :id"),
        {"id": ref_id},
    )
    contents = result.fetchall()
    return [row[0] for row in contents]



def delete_reference_db(ref_id):
    db.session.execute(
        text("DELETE FROM authors WHERE reference_id = :id"),
        {"id": ref_id},
    )
    db.session.execute(
        text("DELETE FROM referencetable WHERE id = :id"),
        {"id": ref_id},
    )
    db.session.commit()


def create_reference(reference):
    field_contents = {
        "article": ["title", "journal", "year", "volume", "number", "pages", "month", "note"],
        "book": ["editor", "title", "publisher", "year", "volume", "number", "pages", "month", "note"],
    }

    fields = field_contents.get(reference.type)

    if not fields:
        raise ValueError(f"Invalid reference type: {reference.type}")
    
    field_places = ", ".join(f":{field}" for field in fields)
    field_names = ", ".join(fields)

    sql = text(
        "INSERT INTO referencetable (" +field_names+ ", reftype) "
        "VALUES (" +field_places+ ", :reftype) RETURNING id"
    )

    parameters = {field: getattr(reference, field, None) for field in fields}
    parameters["reftype"] = reference.type

    result = db.session.execute(sql, parameters)

    db.session.commit()

    row_id = result.fetchone()[0]

    for author in reference.authors:
        create_author(author, row_id)



def edit_reference(reference):
    # assuming our future tables will be named like this
    fields = [
        attr
        for attr in reference.__dict__.keys()
        if attr not in ["id", "type", "authors"]
    ]

    set_clause = ", ".join([f"{field} = :{field}" for field in fields])
    update_reference_sql = text(
        f"UPDATE referencetable SET {set_clause} WHERE id = :reference_id"
    )

    params = {field: getattr(reference, field) for field in fields}
    params["reference_id"] = reference.id

    db.session.execute(update_reference_sql, params)

    remove_previous_authors_sql = text(
        "DELETE FROM authors WHERE reference_id = :reference_id"
    )
    db.session.execute(
        remove_previous_authors_sql,
        {"reference_id": reference.id},
    )

    for author in reference.authors:
        create_author(author, reference.id)

    db.session.commit()




def create_author(author, reference_id):
    sql = text(
        "INSERT INTO authors (author, reference_id) VALUES (:author, :reference_id)"
    )
    db.session.execute(sql, {"author": author, "reference_id": reference_id})
    db.session.commit()




def generate_bibkey(reference):
    author = "".join([name.split()[-1][:4] for name in reference.authors.split(" & ")])
    title = reference.title[:3]
    year = reference.year
    return f"{author}{title}{year}"




def join_bibtex():
    references = get_all_references()
    bibtex_entries = []
    for reference in references:
        bibtex_str = f"@{reference.__class__.__name__.lower()}{{{str(generate_bibkey(reference))},\n"
        for key, value in reference.__dict__.items():
            if key not in ["id", "type"] and value:
                bibtex_str += f"  {key} = {{{str(value)}}},\n"
        bibtex_str += "}\n"
        bibtex_entries.append(bibtex_str)
    return "\n".join(bibtex_entries)


































