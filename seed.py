import random
from datetime import datetime, timedelta

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from expense import Base, Expense, Category

engine = create_engine("sqlite:///pricey.db")  # Adjust with your actual database URI
Base.metadata.create_all(engine)


def seed_categories():
    categories = [
        ("rent", "🏠", 1200),
        ("insurance", "🔥", 400),
        ("food", "🍖", 600),
        ("work", "💼", 200),
        ("going out", "🕺", 380),
        ("hobbies", "🏄", 200),
        ("public transport", "🚂", 350),
        ("savings", "🏦", 400)
    ]
    with Session(engine) as session:
        for category in categories:
            new_category = Category(name=category[0], emoji=category[1], goal=category[2])
            session.add(new_category)
        session.commit()


def seed_expenses():
    sample_expenses = []
    with Session(engine) as session:
        for _ in range(18):
            # Fetch a random category ID
            random_category_id = session.query(Category.id).order_by(func.random()).first()[0]

            # Fetch the Category instance within the same session scope
            random_category = session.get(Category, random_category_id)

            amount = random.randint(10, 2000)
            days_ago = random.randint(1, 365)
            date = datetime.now() - timedelta(days=days_ago)

            # Create a new Expense instance
            expense = Expense(amount=amount, category=random_category, date=date)
            sample_expenses.append(expense)

        # Add all expenses to the session and commit
        session.add_all(sample_expenses)
        session.commit()


if __name__ == '__main__':
    seed_categories()
    seed_expenses()
