import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class GroceryExpiryListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Expiry List")
        self.root.configure(bg="light yellow")

        # I-center ang window sa screen
        self.center_window(900, 700)

        # Dito naka-store lahat ng items
        self.inventory = []

        # Pag-create ng mga UI widgets / interface
        self.create_widgets()

        # I-load ang mga items mula sa file
        self.load_inventory()

        # Ilipat ang expired papunta sa Expired List
        self.move_expired_items()

        # Magpakita ng warning para sa bagong expired
        self.notify_newly_expired()

        # Magpakita ng notification para sa items na malapit mag-expire
        self.notify_expiring_soon()

    # -------------------------------------
    def center_window(self, width, height):
        # Kinukuha ang screen size
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # Compute ng gitna
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        # Set ng laki at posisyon ng window
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # -------------------------------------
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="light yellow")
        main_frame.pack(expand=True)

        # Title ng app
        tk.Label(
            main_frame, text="GROCERY EXPIRY LIST",
            font=("Times New Roman", 40, "bold"), bg="light yellow"
        ).grid(row=0, column=0, columnspan=4, pady=(10, 40))

        # ============================
        # INPUT AREA (CENTERED)
        # ============================
        input_frame = tk.Frame(main_frame, bg="light yellow")
        input_frame.grid(row=1, column=0, columnspan=4, pady=(0, 15))

        # Item Name Input
        tk.Label(input_frame, text="Item Name", bg="light yellow",
                 font=("Times New Roman", 14)).grid(row=0, column=0, pady=5, padx=20)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Quantity Input
        tk.Label(input_frame, text="Quantity", bg="light yellow",
                 font=("Times New Roman", 14)).grid(row=1, column=0, pady=5, padx=20)
        self.qty_entry = tk.Entry(input_frame, width=30)
        self.qty_entry.grid(row=1, column=1, pady=5)

        # Expiry Date Input
        tk.Label(input_frame, text="Expiry Date (YYYY-MM-DD)", bg="light yellow",
                 font=("Times New Roman", 14)).grid(row=2, column=0, pady=5, padx=20)
        self.expiry_entry = tk.Entry(input_frame, width=30)
        self.expiry_entry.grid(row=2, column=1, pady=5)

        # ============================
        # BUTTONS AREA
        # ============================
        button_frame = tk.Frame(main_frame, bg="light yellow")
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        # Add Item Button
        tk.Button(button_frame, text="Add Item", command=self.add_item,
                  bg="lightgreen", width=15).grid(row=0, column=0, padx=10)

        # Remove Selected Item Button
        tk.Button(button_frame, text="Remove Selected", command=self.remove_item,
                  bg="tomato", fg="white", width=15).grid(row=0, column=1, padx=10)

        # Clear All Items Button
        tk.Button(button_frame, text="Clear All", command=self.clear_all,
                  bg="gray", fg="white", width=15).grid(row=0, column=2, padx=10)

        # Analytics Button
        tk.Button(button_frame, text="View Analytics", bg="gold",
                  command=self.toggle_analytics, width=15).grid(row=0, column=3, padx=10)

        # ============================
        # MAIN TABLE PARA SA VALID ITEMS
        # ============================
        columns = ("Item", "Quantity", "Expiry Date")

        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300, anchor="center")
        self.tree.grid(row=3, column=0, columnspan=4, pady=15)

        # Enable editing on double click
        self.tree.bind("<Double-1>", self.edit_item_window)

        # Label for expired section
        tk.Label(
            main_frame, text="⚠️ Expired Items",
            fg="red", bg="light yellow", font=("Arial", 12, "bold")
        ).grid(row=4, column=0, columnspan=4)

        # ============================
        # EXPIRED TABLE
        # ============================
        self.expired_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.expired_tree.heading(col, text=col)
            self.expired_tree.column(col, width=300, anchor="center")
        self.expired_tree.grid(row=5, column=0, columnspan=4, pady=10)

        self.expired_tree.bind("<Double-1>", self.edit_item_window)

        # ============================
        # SEARCH BAR
        # ============================
        tk.Label(main_frame, text="Search Item", bg="light yellow",
                 font=("Times New Roman", 12)).grid(row=6, column=0, pady=10)

        self.search_entry = tk.Entry(main_frame, width=40)
        self.search_entry.grid(row=6, column=1)

        tk.Button(main_frame, text="Search", command=self.search_item,
                  bg="lightblue").grid(row=6, column=2)

    # -------------------------------------
    # ANALYTICS WINDOW
    # (Simpleng summary ng total, expired at valid items)
    def toggle_analytics(self):
        win = tk.Toplevel(self.root)
        win.title("Analytics Overview")
        win.geometry("350x250")
        win.configure(bg="light yellow")

        # I-center ang analytics window
        win.update_idletasks()
        width = 350
        height = 250
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        # Bilangan ng items
        total = len(self.inventory)
        expired = len(self.expired_tree.get_children())
        valid = len(self.tree.get_children())

        # Title
        tk.Label(
            win, text="📊 EXPIRY LIST ANALYTICS",
            font=("Arial", 14, "bold"), bg="light yellow"
        ).pack(pady=10)

        # Data details
        tk.Label(win, text=f"Total Items: {total}",
                 font=("Arial", 12), bg="light yellow").pack(pady=5)

        tk.Label(win, text=f"Expired Items: {expired}",
                 font=("Arial", 12), fg="red", bg="light yellow").pack(pady=5)

        tk.Label(win, text=f"Valid Items: {valid}",
                 font=("Arial", 12), fg="green", bg="light yellow").pack(pady=5)

        # Close button
        tk.Button(win, text="Close", command=win.destroy,
                  bg="lightgray", width=10).pack(pady=15)

    # -------------------------------------
    # SAVE ITEMS TO FILE
    def save_inventory(self):
        with open("GroceryExpiryList.txt", "w") as file:
            for name, qty, expiry in self.inventory:
                file.write(f"{name}|{qty}|{expiry}\n")

    # -------------------------------------
    # LOAD ITEMS FROM FILE
    def load_inventory(self):
        try:
            with open("GroceryExpiryList.txt", "r") as file:
                for line in file:
                    name, qty, expiry = line.strip().split("|")
                    self.inventory.append((name, qty, expiry))
        except FileNotFoundError:
            pass  # Kung walang file, ignore lang

    # -------------------------------------
    # ILIPAT ANG MGA EXPIRED NA ITEM SA "EXPIRED" TABLE
    def move_expired_items(self):
        today = datetime.now().date()

        # Clear both tables bago i-update
        self.tree.delete(*self.tree.get_children())
        self.expired_tree.delete(*self.expired_tree.get_children())

        updated_inventory = []

        for name, qty, expiry in self.inventory:
            try:
                if expiry != "N/A":
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()

                    # Kapag expired na, ilagay sa expired table
                    if expiry_date <= today:
                        self.expired_tree.insert("", "end", values=(name, qty, expiry))
                    else:
                        self.tree.insert("", "end", values=(name, qty, expiry))
                else:
                    self.tree.insert("", "end", values=(name, qty, expiry))
            except:
                # Kung may mali sa date format, ilagay pa rin sa valid list
                self.tree.insert("", "end", values=(name, qty, expiry))

            updated_inventory.append((name, qty, expiry))

        self.inventory = updated_inventory
        self.save_inventory()

    # -------------------------------------
    # NOTIFICATION PARA SA BAGONG EXPIRED NA ITEMS
    def notify_newly_expired(self):
        today = datetime.now().date()
        expired_today = []

        for name, qty, expiry in self.inventory:
            if expiry != "N/A":
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                    if expiry_date <= today:
                        expired_today.append(name)
                except:
                    pass

        # Magpapakita ng warning box kung may expired
        if expired_today:
            messagebox.showwarning(
                "Expired Items",
                "The following items are EXPIRED:\n\n" + "\n".join(expired_today)
            )

    # -------------------------------------
    # MAG-NOTIFY KAPAG 1, 2, 3 DAYS BEFORE EXPIRY
    def notify_expiring_soon(self):
        today = datetime.now().date()

        exp1, exp2, exp3 = [], [], []

        for name, qty, expiry in self.inventory:
            if expiry != "N/A":
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                    days_left = (expiry_date - today).days

                    if days_left == 1:
                        exp1.append(name)
                    elif days_left == 2:
                        exp2.append(name)
                    elif days_left == 3:
                        exp3.append(name)
                except:
                    pass

        message = ""
        if exp1:
            message += "🔥 Items expiring in 1 day:\n" + "\n".join(exp1) + "\n\n"
        if exp2:
            message += "⚠ Items expiring in 2 days:\n" + "\n".join(exp2) + "\n\n"
        if exp3:
            message += "⚠ Items expiring in 3 days:\n" + "\n".join(exp3) + "\n\n"

        if message:
            messagebox.showinfo("Upcoming Expirations", message)

    # -------------------------------------
    # ADD ITEM BUTTON FUNCTION
    def add_item(self):
        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        expiry = self.expiry_entry.get().strip()

        # Error kapag walang name o quantity
        if not name or not qty:
            messagebox.showwarning("Input Error", "Item Name and Quantity are required.")
            return

        # Kung walang expiry, gagawing "N/A"
        expiry_display = expiry if expiry else "N/A"
        today = datetime.now().date()

        expiry_date = None
        if expiry_display.upper() != "N/A":
            try:
                expiry_date = datetime.strptime(expiry_display, "%Y-%m-%d").date()
            except:
                messagebox.showerror("Invalid Date Format", "Use YYYY-MM-DD.")
                return

        # Add item to inventory
        self.inventory.append((name, qty, expiry_display))

        # Determine kung expired o valid ang ilalagay
        if expiry_date and expiry_date <= today:
            self.expired_tree.insert("", "end", values=(name, qty, expiry_display))
        else:
            self.tree.insert("", "end", values=(name, qty, expiry_display))

        self.save_inventory()

        # I-clear input fields
        self.name_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)

    # -------------------------------------
    # EDIT ITEM WINDOW (ON DOUBLE CLICK)
    def edit_item_window(self, event):
        selected = None
        
        # Alamin kung alin ang list na na-click
        if self.tree.focus():
            selected = self.tree.focus()
            source_tree = self.tree
        elif self.expired_tree.focus():
            selected = self.expired_tree.focus()
            source_tree = self.expired_tree
        else:
            return

        values = source_tree.item(selected, "values")
        if not values:
            return

        old_name, old_qty, old_expiry = values

        # Create edit window
        win = tk.Toplevel(self.root)
        win.title("Edit Item")
        win.geometry("350x250")
        win.configure(bg="light yellow")

        # Title
        tk.Label(win, text="Edit Item Details", bg="light yellow",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # NAME
        tk.Label(win, text="Name:", bg="light yellow").pack()
        name_entry = tk.Entry(win)
        name_entry.insert(0, old_name)
        name_entry.pack()

        # QUANTITY
        tk.Label(win, text="Quantity:", bg="light yellow").pack()
        qty_entry = tk.Entry(win)
        qty_entry.insert(0, old_qty)
        qty_entry.pack()

        # EXPIRY
        tk.Label(win, text="Expiry (YYYY-MM-DD):", bg="light yellow").pack()
        expiry_entry = tk.Entry(win)
        expiry_entry.insert(0, old_expiry)
        expiry_entry.pack()

        # Save Button Logic
        def save_changes():
            new_name = name_entry.get().strip()
            new_qty = qty_entry.get().strip()
            new_expiry = expiry_entry.get().strip()

            # Required fields check
            if not new_name or not new_qty:
                messagebox.showwarning("Error", "Name and Quantity cannot be empty.")
                return

            # Date validation
            if new_expiry.upper() != "N/A":
                try:
                    datetime.strptime(new_expiry, "%Y-%m-%d")
                except:
                    messagebox.showerror("Invalid Date Format", "Use YYYY-MM-DD.")
                    return

            # Update inventory list
            if (old_name, old_qty, old_expiry) in self.inventory:
                index = self.inventory.index((old_name, old_qty, old_expiry))
                self.inventory[index] = (new_name, new_qty, new_expiry)

            self.save_inventory()
            self.move_expired_items()

            win.destroy()

        tk.Button(win, text="Save", bg="lightgreen", width=10,
                  command=save_changes).pack(pady=10)

        tk.Button(win, text="Cancel", bg="gray", fg="white", width=10,
                  command=win.destroy).pack()

    # -------------------------------------
    # REMOVE SELECTED ITEM
    def remove_item(self):
        selected_tree = self.tree.selection()
        selected_expired = self.expired_tree.selection()

        if not selected_tree and not selected_expired:
            messagebox.showinfo("Error", "No item selected.")
            return

        # Remove from valid list
        for item in selected_tree:
            values = self.tree.item(item, "values")
            if values in self.inventory:
                self.inventory.remove(values)
            self.tree.delete(item)

        # Remove from expired list
        for item in selected_expired:
            values = self.expired_tree.item(item, "values")
            if values in self.inventory:
                self.inventory.remove(values)
            self.expired_tree.delete(item)

        self.save_inventory()

    # -------------------------------------
    # CLEAR ALL ITEMS
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all items?"):
            self.tree.delete(*self.tree.get_children())
            self.expired_tree.delete(*self.expired_tree.get_children())
            self.inventory.clear()
            self.save_inventory()

    # -------------------------------------
    # SEARCH FUNCTION
    def search_item(self):
        query = self.search_entry.get().strip().lower()

        # Walang input sa search bar
        if not query:
            messagebox.showinfo("Search", "Please enter an item to search.")
            return

        found = False
        today = datetime.now().date()

        for name, qty, expiry in self.inventory:
            if query in name.lower():
                found = True

                # Walang expiry
                if expiry.upper() == "N/A":
                    messagebox.showinfo(
                        "Search Result",
                        f"Item: {name}\nQuantity: {qty}\nStatus: NO EXPIRY DATE"
                    )
                    break

                # Date validation
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                except:
                    messagebox.showinfo(
                        "Search Result",
                        f"Item: {name}\nQuantity: {qty}\nStatus: INVALID DATE FORMAT"
                    )
                    break

                days_left = (expiry_date - today).days

                # Kung expired
                if days_left < 0:
                    messagebox.showwarning(
                        "Search Result",
                        f"Item: {name}\nQuantity: {qty}\nExpiry: {expiry}\n\nSTATUS: EXPIRED ❌"
                    )
                # Kung today ang expiry
                elif days_left == 0:
                    messagebox.showwarning(
                        "Search Result",
                        f"Item: {name}\nQuantity: {qty}\nExpiry: {expiry}\n\nSTATUS: EXPIRES TODAY ⚠️"
                    )
                # Valid pa
                else:
                    messagebox.showinfo(
                        "Search Result",
                        f"Item: {name}\nQuantity: {qty}\nExpiry: {expiry}\n\nSTATUS: NOT EXPIRED ✔️\nDays Left: {days_left}"
                    )

                break

        if not found:
            messagebox.showinfo("Not Found", "Item not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryExpiryListApp(root)
    root.mainloop()
