from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = NONE
    try:
        conn = sqilte3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 


@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not NONE:
            return jsonify(books)
        
    if request.method == 'POST':
        new_author = requst.form['author']
        new_lang = requst.form['language']
        new_title = requst.form['title']
        sql = """INSERT INTO book (author, language, title) VALUES(?, ?, ?)"""
        cursor = cur.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201

    books_list.append(new_obj)
    return jsonify(books_list), 201

@app.route('/book/<int:id>', method=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in book_list:
            if book['id'] == id:
                return jsonify(book)
            pass
    if request.method == 'PUT':
        for book in book_list:
            if book['id'] == id:
                book['author'] = request.form('author')
                book['language'] = request.form('language')
                book['title'] = request.form('title')

                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                return jsonify(updated_book)
    if request.method == 'DELETE':
       for index, book in enumerate(books_list):
           if book['id'] == id:
               books_list.pop(index)
               return jsonify(books_list)

if __name__ == '__main__':
    app.run(debug=True)

