from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
2
class MasterBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, nullable=False)
    remaining_budget = db.Column(db.Float, nullable=False, default=0.0)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)  
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    next_due_date = db.Column(db.Date, nullable=False)        

@app.route('/')
def index():
    today = date.today()
    budgets = Budget.query.filter(Budget.end_date >= today).all()
    expenses = Expense.query.all()
    master_budget = MasterBudget.query.first()
    
    total_budget = master_budget.total_budget if master_budget else 0
    remaining_budget = master_budget.remaining_budget if master_budget else 0
    total_spending = db.session.query(db.func.sum(Expense.amount)).scalar() or 0

    # Retrieve subscriptions for the main page and for subscription alerts
    subscriptions = Subscription.query.all()
    for subscription in subscriptions:
        days_until_due = (subscription.next_due_date - today).days
        if 0 <= days_until_due <= 7:
            flash(f"Alert: Your subscription '{subscription.name}' is due in {days_until_due} day(s) on {subscription.next_due_date.strftime('%Y-%m-%d')}.")

    return render_template('index.html', 
                           budgets=budgets, 
                           expenses=expenses,
                           master_budget=master_budget, 
                           total_budget=total_budget,
                           remaining_budget=remaining_budget,
                           total_spending=total_spending,
                           subscriptions=subscriptions)

@app.route('/set_master_budget', methods=['GET', 'POST'])
def set_master_budget():
    master_budget = MasterBudget.query.first()
    
    if request.method == 'POST':
        total_budget = float(request.form['total_budget'])
        
        # Calculate remaining budget based on current expenses
        total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
        remaining_budget = total_budget - total_expenses
        
        if master_budget:
            master_budget.total_budget = total_budget
            master_budget.remaining_budget = remaining_budget
        else:
            master_budget = MasterBudget(total_budget=total_budget, remaining_budget=remaining_budget)
            db.session.add(master_budget)

        db.session.commit()
        flash('Master budget set successfully!')
        return redirect(url_for('index'))

    return render_template('setmasterbudget.html', master_budget=master_budget)

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        # Create the sub-budget with remaining_amount equal to amount
        new_budget = Budget(
            category=category,
            amount=amount,
            remaining_amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_budget)

        # Update the master budget by reducing its remaining_budget by the new sub-budget amount
        master_budget = MasterBudget.query.first()
        if master_budget:
            master_budget.remaining_budget -= amount
        else:
            flash("Please set a master budget first.")
            return redirect(url_for('set_master_budget'))
        
        db.session.commit()
        flash('Budget set successfully!')
        return redirect(url_for('index'))

    return render_template('setbudget.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()

        # Look up the sub-budget for this expense category
        budget = Budget.query.filter_by(category=category).first()
        if not budget:
            flash("No sub-budget set for this category. Please create one first.")
            return redirect(url_for('add_expense'))

        # Ensure the expense does not exceed the sub-budget's remaining amount
        if amount > budget.remaining_amount:
            flash("Expense exceeds the remaining amount of the sub-budget for this category.")
            return redirect(url_for('add_expense'))

        new_expense = Expense(category=category, amount=amount, date=expense_date)
        db.session.add(new_expense)

        # Reduce the sub-budget's remaining amount
        budget.remaining_amount -= amount

        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('index'))
    else:
        # Retrieve all budgets and extract unique categories
        budgets = Budget.query.all()
        categories = list({budget.category for budget in budgets})
        return render_template('addexpense.html', categories=categories)

@app.route('/add_subscription', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        next_due_date = datetime.strptime(request.form['next_due_date'], '%Y-%m-%d').date()

        new_subscription = Subscription(name=name, amount=amount, next_due_date=next_due_date)
        db.session.add(new_subscription)
        db.session.commit()

        flash('Subscription added successfully!')
        return redirect(url_for('index'))
    
    return render_template('addsubscription.html')    

@app.route('/clear_data')
def clear_data():
    db.session.query(Expense).delete()
    db.session.query(Budget).delete()
    db.session.query(MasterBudget).delete()
    db.session.query(Subscription).delete()  # Delete subscription data as well
    db.session.commit()
    flash('All data cleared successfully!')
    return redirect(url_for('index'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 