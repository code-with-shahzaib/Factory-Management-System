# 🏭 Factory Management Software

**Factory Management Software** is a Python-based desktop application designed to streamline the management of orders, invoices, and customer interactions for small factories and design studios. Built with simplicity and functionality in mind, it enables efficient billing and documentation with a professional touch.

## 📦 Features

* *   ✅ Easy-to-use GUI for managing clients and orders
* *   🧾 Dynamic invoice generation using Jinja2 and WeasyPrint
* *   📄 Export invoices to high-quality PDF format
* *   🖼 Custom invoice template with company branding and logo
* *   🗂 Organized folder structure with support for reusable templates
* *   💡 Ideal for small manufacturers, art studios, and design houses    

## 🖥 Technologies Used

* *   **Python 3.x**
* *   **Tkinter** – for GUI development
* *   **Jinja2** – for rendering dynamic HTML templates
* *   **WeasyPrint** – for generating PDFs from HTML/CSS
* *   **SQLite3** – for lightweight local database storage

## 📁 Project Structure
Factory Management Software/│                                   
         ├── main.py                                             
         ├── database.py                                       
         ├── invoice_templates/ │                            
                  └── template.html                              
         ├── images/ │                                   
                  └── logo.png     

## 📸 Sample Invoice Layout

Invoices are styled professionally and include:

* *   Company branding and contact information
* *   Client billing details
* *   Order information with description, price, quantity
* *   Automatically calculated tax, discount, and total
* *   Footer with payment terms

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

* *   Python 3.x
* *   pip (Python package installer)

### Installation

1. 1.  Clone this repository:

`git clone git@github.com:code-with-shahzaib/Factory-Management-System.git 
 cd factory-management-software`

1. 2.  Install dependencies:
`pip install jinja2 weasyprint`

> **Note:** On some systems, WeasyPrint may require additional system packages like `libpango`, `libcairo`, and `gdk-pixbuf`. Refer to the [WeasyPrint installation guide](https://weasyprint.readthedocs.io/en/latest/install.html) for details.

### Usage

Run the application:
`python main.py`

Follow the GUI to input client and order information. The software will generate and save a PDF invoice using the provided template.

## 📌 Customization

* *   Modify `invoice_templates/template.html` to adjust the layout or branding of invoices.
* *   Replace `images/logo.png` with your own company logo.
* *   Extend functionality in `main.py` or `database.py` to suit your factory's specific workflows.

## 🛠 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue first to discuss the proposal.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

* * *

**Crafted with ❤️ by Muhammad Shahzaib for Premax Arts & Designs.**
