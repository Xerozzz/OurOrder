from flask import Flask, url_for, render_template, flash, redirect, request, jsonify, make_response, send_file

# For validating order inputs


def input_validation_check(name, order, session):
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
    if len(session) != 5:
        flash('Session ID is must be 5 digits!', 'danger')
        ret = True
    return ret
