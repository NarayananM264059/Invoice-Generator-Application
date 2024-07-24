from jinja2 import Environment, FileSystemLoader
import inflect
import pdfkit
import os


def number_to_words(number):
    p = inflect.engine()
    return p.number_to_words(number).replace(", and", " and").replace(", ", " ")

def calculate_tax(net_amount, place_of_supply, place_of_delivery):
    if place_of_supply == place_of_delivery:
        cgst = sgst = 0.09 * net_amount
        igst = 0
        tax_type = "CGST & SGST"
    else:
        cgst = sgst = 0
        igst = 0.18 * net_amount
        tax_type = "IGST"
    return cgst, sgst, igst, tax_type

def generate_invoice(data, template_path, output_path):
    # Load template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_path)
    
    # Process data
    seller = data.get("seller", {})
    billing = data.get("billing", {})
    shipping = data.get("shipping", {})
    order_details = data.get("order_details", {})
    invoice_details = data.get("invoice_details", {})
    
    items = data.get("items", [])
    
    # Prepare items HTML
    items_html = ""
    total_amount = 0
    for i, item in enumerate(items, start=1):
        net_amount = item['unit_price'] * item['quantity'] - item['discount']
        cgst, sgst, igst, tax_type = calculate_tax(net_amount, data['place_of_supply'], data['place_of_delivery'])
        tax_amount = cgst + sgst + igst
        total = net_amount + tax_amount
        items_html += f"""
        <tr>
            <td>{i}</td>
            <td>{item['description']}</td>
            <td>₹{item['unit_price']:.2f}</td>
            <td>{item['quantity']}</td>
            <td>₹{item['discount']:.2f}</td>
            <td>₹{net_amount:.2f}</td>
            <td>{tax_type} ({item['tax_rate']}%)</td>
            <td>₹{cgst:.2f} + ₹{sgst:.2f} + ₹{igst:.2f}</td>
            <td>₹{total:.2f}</td>
        </tr>
        """
        total_amount += total
    
    amount_in_words = number_to_words(total_amount)
    
    # Render template
    html_content = template.render(
        seller_name=seller.get("name", ""),
        seller_address=seller.get("address", ""),
        seller_city=seller.get("city_state_pincode", ""),
        seller_pan=seller.get("pan", ""),
        seller_gst=seller.get("gst", ""),
        billing_name=billing.get("name", ""),
        billing_address=billing.get("address", ""),
        billing_city=billing.get("city_state_pincode", ""),
        billing_state_code=billing.get("state_code", ""),
        shipping_name=shipping.get("name", ""),
        shipping_address=shipping.get("address", ""),
        shipping_city=shipping.get("city_state_pincode", ""),
        shipping_state_code=shipping.get("state_code", ""),
        order_no=order_details.get("order_no", ""),
        order_date=order_details.get("order_date", ""),
        invoice_no=invoice_details.get("invoice_no", ""),
        invoice_date=invoice_details.get("invoice_date", ""),
        place_of_supply=data.get("place_of_supply", ""),
        place_of_delivery=data.get("place_of_delivery", ""),
        reverse_charge=data.get("reverse_charge", ""),
        items_body=items_html,
        total=f"₹{total_amount:.2f}",
        amount_in_words=f"{amount_in_words} Rupees only"
    )

    # Write to output file
    with open(output_path, "w",encoding="utf-8") as file:
        file.write(html_content)
    
    # Convert HTML content to PDF
    #pdfkit.from_file(output_path, output_path.replace(".html", ".pdf"))