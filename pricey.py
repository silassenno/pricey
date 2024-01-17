from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import expense

app = Flask("pricey")
app.engine = create_engine("sqlite:///pricey.db", echo=True)
expense.Base.metadata.create_all(app.engine)

# months of current year with start day and end day
months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]

current_year = datetime.now().year
years = [year for year in range(current_year - 5, current_year + 2)]


@app.route("/expense/add", methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        with Session(app.engine) as session:
            category_id = request.form['category']
            category = session.query(expense.Category).filter_by(id=category_id).one_or_none()

            if category is not None:
                new_expense = expense.Expense(
                    amount=request.form['amount'],
                    category=category,  # Assign the category object
                    date=datetime.strptime(request.form['date'], "%Y-%m-%d")
                )
                session.add(new_expense)
                session.commit()
                return redirect(url_for('home'))
    with Session(app.engine) as session:
        categories = session.query(expense.Category).all()
        # Render the form for a new expense
        return render_template('expense_form.html', expense=None, default_date=datetime.now().strftime('%Y-%m-%d'),
                               categories=categories)


@app.route("/expense/edit/<int:expense_id>", methods=['GET', 'POST'])
def edit(expense_id):
    with Session(app.engine) as session:
        expense_to_edit = session.query(expense.Expense).filter_by(id=expense_id).one_or_none()

        if request.method == 'POST' and expense_to_edit is not None:
            category_id = request.form['category']
            category = session.query(expense.Category).filter_by(id=category_id).one_or_none()

            if category is not None:
                expense_to_edit.amount = request.form['amount']
                expense_to_edit.category = category  # Assign the category object
                expense_to_edit.date = datetime.strptime(request.form['date'], "%Y-%m-%d")
                session.commit()
                return redirect(url_for('home'))

        categories = session.query(expense.Category).all()  # Fetch categories within the same session
        # Render the form with the expense to be edited
        return render_template('expense_form.html', expense=expense_to_edit, default_date=None, categories=categories)


@app.route("/expense/delete/<int:expense_id>")
def delete(expense_id):
    with Session(app.engine) as session:
        expense_to_delete = session.query(expense.Expense).filter_by(id=expense_id).one()
        session.delete(expense_to_delete)
        session.commit()
    return redirect(url_for('home'))


@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    # Implement the logic to add a new category
    if request.method == 'POST':
        with Session(app.engine) as session:
            new_category = expense.Category(
                name=request.form['name'],
                emoji=request.form['emoji'],
                goal=request.form['goal']
            )
            session.add(new_category)
            session.commit()
            return redirect(url_for('home'))
    return render_template('category_form.html', category=None)


@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    with Session(app.engine) as session:
        category_to_edit = session.query(expense.Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        with Session(app.engine) as session:
            category_to_edit.name = request.form['name']
            category_to_edit.emoji = request.form['emoji']
            category_to_edit.goal = request.form['goal']
            session.commit()
            return redirect(url_for('home'))
    return render_template('category_form.html', category=category_to_edit)


@app.route('/category/delete/<int:category_id>')
def delete_category(category_id):
    with Session(app.engine) as session:
        category_to_delete = session.query(expense.Category).filter_by(id=category_id).one()
        session.delete(category_to_delete)
        session.commit()
    return redirect(url_for('home'))


@app.route('/')
def home():
    # if no month is selected, display current month
    if request.args.get('month'):
        current_month = request.args.get('month')
    else:
        current_month = months[datetime.now().month]
    if request.args.get('year'):
        current_year = int(request.args.get('year'))
    else:
        current_year = datetime.now().year
    with Session(app.engine) as session:
        expenses = session.query(expense.Expense).all()
        categories = session.query(expense.Category).all()
        return render_template('index.html', expenses=expenses, categories=categories, months=months,
                               selected_month=current_month, selected_year=current_year, years=years)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
