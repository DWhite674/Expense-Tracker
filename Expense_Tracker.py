import csv
import os
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import ttk, messagebox

FILE_NAME = "expenses.csv"

def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()
    
    if not category or not amount:
        messagebox.showwarning("Input Error", "Category and Amount are required!")
        return

    try: 
        amount_val = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number!")
        return
    
    
    with open(FILE_NAME, "a", newline= "") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount_val, description])
    
    
    messagebox.showinfo("Success", "Expense added!")
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    load_expenses()
    

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
        
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2 or not row[1]:
                continue
            tree.insert("", tk.END, values=row)
            
                    
def show_summary():
    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("Summary", "No expenses recorded yet!")
        return
    
    totals = {}
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2 or not row[1]:
                continue
            category, amount, _ = row
            totals[category] = totals.get(category, 0) + float(amount)


    summary_text = "\n".join(f"{cat}: ${amt:.2f}" for cat, amt in totals.items())
    total_spent = sum(totals.values())
    summary_text += f"\n\nTotal Spent: ${total_spent:.2f}"
    messagebox.showinfo("Summary", summary_text)
    
    plt.bar(totals.keys(), totals.values(), color="skyblue")
    plt.title("spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=30)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    
    
root = tk.Tk()
root.title("expense Tracker")

tk.Label(root, text="Category").grid(row=0, column = 0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=0, column=1, padx=5, pady=5)


tk.Label(root, text="Amount").grid(row=1, column= 0 , padx = 5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Description").grid(row=2,column=0, padx=5, pady=5)
desc_entry = tk.Entry(root)
desc_entry.grid(row=2, column=1, padx=5, pady=5)


tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Summary & Graph", command=show_summary).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Exit", command=root.quit).grid(row=3, column=3, padx=5, pady=5)

tree = ttk.Treeview(root, columns=("Category", "Amount", "Description"), show="headings")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

load_expenses()
root.mainloop()