'''Main Application Code'''
# Import dependencies
import os
import io
from flask import Flask, url_for, render_template, flash, redirect, request, send_file
from flask_caching import Cache
import pandas as pd
import functions

# App configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SET A KEY'
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "flask_caching.backends.RedisCache",  # Selecting REDIS as server
    "CACHE_KEY_PREFIX": "ourorder",
    "CACHE_REDIS_URL": os.environ.get("REDIS_URL")
}
app.config.from_mapping(config)
cache = Cache(app)

# Setting Constants
CACHE_TIMEOUT = 1800

# Index Route


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    INDEX Route. Allows GET requests and POST request to submit orders
    '''
    if request.method == 'POST':
        # Obtain form results
        name = request.form['name']
        order = request.form['order']
        session = request.form['session']
        price = request.form['price']
        notes = request.form['notes']

        # Validate form results
        if functions.input_validation_check(name, order, session):
            render_template('index.html')
        else:
            try:
                # Store order in cache and update
                item = cache.get(session)
                if item is None:
                    item = {name: [order, notes, price]}
                else:
                    item[name] = [order, notes, price]  # pragma: no cover
                try:
                    cache.set(session, item, timeout=CACHE_TIMEOUT)
                    flash("Order added successfully!", 'success')
                    return redirect(url_for('index'))
                except Exception as error:  # pylint: disable=broad-except # pragma: no cover
                    flash(f'Error adding order: {str(error)}', 'danger')
            except Exception:  # pylint: disable=broad-except # pragma: no cover
                flash('Session ID must be digits!', 'danger')
    return render_template('index.html')

# Orders Route


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    '''
    ORDERS Route. Allows GET requests and POST request to check orders and export to excel
    '''
    if request.method == 'POST':
        # Obtain results from form
        session = request.form['session']

        # Validate results
        if not session or len(session) != 5:
            flash('Session ID is required and must be 5 digits!', 'danger')
            return render_template('orders.html', orders=None, total=0)
        try:
            order = cache.get(session)
            total = 0
            if order is None:
                order = 'N'
            else:
                try:
                    for value in order.values():
                        total += float(value[2])
                except Exception: # pylint: disable=broad-except
                    flash(
                        'No total price due to invalid or None price input! (This is not an error)',
                        'danger')
            return render_template('orders.html', order=order, total=total)
        except Exception:  # pylint: disable=broad-except # pragma: no cover
            flash('Session ID must be digits!')
    return render_template('orders.html')


# Export Route
@app.route('/export', methods=['POST'])
def export():
    '''
    EXPORT Route. Allows POST request only to generate orders in excel format
    '''
    try:
        data = request.get_json().get('orders')
        # Create dataframe from data
        data_frame = pd.DataFrame.from_dict(
            data, orient='index', columns=[
                'Order', 'Notes', 'Price'])

        # Convert the DataFrame to an Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer: # pylint: disable=abstract-class-instantiated
            data_frame.to_excel(
                writer,
                sheet_name="exportdata",
                index=True,
                header=True)
        output.seek(0)

        # Create a Flask response with the Excel file
        response = send_file(
            output,
            as_attachment=True,
            mimetype='application/vnd.ms-excel',
            download_name="export.xlsx")
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        return response
    except Exception as error:  # pylint: disable=broad-except # pragma: no cover
        return f"Error exporting data: {str(error)}"

# Generate Route


@app.route('/generate', methods=['GET'])
def generate():
    '''
    GENERATE Route. Allows GET requests only, temp route to generate test data
    '''
    item = {
        "YT": ["Potato Salad", "With extra cream", "3.00"],
        "Keith": ["Potato Soup", "With extra eggs", "10.00"],
        "John": ["Ribeye Steak", "With extra sauce", "12.00"],
        "Alex": ["Mcchicken meal with potato pie", "Upsize, drink coke no ice", "20.00"],
    }
    cache.set("11111", item, timeout=CACHE_TIMEOUT)
    print("Test Data Generated!")
    return redirect(url_for('orders'))


if __name__ == '__main__':
    app.run()
