import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/donate/', methods=['GET', 'POST'])
def donate():
    # Retrieve the donor name and donation amt from submitted form if request method is POST
    if request.method == 'POST':
        name = request.form['name']
        donation = request.form['donation']
        # Retrieve the donor from the database
        find_donor = Donation.select(Donation.donor).join(Donor).where(Donor.name == name)
        # Create new donation with indicated donor and amount
        if find_donor:
            new = Donation.create(donor=find_donor, value=donation)
            new.save()
            return redirect(url_for('home'))
        else:
            return render_template(
                'newdonation.jinja2', error="Add a donation for an existing donor."
            )
    # Render the template for the donation creation page if request method is GET
    return render_template('newdonation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

