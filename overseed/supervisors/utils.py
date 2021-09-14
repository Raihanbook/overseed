import os
import secrets
from PIL import Image
from flask import current_app


# This function takes a picture that has been uploaded by a WTForm, and saves
# it to the static/company_icons folder.
# ---------------
# Returns the filename of the saved picture.
# ---------------
# From Corey MSchafer's youtube tutorial series.
# https://www.youtube.com/watch?v=803Ei2Sq-Zs
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    # discard the filename, keep the extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # Use a random code
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/company_icons', picture_fn)
    
    i = Image.open(form_picture)
    i.save(picture_path)
        
    return picture_fn