import tkinter as tk
from database import initialize_database
from gui import FactoryManagementGUI

def main():
    # Initialize database
    initialize_database()
    
    # Create main window
    root = tk.Tk()
    app = FactoryManagementGUI(root)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()