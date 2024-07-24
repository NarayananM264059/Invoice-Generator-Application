from flask import Flask, render_template, request
from generate_invoice import generate_invoice

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice_route():
    # Collect form data
    data = {
        "seller": {
            "name": request.form['seller_name'],
            "address": request.form['seller_address'],
            "city_state_pincode": request.form['seller_city_state_pincode'],
            "pan": request.form['seller_pan'],
            "gst": request.form['seller_gst']
        },
        "billing": {
            "name": request.form['billing_name'],
            "address": request.form['billing_address'],
            "city_state_pincode": request.form['billing_city_state_pincode'],
            "state_code": request.form['billing_state_code']
        },
        "shipping": {
            "name": request.form['shipping_name'],
            "address": request.form['shipping_address'],
            "city_state_pincode": request.form['shipping_city_state_pincode'],
            "state_code": request.form['shipping_state_code']
        },
        "order_details": {
            "order_no": request.form['order_no'],
            "order_date": request.form['order_date']
        },
        "invoice_details": {
            "invoice_no": request.form['invoice_no'],
            "invoice_date": request.form['invoice_date']
        },
        "place_of_supply": request.form['place_of_supply'],
        "place_of_delivery": request.form['place_of_delivery'],
        "reverse_charge": request.form['reverse_charge'],
        "items": [
            {
                "description": request.form['item_description'],
                "unit_price": float(request.form['unit_price']),
                "quantity": int(request.form['quantity']),
                "discount": float(request.form.get('discount', 0)),
                "net_amount": float(request.form['unit_price']) * int(request.form['quantity']) - float(request.form.get('discount', 0)),
                "tax_rate": 18,
                "tax_amount": (float(request.form['unit_price']) * int(request.form['quantity']) - float(request.form.get('discount', 0))) * 0.18,
                "total": (float(request.form['unit_price']) * int(request.form['quantity']) - float(request.form.get('discount', 0))) * 1.18
            }
        ],
        "total": (float(request.form['unit_price']) * int(request.form['quantity']) - float(request.form.get('discount', 0))) * 1.18,
        "amount_in_words": "One Thousand One Hundred and Ninety-five rupees only"  # Use a library or function to convert number to words
    }

    generate_invoice(data, "invoice_template.html", "static/invoice.html")

    return "Invoice generated! <a href='/static/invoice.html'>View Invoice</a>"

if __name__ == "__main__":
    app.run(debug=True)
