from flask import Flask, request, jsonify

app = Flask(__name__)

books_list = []

@app.route('/books', methods=['GET', 'POST'])
def books():
    if requst.method == 'GET':
        if len(books.list) > 0:
            return jsonify(books_list)
        else:
            Nothing found, 404

    if requst.method == 'POST':
        new_author = requst.from['author']
        new_lang = requst.from['language']
        new_title = requst.from['title']
        iD = books_list[-1]['id']+1

        new_obj = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title
    }
    books_list.append(new_obj)
    return jsonify(books_list), 201

if __name__ == '__main__':
    app.run()

