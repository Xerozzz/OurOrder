from flask import Flask, render_template, flash, redirect, request
import os
from flask_caching import Cache


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SET A KEY'
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 900
}
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtain form results
        name = request.form['name']
        order = request.form['order']
        session = request.form['session']

        # Validate form results
        if not name:
            flash('Name is required!')
        elif not order:
            flash('Order is required!')
        elif not session or len(session) != 5 :
            flash('Session ID is required and must be 5 digits!')
        else:
            try:
                session = int(session)
                # Store order in cache and update
                item = cache.get(session)
                if item == None:
                    item = {name: order}
                    print(session,item)
                    cache.set(session, item)
                else:
                    item[name] = order
                    cache.set(session, item)
                flash("Order added successfully!")
                return redirect(url_for('index'))
            except:
                flash('Session ID must be digits!')            
    return render_template('index.html')

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        # Obtain results from form
        session = request.form['session']

        # Validate results
        if not session or len(session) != 5 :
            flash('Session ID is required and must be 5 digits!')
        try:
            session = int(session)
            orders = cache.get(session)
            print(orders)
            return render_template('orders.html', orders=orders)
        except:
            flash('Session ID must be digits!')
    return render_template('orders.html')