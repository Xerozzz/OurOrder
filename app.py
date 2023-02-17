from flask import Flask, render_template, flash, redirect, request, jsonify, make_response, send_file
import os
import io
from flask_caching import Cache
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SET A KEY'
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1800
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
        price = request.form['price']
        notes = request.form['notes']

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
                    item = {name: [order, notes, price]}
                else:
                    item[name] = [order, notes, price]
                cache.set(session, item, timeout=1800)
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
    response = send_file(output, as_attachment=True, mimetype='application/vnd.ms-excel', download_name="exportdata.xlsx")
    response.headers['Content-Disposition'] = 'attachment; filename=export.xlsx'
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    return response