class Contact:
    def __init__(self, store_name, phone, email, address):
        self.store_name = store_name
        self.phone = phone
        self.email = email
        self.address = address

class ContactManager:
    def __init__(self):
        self.contacts = []
    
    def add_contact(self, contact):
        self.contacts.append(contact)
        print(f"\nContact for {contact.store_name} added successfully!")
    
    def view_contact_list(self):
        print("\n--- Contact List ---")
        if not self.contacts:
            print("No contacts available.")
            return
        
        for idx, contact in enumerate(self.contacts, 1):
            print(f"{idx}. {contact.store_name}: {contact.phone}")
    
    def search_contact(self, search_term):
        results = []
        for contact in self.contacts:
            if (search_term.lower() in contact.store_name.lower() or 
                search_term in contact.phone):
                results.append(contact)
        
        if not results:
            print("\nNo matching contacts found.")
            return
        
        print("\n--- Search Results ---")
        for contact in results:
            self.display_contact_details(contact)
    
    def update_contact(self, index, updated_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = updated_contact
            print("\nContact updated successfully!")
        else:
            print("\nInvalid contact index.")
    
    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            deleted_name = self.contacts[index].store_name
            del self.contacts[index]
            print(f"\nContact for {deleted_name} deleted successfully!")
        else:
            print("\nInvalid contact index.")
    
    def display_contact_details(self, contact):
        print(f"\nStore Name: {contact.store_name}")
        print(f"Phone: {contact.phone}")
        print(f"Email: {contact.email}")
        print(f"Address: {contact.address}")

def get_contact_input():
    store_name = input("Enter store name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    address = input("Enter address: ").strip()
    
    if not store_name or not phone:
        print("Store name and phone number are required!")
        return None
    
    return Contact(store_name, phone, email, address)

def main():
    manager = ContactManager()
    
    while True:
        print("\n--- Contact Management System ---")
        print("1. Add New Contact")
        print("2. View Contact List")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            print("\n--- Add New Contact ---")
            contact = get_contact_input()
            if contact:
                manager.add_contact(contact)
        
        elif choice == '2':
            manager.view_contact_list()
            if manager.contacts:
                view_details = input("\nEnter contact number to view details (or 0 to go back): ")
                if view_details.isdigit():
                    idx = int(view_details) - 1
                    if 0 <= idx < len(manager.contacts):
                        manager.display_contact_details(manager.contacts[idx])
        
        elif choice == '3':
            print("\n--- Search Contact ---")
            search_term = input("Enter name or phone number to search: ").strip()
            if search_term:
                manager.search_contact(search_term)
        
        elif choice == '4':
            manager.view_contact_list()
            if manager.contacts:
                contact_num = input("\nEnter contact number to update (or 0 to go back): ")
                if contact_num.isdigit():
                    idx = int(contact_num) - 1
                    if 0 <= idx < len(manager.contacts):
                        print("\nEnter new details:")
                        updated_contact = get_contact_input()
                        if updated_contact:
                            manager.update_contact(idx, updated_contact)
        
        elif choice == '5':
            manager.view_contact_list()
            if manager.contacts:
                contact_num = input("\nEnter contact number to delete (or 0 to go back): ")
                if contact_num.isdigit():
                    idx = int(contact_num) - 1
                    if 0 <= idx < len(manager.contacts):
                        manager.delete_contact(idx)
        
        elif choice == '6':
            print("\nExiting Contact Management System. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()