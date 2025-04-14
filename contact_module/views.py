from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import ContactUsForm
from .models import ContactUS
from extensions import db
from site_module.models import SiteSetting

contact_views = Blueprint('contact_views', __name__, template_folder='templates')


@contact_views.route('/', methods=['GET', 'POST'])
def contact_view():
    form = ContactUsForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        message = form.message.data
        subject = form.title.data
        newContact = ContactUS(full_name=full_name, email=email, message=message, title=subject)
        db.session.add(newContact)
        db.session.commit()
        flash("your Message has been sent successfully!", "success")
        return redirect(url_for('contact_views.contact_view'))
    site_setting = SiteSetting.query.filter_by(is_main_setting=True).first()
    return render_template('contact_module/contact_us_page.html', form=form, site_setting=site_setting)
