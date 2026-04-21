import tkinter as tk
from tkinter import ttk

from src.dao.customer_dao import CustomerDAO

class CustomerTab(ttk.Frame):
    """
    The tab dedicated to managing customers. It includes a search/browse panel on the left and a detailed form on the right.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # --- Data Access ---
        self.customer_dao = CustomerDAO()
        self.current_customer =[]

        # --- UI Layout ---
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Left Panel: Search and Browse
        ttk.Label(left_frame, text="Search Customers", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        # Search Box and Buttons
        search_subframe = ttk.Frame(left_frame)
        search_subframe.pack(fill="x", pady=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_subframe, textvariable=self.search_var).pack(side="left", fill="x", expand=True)
        ttk.Button(search_subframe, text="Search").pack(side="left", padx=(2, 0))
        ttk.Button(search_subframe, text="Clear").pack(side="left", padx=(2, 0))

        # Customer List
        self.customer_listbox = tk.Listbox(left_frame, width=35, height=20)
        self.customer_listbox.pack(fill="y", expand=True, pady=5)
        self.customer_listbox.bind("<<ListboxSelect>>", self.on_customer_select)  # Bind selection event to a handler

        # Right Panel: Customer Details Form
        ttk.Label(right_frame, text="Customer Details", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        # Form Variables
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.apt_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.zip_var = tk.StringVar()

        # Build the form rows (Personal Info)
        ttk.Label(right_frame, text="Personal Information", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(10, 2))
        self.create_form_row(right_frame, "First Name:", self.first_name_var)
        self.create_form_row(right_frame, "Last Name:", self.last_name_var)
        self.create_form_row(right_frame, "DOB (YYYY-MM-DD):", self.dob_var)
        self.create_form_row(right_frame, "Phone:", self.phone_var)
        self.create_form_row(right_frame, "Email:", self.email_var)

        # Build the form rows (Address Info)
        ttk.Label(right_frame, text="Address", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(15, 2))
        self.create_form_row(right_frame, "Street:", self.street_var)
        self.create_form_row(right_frame, "Apt Number:", self.apt_var)
        self.create_form_row(right_frame, "City:", self.city_var)
        self.create_form_row(right_frame, "State:", self.state_var)
        self.create_form_row(right_frame, "Zipcode:", self.zip_var)

        # Bottom panel: Action Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="Add Customer").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Customer").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Customer").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form").pack(side="left", padx=5)

        # Feature Button: View Policies (for the selected customer)
        ttk.Button(btn_frame, text="View Policies ->").pack(side="right", padx=5)

        # Call to load customers into the listbox when the tab is initialized
        self.load_customers()

    def load_customers(self):
        """Fetches customers from the Oracle DB and populates the listbox."""
        self.customer_listbox.delete(0, tk.END)
        try:
            # Fetch all records using your teammates' DAO
            self.current_customers = self.customer_dao.get_all()
            for c in self.current_customers:
                display_text = f"ID {c.customer_id}: {c.last_name}, {c.first_name}"
                self.customer_listbox.insert(tk.END, display_text)
        except Exception as e:
            print(f"Database Error: {e}")
            self.customer_listbox.insert(tk.END, "Error connecting to Database")

    def on_customer_select(self, event):
        """Fills the form on the right when a name is clicked on the left."""
        if not self.customer_listbox.curselection():
            return

        index = self.customer_listbox.curselection()[0]
        selected_customer = self.current_customers[index]

        # Populate the text boxes with the database values
        self.first_name_var.set(selected_customer.first_name or "")
        self.last_name_var.set(selected_customer.last_name or "")

        # Safely format the date if it exists
        dob_str = selected_customer.date_of_birth.strftime("%Y-%m-%d") if selected_customer.date_of_birth else ""
        self.dob_var.set(dob_str)

        self.phone_var.set(selected_customer.phone_number or "")
        self.email_var.set(selected_customer.email or "")
        self.street_var.set(selected_customer.street or "")
        self.apt_var.set(selected_customer.apartment_number or "")
        self.city_var.set(selected_customer.city or "")
        self.state_var.set(selected_customer.state or "")
        self.zip_var.set(selected_customer.zipcode or "")

    def clear_form(self):
        """Clears all text boxes."""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.dob_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.street_var.set("")
        self.apt_var.set("")
        self.city_var.set("")
        self.state_var.set("")
        self.zip_var.set("")
        self.customer_listbox.selection_clear(0, tk.END)

    def create_form_row(self, parent, label_text, variable):
        """ Helper function to create a labeled text box neatly."""
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label_text, width=25).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)

class PolicyTab(ttk.Frame):
    """
    The tab dedicated to managing insurance policies. It includes a search/browse panel on the left
    and a detailed form on the right that dynamically changes based on the policy type.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # --- UI Layout ---
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)


        # LEFT PANEL: Search & Browse
        ttk.Label(left_frame, text="Search Policies", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        search_subframe = ttk.Frame(left_frame)
        search_subframe.pack(fill="x", pady=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_subframe, textvariable=self.search_var).pack(side="left", fill="x", expand=True)
        ttk.Button(search_subframe, text="Search").pack(side="left", padx=(2, 0))
        ttk.Button(search_subframe, text="Clear").pack(side="left", padx=(2, 0))

        self.policy_listbox = tk.Listbox(left_frame, width=35, height=20)
        self.policy_listbox.pack(fill="y", expand=True, pady=5)

        # RIGHT PANEL: Base Policy Form
        ttk.Label(right_frame, text="Policy Details", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        self.customer_id_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.monthly_payment_var = tk.StringVar()
        self.coverage_var = tk.StringVar()
        self.policy_type_var = tk.StringVar(value="HOME")  # Default value

        ttk.Label(right_frame, text="Base Information", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(5, 2))
        self.create_form_row(right_frame, "Customer ID:", self.customer_id_var)
        self.create_form_row(right_frame, "Start Date (YYYY-MM-DD):", self.start_date_var)
        self.create_form_row(right_frame, "Monthly Payment ($):", self.monthly_payment_var)
        self.create_form_row(right_frame, "Coverage Amount ($):", self.coverage_var)

        # Dropdown for Policy Type
        type_row = ttk.Frame(right_frame)
        type_row.pack(fill="x", pady=5)
        ttk.Label(type_row, text="Policy Type:", width=25).pack(side="left")
        type_combo = ttk.Combobox(type_row, textvariable=self.policy_type_var, values=["HOME", "CAR", "LIFE"], state="readonly")
        type_combo.pack(side="left", fill="x", expand=True)

        # Trigger an update whenever the dropdown value changes
        self.policy_type_var.trace_add("write", self.update_dynamic_frames)

        # Dynamic sub-frames - Container to hold the specific fields for each policy type.
        self.dynamic_container = ttk.Frame(right_frame)
        self.dynamic_container.pack(fill="x", pady=10)

        # Home frames and variables
        self.home_frame = ttk.Frame(self.dynamic_container)
        self.house_price_var = tk.StringVar()
        self.house_area_var = tk.StringVar()
        self.bedrooms_var = tk.StringVar()
        self.bathrooms_var = tk.StringVar()
        self.home_end_date_var = tk.StringVar()

        # Address vars for home
        self.home_street_var = tk.StringVar()
        self.home_city_var = tk.StringVar()

        ttk.Label(self.home_frame, text="Home specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))

        self.create_form_row(self.home_frame, "House Price:", self.house_price_var)
        self.create_form_row(self.home_frame, "House Area (sq ft):", self.house_area_var)
        self.create_form_row(self.home_frame, "Bedrooms:", self.bedrooms_var)
        self.create_form_row(self.home_frame, "Bathrooms:", self.bathrooms_var)
        self.create_form_row(self.home_frame, "End Date:", self.home_end_date_var)
        self.create_form_row(self.home_frame, "Street Address:", self.home_street_var)
        self.create_form_row(self.home_frame, "City:", self.home_city_var)

        # Car frame and variables
        self.car_frame = ttk.Frame(self.dynamic_container)
        self.make_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.vin_var = tk.StringVar()
        self.mileage_var = tk.StringVar()
        self.car_end_date_var = tk.StringVar()

        ttk.Label(self.car_frame, text="Vehicle specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))

        self.create_form_row(self.car_frame, "Make:", self.make_var)
        self.create_form_row(self.car_frame, "Model:", self.model_var)
        self.create_form_row(self.car_frame, "VIN:", self.vin_var)
        self.create_form_row(self.car_frame, "Yearly Mileage:", self.mileage_var)
        self.create_form_row(self.car_frame, "End Date:", self.car_end_date_var)

        # Life frame and variables
        self.life_frame = ttk.Frame(self.dynamic_container)
        self.conditions_var = tk.StringVar()
        self.beneficiary_var = tk.StringVar()

        ttk.Label(self.life_frame, text="Life policy specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))
        self.create_form_row(self.life_frame, "Existing Conditions:", self.conditions_var)
        self.create_form_row(self.life_frame, "Beneficiary:", self.beneficiary_var)

        # Initially show the correct frame based on the default dropdown value
        self.update_dynamic_frames()

        # Bottom panel: Action Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="Add Policy").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Policy").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Policy").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form").pack(side="left", padx=5)

    # Function to create a labeled entry row in the form, used for both base and dynamic fields.
    def create_form_row(self, parent, label_text, variable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label_text, width=25).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)

    # Function that updates which dynamic sub-frame is visible based on the selected policy type in the dropdown.
    def update_dynamic_frames(self, *args):
        """Hides all sub-frames and only shows the one matching the dropdown."""
        self.home_frame.pack_forget()
        self.car_frame.pack_forget()
        self.life_frame.pack_forget()

        selected_type = self.policy_type_var.get()
        if selected_type == "HOME":
            self.home_frame.pack(fill="both", expand=True)
        elif selected_type == "CAR":
            self.car_frame.pack(fill="both", expand=True)
        elif selected_type == "LIFE":
            self.life_frame.pack(fill="both", expand=True)


class InsuranceApp(tk.Tk):
    """
    The main application window that contains the notebook with the Customer and Policy tabs.
    """
    def __init__(self):
        super().__init__()
        self.title("Insurance Management System")
        self.geometry("950x650")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.customer_tab = CustomerTab(self.notebook)
        self.notebook.add(self.customer_tab, text="Customers")
        self.policy_tab = PolicyTab(self.notebook)
        self.notebook.add(self.policy_tab, text="Policies")

# Call the main application
if __name__ == "__main__":
    app = InsuranceApp()
    app.mainloop()