'''Functions Code'''
from flask import flash

def input_validation_check(name, order, session):
    """
    Validating orders input, to ensure name, 
    order and session are input and within correct parameters
    """
    try:
        ret = False
        values = {
            "Name": name,
            "Order": order,
            "Session": session
        }
        for key, value in values.items():
            if not value:
                flash(f'{key} is required!', 'danger')
                ret = True
        if len(session) != 5 or session.isdigit() is False:
            flash('Session ID is must be 5 digits!', 'danger')
            ret = True
        return ret
    except Exception as error: # pylint: disable=broad-except
        print(error)
        return error
