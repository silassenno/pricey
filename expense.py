from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    emoji: Mapped[str] = mapped_column(String, unique=True)
    goal: Mapped[Numeric] = mapped_column(Numeric, nullable=True)

    # Relationship to expenses
    expenses = relationship("Expense")

    def get_expenses_for_month(self, month, year):
        total_expenses = sum(expense.amount for expense in self.expenses
                             if expense.date.strftime("%B") == month and expense.date.year == year)

        return total_expenses


class Expense(Base):
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Numeric] = mapped_column(Numeric)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    date: Mapped[datetime] = mapped_column(DateTime)

    # Relationship with category
    category = relationship("Category", back_populates="expenses")
