from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

BOOK_SERVICE_URL = "http://book_service:5001/books"
ORDER_SERVICE_URL = "http://order_service:5002/orders"

@app.route('/', methods=['GET', 'POST'])
def index():
    books = requests.get(BOOK_SERVICE_URL).json()
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        book = next((b for b in books if str(b['id']) == book_id), None)
        if book:
            requests.post(ORDER_SERVICE_URL, json={"book_id": book['id'], "title": book['title']})
        return redirect('/')
    orders = requests.get(ORDER_SERVICE_URL).json()
    return render_template('index.html', books=books, orders=orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
