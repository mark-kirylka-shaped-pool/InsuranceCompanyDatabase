import tkinter as tk
from tkinter import ttk
from datetime import datetime

from src.dao.customer_dao import CustomerDAO, Customer
from src.dao.policy_dao import PolicyDAO, Policy
from src.dao.home_insurance_dao import HomeInsuranceDAO, HomeInsurance
from src.dao.car_insurance_dao import CarInsuranceDAO, CarInsurance
from src.dao.life_insurance_dao import LifeInsuranceDAO, LifeInsurance
# ----------------------------------------------------------------------------------------------------------------------

def create_form_row(parent, label_text, variable):
    """" Helper function to create a labeled text box neatly."""
    row = ttk.Frame(parent)
    row.pack(fill="x", pady=2)
    ttk.Label(row, text=label_text, width=25).pack(side="left")
    ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
# ----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
# --- CUSTOMER TAB ---
class CustomerTab(ttk.Frame):
    """
    The tab dedicated to managing customers. It includes a search/browse panel on the left and a detailed form on the right.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # --- Customers data access ---
        self.customer_dao = CustomerDAO()
        self.current_customer: list =[]

        # --- UI Layout ---
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Left Panel: Search & Browse
        ttk.Label(left_frame, text="Search Customers", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        # Search Box and Buttons
        search_subframe = ttk.Frame(left_frame)
        search_subframe.pack(fill="x", pady=5)
        self.customer_search_var = tk.StringVar()
        ttk.Entry(search_subframe, textvariable=self.customer_search_var).pack(side="left", fill="x", expand=True)
        ttk.Button(search_subframe, text="Search", command=self.search_customers).pack(side="left", padx=(2, 0))
        ttk.Button(search_subframe, text="Clear", command=self.clear_customer_search).pack(side="left", padx=(2, 0))

        # Customer List
        self.customer_listbox = tk.Listbox(left_frame, width=35, height=20, exportselection=False)
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
        create_form_row(right_frame, "First Name:", self.first_name_var)
        create_form_row(right_frame, "Last Name:", self.last_name_var)
        create_form_row(right_frame, "DOB (YYYY-MM-DD):", self.dob_var)
        create_form_row(right_frame, "Phone:", self.phone_var)
        create_form_row(right_frame, "Email:", self.email_var)

        # Build the form rows (Address Info)
        ttk.Label(right_frame, text="Address", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(15, 2))
        create_form_row(right_frame, "Street:", self.street_var)
        create_form_row(right_frame, "Apt Number:", self.apt_var)
        create_form_row(right_frame, "City:", self.city_var)
        create_form_row(right_frame, "State:", self.state_var)
        create_form_row(right_frame, "Zipcode:", self.zip_var)

        # Bottom panel: Action Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="Add Customer", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Customer", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Customer", command=self.delete_customer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View Policies ->", command=self.view_customer_policies).pack(side="right", padx=5)

        # Call to load customers into the listbox when the tab is initialized
        self.load_customers()
    # ------------------------------------------------------------------------------------------------------------------

    def load_customers(self):
        """Fetches customers from the Oracle DB and populates the listbox."""
        self.customer_listbox.delete(0, tk.END)
        try:
            # Call the get_all method from your teammates' CustomerDAO to fetch all records
            self.current_customers = self.customer_dao.get_all()
            for c in self.current_customers:
                display_text = f"ID {c.customer_id}: {c.last_name}, {c.first_name}"
                self.customer_listbox.insert(tk.END, display_text)
        except Exception as e:
            print(f"Database Error while loading customers: {e}")
            self.customer_listbox.insert(tk.END, "Error loading customers from Database")
    # ------------------------------------------------------------------------------------------------------------------

    def on_customer_select(self, event):
        """Fills the 'Customer Details' form with the data from the selected customer in the listbox."""
        # Get the index of the selected item in the listbox
        if not self.customer_listbox.curselection():
            return

        index = self.customer_listbox.curselection()[0]
        selected_customer = self.current_customers[index]

        # Populate the text boxes with the database values
        self.first_name_var.set(selected_customer.first_name or "")
        self.last_name_var.set(selected_customer.last_name or "")

        # Safely format the date if it exists
        dob_str = selected_customer.date_of_birth.strftime("%Y-%m-%d") \
            if hasattr(selected_customer.date_of_birth, 'strftime') else (selected_customer.date_of_birth or "")
        self.dob_var.set(dob_str)

        self.phone_var.set(selected_customer.phone_number or "")
        self.email_var.set(selected_customer.email or "")
        self.street_var.set(selected_customer.street or "")
        self.apt_var.set(selected_customer.apartment_number or "")
        self.city_var.set(selected_customer.city or "")
        self.state_var.set(selected_customer.state or "")
        self.zip_var.set(selected_customer.zipcode or "")
    # ------------------------------------------------------------------------------------------------------------------

    def add_customer(self):
        """
        Add a new customer to the database using the data from the form. It performs basic validation, converts the
        DOB to a date object, creates a Customer object, and then calls the DAO to save it to the database.
        """
        try:
            # Grab all the data from the text boxes and trim whitespace
            first = self.first_name_var.get().strip()
            last = self.last_name_var.get().strip()
            dob_str = self.dob_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()
            street = self.street_var.get().strip()
            apt = self.apt_var.get().strip()
            city = self.city_var.get().strip()
            state = self.state_var.get().strip()
            zipcode = self.zip_var.get().strip()

            # Basic Validation: Make sure they at least entered a name
            if not first or not last:
                print("Validation Error: First and Last name are required.")
                return

            # Convert the DOB string into a datetime object
            parsed_dob = None
            if dob_str:
                try:
                    parsed_dob = datetime.strptime(dob_str, "%Y-%m-%d")
                except ValueError:
                    print("Date Error: Please use YYYY-MM-DD format.")
                    return

            # Create a Customer object with the form data
            new_customer = Customer(
                first_name=first,
                last_name=last,
                date_of_birth=parsed_dob,
                phone_number=phone,
                email=email,
                street=street,
                city=city,
                state=state,
                apartment_number=apt,
                zipcode=zipcode
            )

            # Hand it off to the DAO to add it to the database
            self.customer_dao.add(new_customer)
            print("Success! Customer added to Oracle.")

            # Refresh the visual list and clear the text boxes!
            self.load_customers()
            self.clear_form()

        except Exception as e:
            print(f"Failed to add customer: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def delete_customer(self):
        """
        Deletes the selected customer from the database. It first checks if a customer is selected, then confirms the
        deletion, and finally calls the DAO to remove it from the database.
        """
        try:
            # Make sure they actually clicked on someone in the list first
            if not self.customer_listbox.curselection():
                print("Action Error: Please select a customer from the list to delete.")
                return

            # Figure out exactly who is selected
            index = self.customer_listbox.curselection()[0]
            selected_customer = self.current_customers[index]

            # Send their specific ID to the database to be removed
            self.customer_dao.remove(selected_customer.customer_id)
            print(f"Success! Customer ID {selected_customer.customer_id} deleted from Oracle.")

            # Refresh the visual list and clear the text boxes!
            self.load_customers()
            self.clear_form()

        except Exception as e:
            print(f"Failed to delete customer: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def update_customer(self):
        """
        Updates the selected customer's information in the database. It gathers the data from the form, validates it,
        creates a new Customer object with the same ID, and sends it to the DAO to update the record in the database.
        """
        try:
            # Make sure a customer is selected
            if not self.customer_listbox.curselection():
                print("Action Error: Please select a customer from the list to update.")
                return

            # Get the original ID of the person we are editing
            index = self.customer_listbox.curselection()[0]
            original_customer = self.current_customers[index]
            target_id = original_customer.customer_id

            # Grab all the data from the text boxes and trim whitespace
            first = self.first_name_var.get().strip()
            last = self.last_name_var.get().strip()
            dob_str = self.dob_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()
            street = self.street_var.get().strip()
            apt = self.apt_var.get().strip()
            city = self.city_var.get().strip()
            state = self.state_var.get().strip()
            zipcode = self.zip_var.get().strip()

            # Basic Validation: Make sure they at least entered a name
            if not first or not last:
                print("Validation Error: First and Last name are required.")
                return

            # Convert the DOB string into a datetime object
            parsed_dob = None
            if dob_str:
                try:
                    parsed_dob = datetime.strptime(dob_str, "%Y-%m-%d")
                except ValueError:
                    print("Date Error: Please use YYYY-MM-DD format.")
                    return

            # Update the Customer object with the form data (including the original ID so the DAO knows who to update)
            updated_customer = Customer(
                first_name=first,
                last_name=last,
                date_of_birth=parsed_dob,
                phone_number=phone,
                email=email,
                street=street,
                city=city,
                state=state,
                apartment_number=apt,
                zipcode=zipcode,
                customer_id=target_id  # The DAO needs this to know who to overwrite
            )

            # Send the update to the database
            self.customer_dao.update(updated_customer)
            print(f"Success! Customer ID {target_id} updated in Oracle.")

            # Refresh the list and clear the form
            self.load_customers()
            self.clear_form()

        except Exception as e:
            print(f"Failed to update customer: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def search_customers(self):
        """
        Searches for customers based on the query in the search box. It filters the currently loaded customers in
        memory and updates the listbox to show only matching results. The search looks for matches in the customer
        ID, first name, or last name.
        """
        query = self.customer_search_var.get().strip().lower()

        # Always load fresh from DB first to get the full list
        self.load_customers()

        if not query:
            return  # If the search box is empty, we just leave the full list loaded!

        # Filter what was just loaded
        filtered_customers = []
        self.customer_listbox.delete(0, tk.END)

        for c in self.current_customers:
            # Check if the query matches the ID or name
            if query in str(c.customer_id) or query in c.first_name.lower() or query in c.last_name.lower():
                filtered_customers.append(c)
                self.customer_listbox.insert(tk.END, f"ID {c.customer_id}: {c.last_name}, {c.first_name}")

        # Update the memory array so clicking them still works perfectly!
        self.current_customers = filtered_customers
    # ------------------------------------------------------------------------------------------------------------------

    def clear_customer_search(self):
        """Clears the search box and reloads the full customer list from the database."""
        self.customer_search_var.set("")
        self.load_customers()
    # ------------------------------------------------------------------------------------------------------------------

    def view_customer_policies(self):
        """Switches to the Policy tab and searches for the selected customer."""
        try:
            # Make sure a customer is selected
            if not self.customer_listbox.curselection():
                print("Action Error: Please select a customer to view their policies.")
                return

            # Grab the ID of the selected customer
            index = self.customer_listbox.curselection()[0]
            selected_customer = self.current_customers[index]
            cust_id = selected_customer.customer_id

            # Safety check: make sure the tabs have been linked together
            if not hasattr(self, 'policy_tab') or not hasattr(self, 'notebook'):
                print("System Error: Customer Tab has not been linked to the Policy Tab yet.")
                return

            # Visually flip the notebook over to the Policy Tab
            self.notebook.select(self.policy_tab)

            # Type the ID into the Policy search box
            self.policy_tab.policy_search_var.set(str(cust_id))

            # "Click" the Policy search button automatically!
            self.policy_tab.search_policies()

        except Exception as e:
            print(f"Failed to switch to policies: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def clear_form(self):
        """Clears all text boxes and resets the form to a blank state. Also clears the selection in the listbox."""
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
    # ------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================
# --- POLICY TAB ---
class PolicyTab(ttk.Frame):
    """
    The tab dedicated to managing insurance policies. It includes a search/browse panel on the left
    and a detailed form on the right that dynamically changes based on the policy type.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # --- Policies data Access ---
        self.policy_dao = PolicyDAO()
        self.home_insurance_dao = HomeInsuranceDAO()
        self.car_insurance_dao = CarInsuranceDAO()
        self.life_insurance_dao = LifeInsuranceDAO()

        self.customer_dao = CustomerDAO()

        self.current_policies_data: list = []
        self. selected_policy_index = None          # Tracks which policy is currently selected in the listbox

        # --- UI Layout ---
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)


        # LEFT PANEL: Search & Browse
        ttk.Label(left_frame, text="Search Policies", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        # Search Box and Buttons
        search_subframe = ttk.Frame(left_frame)
        search_subframe.pack(fill="x", pady=5)
        self.policy_search_var = tk.StringVar()
        ttk.Entry(search_subframe, textvariable=self.policy_search_var).pack(side="left", fill="x", expand=True)
        ttk.Button(search_subframe, text="Search", command=self.search_policies).pack(side="left", padx=(2, 0))
        ttk.Button(search_subframe, text="Clear", command=self.clear_policy_search).pack(side="left", padx=(2, 0))

        # Policy List
        self.policy_listbox = tk.Listbox(left_frame, width=45, height=20, exportselection=False)
        self.policy_listbox.pack(fill="y", expand=True, pady=5)
        self.policy_listbox.bind("<<ListboxSelect>>", self.on_policy_select)

        # RIGHT PANEL: Policy Details Form
        ttk.Label(right_frame, text="Policy Details", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        # Form Variables
        self.customer_id_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.monthly_payment_var = tk.StringVar()
        self.coverage_var = tk.StringVar()
        self.policy_type_var = tk.StringVar(value="HOME")  # Default value

        # Build the form rows (Base Information)
        ttk.Label(right_frame, text="Base Information", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(5, 2))
        create_form_row(right_frame, "Customer ID:", self.customer_id_var)
        create_form_row(right_frame, "Start Date (YYYY-MM-DD):", self.start_date_var)
        create_form_row(right_frame, "Monthly Payment ($):", self.monthly_payment_var)
        create_form_row(right_frame, "Coverage Amount ($):", self.coverage_var)

        # Policy Type Display (non-editable, just shows the type of the currently selected policy)
        type_row = ttk.Frame(right_frame)
        type_row.pack(fill="x", pady=5)
        ttk.Label(type_row, text="Policy Type:", width=25).pack(side="left")
        type_combo = ttk.Combobox(type_row, textvariable=self.policy_type_var, values=["HOME", "CAR", "LIFE"], state="readonly")
        type_combo.pack(side="left", fill="x", expand=True)

        # Whenever the policy type changes (either by selection or programmatically), we need to update the dynamic fields shown on the right.
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
        self.home_street_var = tk.StringVar()
        self.home_city_var = tk.StringVar()
        self.home_state_var = tk.StringVar()
        self.home_zip_var = tk.StringVar()

        # Build the home insurance specific fields
        ttk.Label(self.home_frame, text="Home specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))
        create_form_row(self.home_frame, "House Price:", self.house_price_var)
        create_form_row(self.home_frame, "House Area (sq ft):", self.house_area_var)
        create_form_row(self.home_frame, "Bedrooms:", self.bedrooms_var)
        create_form_row(self.home_frame, "Bathrooms:", self.bathrooms_var)
        create_form_row(self.home_frame, "End Date:", self.home_end_date_var)
        create_form_row(self.home_frame, "Street Address:", self.home_street_var)
        create_form_row(self.home_frame, "City:", self.home_city_var)
        create_form_row(self.home_frame, "State:", self.home_state_var)
        create_form_row(self.home_frame, "Zipcode:", self.home_zip_var)

        # Button to copy the customer's address into the home insurance fields when creating a new home policy
        ttk.Button(self.home_frame, text="Copy Address from Customer ID", command=self.copy_customer_address).pack(anchor="w", pady=5, padx=25)

        # Car frame and variables
        self.car_frame = ttk.Frame(self.dynamic_container)
        self.make_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.vin_var = tk.StringVar()
        self.mileage_var = tk.StringVar()
        self.car_end_date_var = tk.StringVar()

        # Build the car insurance specific fields
        ttk.Label(self.car_frame, text="Vehicle specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))
        create_form_row(self.car_frame, "Make:", self.make_var)
        create_form_row(self.car_frame, "Model:", self.model_var)
        create_form_row(self.car_frame, "VIN:", self.vin_var)
        create_form_row(self.car_frame, "Yearly Mileage:", self.mileage_var)
        create_form_row(self.car_frame, "End Date:", self.car_end_date_var)

        # Life frame and variables
        self.life_frame = ttk.Frame(self.dynamic_container)
        self.conditions_var = tk.StringVar()
        self.beneficiary_var = tk.StringVar()

        # Build the life insurance specific fields
        ttk.Label(self.life_frame, text="Life policy specifics", font=("Helvetica", 10, "italic")).pack(anchor="w", pady=(0, 2))
        create_form_row(self.life_frame, "Existing Conditions:", self.conditions_var)
        create_form_row(self.life_frame, "Beneficiary:", self.beneficiary_var)

        # Initially show the home insurance frame by default
        self.update_dynamic_frames()

        # Bottom panel: Action Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="Add Policy", command=self.add_policy).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Policy", command=self.update_policy).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Policy", command=self.delete_policy).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)

        # Call to load policies into the listbox when the tab is initialized
        self.load_policies()
    # ------------------------------------------------------------------------------------------------------------------

    def load_policies(self):
        """Fetches policies from the Oracle DB and populates the listbox."""
        self.policy_listbox.delete(0, tk.END)
        self.current_policies_data = []                         # Clear the current policies data list to prevent stale data issues when we reload from the database
        try:
            base_policies = self.policy_dao.get_all()
            for p in base_policies:
                p_type = "UNKNOWN"
                details = None

                # Check child tables to determine policy type and get specific details
                home_records = self.home_insurance_dao.get_by_policy(p.policy_id)
                car_records = self.car_insurance_dao.get_by_policy(p.policy_id)
                life_records = self.life_insurance_dao.get_by_policy(p.policy_id)

                if home_records:
                    p_type = "HOME"
                    details = home_records[0]
                elif car_records:
                    p_type = "CAR"
                    details = car_records[0]
                elif life_records:
                    p_type = "LIFE"
                    details = life_records[0]

                self.current_policies_data.append({"base": p, "type": p_type, "details": details})

                # Format the display text for the listbox entry
                display_text = f"ID {p.policy_id}: [{p_type}] Customer {p.customer_id}) - ${p.coverage}"
                self.policy_listbox.insert(tk.END, display_text)

        except Exception as e:
            print(f"Database Error while loading policies: {e}")
            self.policy_listbox.insert(tk.END, "Error loading policies from Database")
    #-------------------------------------------------------------------------------------------------------------------

    def on_policy_select(self, event=None):
        """Fills the form on the right when a policy is clicked on the left."""
        if not self.policy_listbox.curselection():
            return

        index = self.policy_listbox.curselection()[0]
        data = self.current_policies_data[index]

        self.clear_form()  # Clear the form before populating new data

        self.selected_policy_index = index  # Update the currently selected policy index

        # Populate the base fields
        self.populate_base_fields(data["base"], data["type"])
        self.populate_dynamic_fields(data["type"], data["details"])
    # ------------------------------------------------------------------------------------------------------------------

    def populate_base_fields(self, base_p, p_type):
        """Helper to fill out the top half of the form that is common to all policy types."""
        self.customer_id_var.set(base_p.customer_id or "")
        start_str = base_p.start_date.strftime("%Y-%m-%d") if hasattr(base_p.start_date, 'strftime') else (base_p.start_date or "")
        self.start_date_var.set(start_str)
        self.monthly_payment_var.set(base_p.monthly_payment or "")
        self.coverage_var.set(base_p.coverage or "")
        self.policy_type_var.set(p_type)
    # ------------------------------------------------------------------------------------------------------------------

    def populate_dynamic_fields(self, p_type, details):
        """Helper to fill out the bottom half of the form based on the policy type."""
        if not details: return

        if p_type == "HOME":
            self.house_price_var.set(details.house_price or "")
            self.house_area_var.set(details.house_area or "")
            self.bedrooms_var.set(details.bedroom_number or "")
            self.bathrooms_var.set(details.bathroom_number or "")
            end_str = details.end_date.strftime("%Y-%m-%d") if hasattr(details.end_date, 'strftime') else (
                        details.end_date or "")
            self.home_end_date_var.set(end_str)
            self.home_street_var.set(details.street or "")
            self.home_city_var.set(details.city or "")
        elif p_type == "CAR":
            self.make_var.set(details.make or "")
            self.model_var.set(details.model or "")
            self.vin_var.set(details.vin or "")
            self.mileage_var.set(details.yearly_mileage or "")
            end_str = details.end_date.strftime("%Y-%m-%d") if hasattr(details.end_date, 'strftime') else (
                        details.end_date or "")
            self.car_end_date_var.set(end_str)
        elif p_type == "LIFE":
            self.conditions_var.set(details.existing_conditions or "")
            self.beneficiary_var.set(details.beneficiary or "")
    # ------------------------------------------------------------------------------------------------------------------

    def add_policy(self):
        """
        Adds a new policy to the database. It first validates the base information, creates a Policy record to get
        the new ID, and then creates the specific sub-record based on the selected policy type.
        """
        try:
            # Grab the base information from the form
            cust_id = self.customer_id_var.get().strip()
            start_str = self.start_date_var.get().strip()
            payment = self.monthly_payment_var.get().strip()
            coverage = self.coverage_var.get().strip()
            p_type = self.policy_type_var.get()

            # Basic Validation: Customer ID and Start Date are required for all policies
            if not cust_id or not start_str:
                print("Validation Error: Customer ID and Start Date are required.")
                return

            # Convert the start date string into a datetime object
            start_date = datetime.strptime(start_str, "%Y-%m-%d")

            # Insert into the base Policy table first to generate a new Policy ID
            base_policy = Policy(
                customer_id=cust_id,
                monthly_payment=payment,
                start_date=start_date,
                coverage=coverage
            )
            self.policy_dao.add(base_policy)

            # After adding, we need to retrieve the new policy ID generated by the database. One way is to fetch all policies for this customer and find the max ID.
            customer_policies = self.policy_dao.get_by_customer(int(cust_id))
            if not customer_policies:
                print("Error: Could not retrieve the newly created policy ID.")
                return
            new_policy_id = max(p.policy_id for p in customer_policies)

            # Insert into the specific child table based on the selected policy type
            if p_type == "HOME":
                end_str = self.home_end_date_var.get().strip()
                end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else None

                home_policy = HomeInsurance(
                    policy_id=new_policy_id,
                    end_date=end_date,
                    house_price=self.house_price_var.get().strip() or None,
                    house_area=self.house_area_var.get().strip() or None,
                    bedroom_number=self.bedrooms_var.get().strip() or None,
                    bathroom_number=self.bathrooms_var.get().strip() or None,
                    street=self.home_street_var.get().strip() or None,
                    city=self.home_city_var.get().strip() or None,
                    state=self.home_state_var.get().strip() or None,
                    zip_code=self.home_zip_var.get().strip() or None
                )
                self.home_insurance_dao.add(home_policy)

            elif p_type == "CAR":
                end_str = self.car_end_date_var.get().strip()
                end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else None

                car_policy = CarInsurance(
                    policy_id=new_policy_id,
                    end_date=end_date,
                    make=self.make_var.get().strip() or None,
                    model=self.model_var.get().strip() or None,
                    vin=self.vin_var.get().strip() or None,
                    yearly_mileage=self.mileage_var.get().strip() or None
                )
                self.car_insurance_dao.add(car_policy)

            elif p_type == "LIFE":
                life_policy = LifeInsurance(
                    policy_id=new_policy_id,
                    existing_conditions=self.conditions_var.get().strip() or None,
                    beneficiary=self.beneficiary_var.get().strip() or None
                )
                self.life_insurance_dao.add(life_policy)

            print(f"Success! {p_type} Policy added to Oracle.")
            self.after(500, self.add_policy)  # Small delay to ensure the database has processed the new entries before we refresh
            self.clear_form()

        except Exception as e:
            print(f"Failed to add policy: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def delete_policy(self):
        """
        Deletes the selected policy from the database. It first checks if a policy is selected, then deletes the
        specific child record based on the policy type, and finally deletes the base policy record.
        """
        try:
            # Ensure a policy is actually selected
            if self.selected_policy_index is None:
                print("Action Error: Please select a policy to delete.")
                return

            # Figure out exactly which policy we are clicking on
            index = self.selected_policy_index
            data = self.current_policies_data[index]

            target_policy_id = data["base"].policy_id
            p_type = data["type"]
            details = data["details"]

            # Delete the specific child record first to satisfy Oracle's rules
            if p_type == "HOME" and details:
                self.home_insurance_dao.remove(details.home_id)
            elif p_type == "CAR" and details:
                self.car_insurance_dao.remove(details.car_id)
            elif p_type == "LIFE" and details:
                self.life_insurance_dao.remove(details.life_id)

            # Then delete the base policy record
            self.policy_dao.remove(target_policy_id)
            print(f"Success! Policy ID {target_policy_id} completely deleted from Oracle.")

            # Refresh the list and clear the text boxes
            self.load_policies()
            self.clear_form()

        except Exception as e:
            print(f"Failed to delete policy: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def update_policy(self):
        """
        Updates the selected policy in the database. It first validates the base information, then updates the base
        policy record, and finally updates the specific child record based on the policy type.
        """
        try:
            # Ensure a policy is selected
            if self.selected_policy_index is None:
                print("Action Error: Please select a policy to update.")
                return

            index = self.selected_policy_index
            data = self.current_policies_data[index]

            base_p = data["base"]
            p_type = data["type"]
            details = data["details"]

            # Grab the updated base information from the form
            cust_id = self.customer_id_var.get().strip()
            start_str = self.start_date_var.get().strip()
            payment = self.monthly_payment_var.get().strip()
            coverage = self.coverage_var.get().strip()
            current_type = self.policy_type_var.get()

            # Basic Validation: Customer ID and Start Date are required for all policies
            if not cust_id or not start_str:
                print("Validation Error: Customer ID and Start Date are required.")
                return

            start_date = datetime.strptime(start_str, "%Y-%m-%d")

            # Prevent Type-Swapping (e.g., turning a House into a Car)
            if current_type != p_type:
                print(
                    f"Warning: Cannot change policy type from {p_type} to {current_type}. Please create a new policy instead.")
                return

            # Update the base Policy record first (keeping the same policy_id to ensure we are updating the existing record and not creating a new one
            updated_base = Policy(
                policy_id=base_p.policy_id,  # CRITICAL: Keep original ID
                customer_id=cust_id,
                monthly_payment=payment,
                start_date=start_date,
                coverage=coverage
            )
            self.policy_dao.update(updated_base)

            # Then update the specific child record based on the policy type (also keeping the same ID to ensure we are updating and not creating new records)
            if current_type == "HOME" and details:
                end_str = self.home_end_date_var.get().strip()
                end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else None

                updated_home = HomeInsurance(
                    house_id=details.house_id,  # CRITICAL: Keep original ID
                    policy_id=base_p.policy_id,
                    end_date=end_date,
                    house_price=self.house_price_var.get().strip() or None,
                    house_area=self.house_area_var.get().strip() or None,
                    bedroom_number=self.bedrooms_var.get().strip() or None,
                    bathroom_number=self.bathrooms_var.get().strip() or None,
                    street=self.home_street_var.get().strip() or None,
                    city=self.home_city_var.get().strip() or None
                )
                self.home_insurance_dao.update(updated_home)

            # Updating a Car policy is similar, but with its own specific fields and using the CarInsuranceDAO. Again,
            # we keep the original car_id to ensure we are updating the existing record.
            elif current_type == "CAR" and details:
                end_str = self.car_end_date_var.get().strip()
                end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else None

                updated_car = CarInsurance(
                    car_id=details.car_id,
                    policy_id=base_p.policy_id,
                    end_date=end_date,
                    make=self.make_var.get().strip() or None,
                    model=self.model_var.get().strip() or None,
                    vin=self.vin_var.get().strip() or None,
                    yearly_mileage=self.mileage_var.get().strip() or None
                )
                self.car_insurance_dao.update(updated_car)

            elif current_type == "LIFE" and details:
                updated_life = LifeInsurance(
                    life_id=details.life_id,
                    policy_id=base_p.policy_id,
                    existing_conditions=self.conditions_var.get().strip() or None,
                    beneficiary=self.beneficiary_var.get().strip() or None
                )
                self.life_insurance_dao.update(updated_life)

            print(f"Success! Policy ID {base_p.policy_id} updated in Oracle.")

            # Use our delay trick again to prevent the visual glitch!
            self.after(500, self.load_policies)
            self.clear_form()

        except Exception as e:
            print(f"Failed to update policy: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def search_policies(self):
        """
        Searches for policies based on the query entered in the search box. It first reloads the full list from the
        database, then filters it in memory based on the query, and finally updates the listbox to show only the matching
        results. The search looks for matches in the Policy ID, Customer ID, and Policy Type.
        """
        query = self.policy_search_var.get().strip().lower()

        # Load full fresh list from DB
        self.load_policies()

        if not query:
            return

        # Filter the loaded list
        filtered_data = []
        self.policy_listbox.delete(0, tk.END)

        for data in self.current_policies_data:
            base_p = data["base"]
            p_type = data["type"]

            # Search by Policy ID, Customer ID, or Type (e.g., "HOME")
            if query in str(base_p.policy_id) or query in str(base_p.customer_id) or query in p_type.lower():
                filtered_data.append(data)

                # Reconstruct the display string
                display_text = f"ID {base_p.policy_id}: [{p_type}] Customer {base_p.customer_id} - ${base_p.coverage}"
                self.policy_listbox.insert(tk.END, display_text)

        # Update memory array
        self.current_policies_data = filtered_data
    # ------------------------------------------------------------------------------------------------------------------

    def clear_policy_search(self):
        """Clears the search box and reloads the full list of policies from the database."""
        self.policy_search_var.set("")
        self.load_policies()
    # ------------------------------------------------------------------------------------------------------------------

    def copy_customer_address(self):
        """Fetches the address of the customer ID entered in the top box and pastes it into the Home Insurance fields."""
        try:
            # Grab the Customer ID from the top text box
            cust_id_str = self.customer_id_var.get().strip()

            # Basic validation to ensure they entered something
            if not cust_id_str:
                print("Notice: Please enter a Customer ID first.")
                return

            # Ask the database for this specific customer
            cust_id = int(cust_id_str)
            target_customer = self.customer_dao.find_by_id(cust_id)

            if not target_customer:
                print(f"Notice: Could not find a Customer with ID {cust_id}.")
                return

            # Paste their data into the Home text boxes!
            self.home_street_var.set(target_customer.street or "")
            self.home_city_var.set(target_customer.city or "")
            self.home_state_var.set(target_customer.state or "")
            self.home_zip_var.set(target_customer.zipcode or "")

            print(f"Success! Address copied for Customer {cust_id}.")

        except ValueError:
            print("Notice: Customer ID must be a valid number.")
        except Exception as e:
            print(f"Failed to copy address: {e}")
    # ------------------------------------------------------------------------------------------------------------------

    def clear_form(self):
        """Clears all text boxes and resets the policy type to the default (HOME). Also clears the selection in the listbox."""
        self.customer_id_var.set("")
        self.start_date_var.set("")
        self.monthly_payment_var.set("")
        self.coverage_var.set("")

        # Clear dynamic fields
        self.house_price_var.set("")
        self.house_area_var.set("")
        self.bedrooms_var.set("")
        self.bathrooms_var.set("")
        self.home_end_date_var.set("")
        self.home_street_var.set("")
        self.home_city_var.set("")
        self.home_state_var.set("")
        self.home_zip_var.set("")

        self.make_var.set("")
        self.model_var.set("")
        self.vin_var.set("")
        self.mileage_var.set("")
        self.car_end_date_var.set("")

        self.conditions_var.set("")
        self.beneficiary_var.set("")

        # Clear listbox selection
        self.policy_listbox.selection_clear(0, tk.END)

        # Clear the currently selected policy index
        self.selected_policy_index = None
    # ------------------------------------------------------------------------------------------------------------------

    def update_dynamic_frames(self, *args):
        """Shows the relevant dynamic fields based on the selected policy type and hides the others."""
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
    # ------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
#--- MAIN APPLICATION ---
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
        self.customer_tab.policy_tab = self.policy_tab
        self.customer_tab.notebook = self.notebook
    # ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
# --- Call the main application ---
if __name__ == "__main__":
    app = InsuranceApp()
    app.mainloop()
