# Invoice-Generator-Application


## Introduction

This application generates invoices in PDF format using data submitted via a web form. It leverages Flask for the web server, Jinja2 for HTML templating, and `pdfkit` for converting HTML to PDF.

## Installation

**Prerequisites:**

- Python 3.6 or higher
- `pdfkit` and `wkhtmltopdf`
- Flask
- Jinja2
- Inflect

**Installation Steps:**

1. **Clone the repository:**

   ```bash
   git clone [repository_url]
   cd [repository_name]
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install `wkhtmltopdf`:**

   - Follow installation instructions from [wkhtmltopdf official site](https://wkhtmltopdf.org/downloads.html).
   - Ensure `wkhtmltopdf` is in your system's PATH.

## Application Structure

- **app.py**: Main Flask application script.
- **generate_invoice.py**: Contains functions for generating invoices and converting HTML to PDF.
- **templates/**: Directory for Jinja2 HTML templates.
- **static/**: Directory for static files (CSS, images).

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

   This will start a development server at `http://127.0.0.1:5000`.

2. **Access the form:**

   Open your browser and navigate to `http://127.0.0.1:5000/`. Fill out the form with invoice details and submit.

3. **View the generated invoice:**

   After submission, the application will generate an invoice in HTML format and save it to `static/invoice.html`. You can view it by navigating to `http://127.0.0.1:5000/static/invoice.html`.

## Code Overview

- **`app.py`**: Sets up the Flask routes and handles form submissions.
  - **`/`**: Renders the form.
  - **`/generate_invoice`**: Collects form data, generates the invoice using `generate_invoice`, and provides a link to view the generated invoice.

- **`generate_invoice.py`**: Contains functions to generate the invoice HTML and convert it to PDF.
  - **`number_to_words`**: Converts numerical amounts to words.
  - **`calculate_tax`**: Computes tax based on place of supply and delivery.
  - **`generate_invoice`**: Renders the invoice HTML using Jinja2, writes it to a file, and converts it to PDF using `pdfkit`.

- **`templates/invoice_template.html`**: Jinja2 template used to render the invoice HTML.

## Customization

- **Invoice Template**: Modify `templates/invoice_template.html` to change the invoice layout and design.
- **CSS and Images**: Update static files in the `static/` directory to customize the appearance of the invoice.

## Troubleshooting

- **`wkhtmltopdf` not found**: Ensure that `wkhtmltopdf` is installed and in your PATH.
- **HTML to PDF conversion issues**: Check the HTML content for errors and ensure `pdfkit` is correctly configured.

