# Import dependencies
from flask import Flask, url_for, render_template, flash, redirect, request, jsonify, make_response, send_file
from flask_caching import Cache
import os, io
import pandas as pd

# App configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SET A KEY'
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1800
}
app.config.from_mapping(config)
cache = Cache(app)

# Setting Constants
CACHE_TIMEOUT = 1800

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtain form results
        name = request.form['name']
        order = request.form['order']
        session = request.form['session']
        price = request.form['price']
        notes = request.form['notes']

        # Validate form results
        if not name:
            flash('Name is required!')
        if not order:
            flash('Order is required!')
        if not session or len(session) != 5 :
            flash('Session ID is required and must be 5 digits!')
        else:
            try:
                session = int(session)
                # Store order in cache and update
                item = cache.get(session)
                if item == None:
                    item = {name: [order, notes, price]}
                else:
                    item[name] = [order, notes, price]
                try:
                    cache.set(session, item, timeout=CACHE_TIMEOUT)
                    flash("Order added successfully!")
                    return redirect(url_for('index'))
                except Exception as e:
                    flash(f'Error adding order: {str(e)}')
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
            total = 0
            if orders == None:
                orders = 'N'
            else:
                for key, value in orders.items():
                    total += float(value[2])
            return render_template('orders.html', orders=orders, total = total)
        except:
            flash('Session ID must be digits!')
    return render_template('orders.html')

@app.route('/export', methods=['POST'])
def export():
    try:
        data = request.get_json().get('session')

        # Create dataframe from data
        df = pd.DataFrame.from_dict(data, orient='index', columns=['Order', 'Notes', 'Price'])

        # Convert the DataFrame to an Excel file in memory
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name="exportdata", index = True, header=True)
        writer.save()
        output.seek(0)

        # Create a Flask response with the Excel file
        response = send_file(output, as_attachment=True, mimetype='application/vnd.ms-excel', download_name="export.xlsx")
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        return response
    except Exception as e:
        flash(f"Error exporting data: {str(e)}")

@app.route('/generate', methods=['GET'])
def generate():
    item = {
        "YT": ["Potato Salad", "With extra cream", "3.00"],
        "Keith": ["Potato Soup", "With extra eggs", "10.00"],      
        "John": ["Ribeye Steak", "With extra sauce", "12.00"],  
        "Alex": ["Mcchicken meal with potato pie", "Upsize, drink coke no ice", "20.00"],  
    }
    cache.set(11111, item, timeout=CACHE_TIMEOUT)
    print("Test Data Generated!")
    return redirect(url_for('orders'))