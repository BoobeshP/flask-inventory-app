from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

# Products
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        pid = request.form['product_id'].strip()
        name = request.form['name'].strip()
        if not pid or not name:
            flash('Both fields are required', 'danger')
        else:
            p = Product(product_id=pid, name=name)
            db.session.add(p)
            try:
                db.session.commit()
                flash('Product added', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error: ' + str(e), 'danger')
        return redirect(url_for('products'))
    return render_template('products.html', products=Product.query.all())

# Locations
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        lid = request.form['location_id'].strip()
        name = request.form['name'].strip()
        if not lid or not name:
            flash('Both fields are required', 'danger')
        else:
            l = Location(location_id=lid, name=name)
            db.session.add(l)
            try:
                db.session.commit()
                flash('Location added', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error: ' + str(e), 'danger')
        return redirect(url_for('locations'))
    return render_template('locations.html', locations=Location.query.all())

# Movements
@app.route('/movements', methods=['GET', 'POST'])
def movements():
    products = Product.query.all()
    locations = Location.query.all()
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form['qty'] or 0)
        if qty <= 0:
            flash('Quantity must be positive', 'danger')
        elif not product_id:
            flash('Product is required', 'danger')
        elif not (from_location or to_location):
            flash('Either from or to location must be provided', 'danger')
        else:
            m = ProductMovement(
                product_id=product_id,
                from_location=from_location,
                to_location=to_location,
                qty=qty
            )
            db.session.add(m)
            db.session.commit()
            flash('Movement recorded', 'success')
        return redirect(url_for('movements'))
    return render_template('movements.html', movements=ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all(), products=products, locations=locations)

# Report: balance per product per location
@app.route('/report')
def report():
    # Build a balance dict {(product_id, location_id): qty}
    balances = {}
    products = Product.query.all()
    locations = Location.query.all()
    for p in products:
        for l in locations:
            balances[(p.product_id, l.location_id)] = 0
    movements = ProductMovement.query.all()
    for m in movements:
        if m.to_location:
            balances[(m.product_id, m.to_location)] = balances.get((m.product_id, m.to_location), 0) + m.qty
        if m.from_location:
            balances[(m.product_id, m.from_location)] = balances.get((m.product_id, m.from_location), 0) - m.qty
    rows = []
    for (pid, lid), qty in balances.items():
        rows.append({
            'product_id': pid,
            'product_name': Product.query.get(pid).name if Product.query.get(pid) else pid,
            'location_id': lid,
            'location_name': Location.query.get(lid).name if Location.query.get(lid) else lid,
            'qty': qty
        })
    return render_template('report.html', rows=rows)

# Simple seed route (for quick local testing) - SAFE to remove before submission if desired.
@app.route('/seed')
def seed():
    # only seed if empty
    if Product.query.first():
        flash('Already seeded', 'info')
        return redirect(url_for('home'))
    p1 = Product(product_id='P1', name='Product A')
    p2 = Product(product_id='P2', name='Product B')
    p3 = Product(product_id='P3', name='Product C')
    l1 = Location(location_id='L1', name='Warehouse X')
    l2 = Location(location_id='L2', name='Warehouse Y')
    l3 = Location(location_id='L3', name='Warehouse Z')
    db.session.add_all([p1,p2,p3,l1,l2,l3])
    db.session.commit()
    # sample movements
    from random import randint
    movements = [
        ProductMovement(product_id='P1', to_location='L1', qty=45),
        ProductMovement(product_id='P2', to_location='L1', qty=25),
        ProductMovement(product_id='P1', from_location='L1', to_location='L2', qty=10),
        ProductMovement(product_id='P3', to_location='L3', qty=15),
    ]
    db.session.add_all(movements)
    db.session.commit()
    flash('Seeded database with sample data', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Allow a quick init command: python app.py initdb
    if len(sys.argv) > 1 and sys.argv[1] == 'initdb':
        with app.app_context():
            db.create_all()
            print('Created a database inventory.db in the current folder.')
        sys.exit(0)
    app.run(host='0.0.0.0', port=5000, debug=True)
