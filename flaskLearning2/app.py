from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='sql7.freesqldatabase.com',
            database='sql7764026',
            user='sql7764026',
            password='tyFaTnW8tz',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
    return conn


@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    if conn is None:
        return "Failed to connect to the database.", 500
    
    cursor = conn.cursor()

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM book")
            books = [
                dict(id=row['id'], author=row['author'], language=row['language'], title=row['title'])
                for row in cursor.fetchall()
            ]
            if books:
                return jsonify(books), 200
            else:
                return "No books found.", 404
        except pymysql.MySQLError as e:
            return f"Error fetching books: {e}", 500

    if request.method == 'POST':
        try:
            new_author = request.form['author']
            new_lang = request.form['language']
            new_title = request.form['title']
            sql = """INSERT INTO book (author, language, title) VALUES (%s, %s, %s)"""
            cursor.execute(sql, (new_author, new_lang, new_title))
            conn.commit()
            return f"Book with the id: {cursor.lastrowid} created successfully", 201
        except pymysql.MySQLError as e:
            return f"Error inserting book: {e}", 500


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    if conn is None:
        return "Failed to connect to the database.", 500

    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM book WHERE id=%s", (id,))
            book = cursor.fetchone()
            if book:
                return jsonify(book), 200
            else:
                return "Book not found.", 404
        except pymysql.MySQLError as e:
            return f"Error fetching book: {e}", 500

    if request.method == 'PUT':
        try:
            author = request.form['author']
            language = request.form['language']
            title = request.form['title']
            sql = """UPDATE book
                    SET author=%s, language=%s, title=%s
                    WHERE id=%s"""
            cursor.execute(sql, (author, language, title, id))
            conn.commit()
            return jsonify({"id": id, "author": author, "language": language, "title": title}), 200
        except pymysql.MySQLError as e:
            return f"Error updating book: {e}", 500

    if request.method == 'DELETE':
        try:
            sql = """DELETE FROM book WHERE id=%s"""
            cursor.execute(sql, (id,))
            conn.commit()
            if cursor.rowcount > 0:
                return f"The book with id: {id} has been deleted.", 200
            else:
                return "Book not found.", 404
        except pymysql.MySQLError as e:
            return f"Error deleting book: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
