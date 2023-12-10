from flask import Blueprint,render_template, url_for, request, flash, session, redirect
from flask_login import login_required, current_user
from . import dbase
from .dbmodels import Products, BucketListItem, Interest
from flask import jsonify

# Initialising the name for this file which is 'userview'
# This file shows what user can see and do
views = Blueprint('userview', __name__)


# Route to home page
@views.route('/')
@login_required               # Log In is required to access this page
def homepage():
    name = current_user.name
    products = Products.query.all()
    return render_template('index.html', user=current_user, name=name, products=products)


# Route to Add to Bucket List with product id initialised at the back
@views.route('/add_to_bucket_list/<int:product_id>')
@login_required
def add_to_bucket_list(product_id):
    product = Products.query.get(product_id)

# Handles if product is 0 and if product is already added into the bucket list
    if product:
        if product.owner == current_user:
            flash("You cannot add your own item into the Bucket List", category='error')

        elif product.stocklvl <= 0:
            flash(f"{product.product_name} is out of stock", category='error')

        else:
            bucket_list_item = BucketListItem(product=product, user=current_user)
            dbase.session.add(bucket_list_item)
            dbase.session.commit()
            flash("Item successfully added into Bucket List", category='success')

    else:
        flash("Product not found", category='error')

    return redirect(url_for('userview.homepage'))


# Route to Account Page
@views.route('/user')
@login_required
def user():
    return render_template('user.html')


# Route to Bucket List Page
@views.route('/bucketlist')
@login_required
def bucketList():
    return render_template('bucketlist.html')


# Route to My Product Page
@views.route('/myproduct')
@login_required
def myproduct():
    user_products = current_user.products
    return render_template('myproduct.html', user_products=user_products)


# Route to Update Stock Level with product id initialised at the back
@views.route('/updatestcklvl/<int:product_id>', methods=['GET', 'POST'])
@login_required
def updatestcklvl(product_id):
    product = Products.query.get(product_id)

    if product:
        if request.method == 'POST':
            updatestck = int(request.form.get('updatestck',0))
            product.stocklvl += updatestck
            dbase.session.commit()

            flash(f"Stock level for {product.product_name} updated by {updatestck}. New Stock Level: {product.stocklvl}",
                  category="success")

            return redirect(url_for('userview.myproduct'))

        return render_template('updatestcklvl.html', product=product)

    else:
        flash("Product not found", category="error")
        return redirect(url_for("userview.homepage"))


# Route to Add User Product
@views.route('/adduserproduct', methods=['GET','POST'])
@login_required
def adduserproduct():
    if request.method == "POST":
        product_name = request.form.get('product_name')
        product_category = request.form.get('product_category')
        product_price = request.form.get('product_price')

        new_product = Products(product_name=product_name, product_category=product_category, product_price=product_price,
                               owner=current_user)

        dbase.session.add(new_product)
        dbase.session.commit()

        flash("Your Product is now available in UMarket!", category='success')

        return redirect(url_for('userview.myproduct'))

    return render_template('adduserproduct.html')


# Route to Delete User Product
@views.route('/deleteproduct/<int:product_id>', methods=["POST"])
@login_required
def deleteproduct(product_id):
    product = Products.query.get(product_id)

# User can only delete their own products
    if product:
        if product.owner == current_user:
            dbase.session.delete(product)
            dbase.session.commit()

            flash(f"Product '{product.product_name}' has been deleted", category='success')

        else:
            flash("You can only delete your own products", category='error')

    else:
        flash("Product not found", category='error')

    return redirect(url_for('userview.myproduct'))


# Route to User's Likes
@views.route('/interests')
@login_required
def interests():
    user_interests = Interest.query.filter_by(user_id=current_user.id).all()
    products = [interest.product for interest in user_interests]
    return render_template('interests.html', user=current_user, products=products)


# Route to User's liked products
@views.route('/like_product/<int:product_id>', methods=["POST"])
@login_required
def like_product(product_id):
    product = Products.query.get(product_id)

# Checks if user has liked the product
    if product:
        existing_interest = Interest.query.filter_by(user=current_user, product=product).first()

        if existing_interest:
            dbase.session.delete(existing_interest)
            dbase.session.commit()
            session[f'liked_product_{product_id}']=False
            return jsonify({'message': 'Product unliked successfully'})

        new_interest = Interest(product=product, user=current_user)
        dbase.session.add(new_interest)
        dbase.session.commit()
        session[f'liked_product_{product_id}'] = True
        return jsonify({'message': 'Product liked successfully'})

    return jsonify({'error': 'Product not found'}), 404
