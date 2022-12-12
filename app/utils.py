from flask import request, render_template, flash, current_app
from flask_mail import Message
import requests


def paginate(query):
    page = request.args.get('page', type=int) or 1
    return query.paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    

def upload_file(file):
    url = 'https://api.cloudinary.com/v1_1/dq8nv0pj6/upload'
    UPLOAD_PRESET = 'tsyyldp2'
    r = requests.post(url, files={'file': file.read()}, data={
                      'upload_preset': UPLOAD_PRESET})
    print(r, r.content)
    try:
        return r.json().get('secure_url')
    except:
        flash("Could not upload file successfully please try again later",
              category='error')
        return ""


def order_column(column):
    if request.args.get('order') == 'ascending':
        return column
    return column.desc()


    