import pandas as pd
from bs4 import BeautifulSoup

# Path to the local HTML file
file_path = "Amazon1.html"

# Open and read the file
with open(file_path, "r", encoding="utf-8") as file:
    webpage = file.read()

# Parse the HTML
soup = BeautifulSoup(webpage, "html.parser")

# Find all product containers
products = soup.find_all("div", class_="s-result-item")

# List to store product details
product_data = []

# Extract data for each product
for product in products:
    # Extract product ID
    product_id = product.get("data-asin", "N/A")
    
    # Extract product title
    title_tag = product.find("span", class_="a-size-medium")
    title = title_tag.text.strip() if title_tag else "N/A"
    
    # Extract product description (if available)
    description_tag = product.find("span", class_="a-size-base-plus")
    description = description_tag.text.strip() if description_tag else "No description available"
    
    # Combine title and description for a detailed title
    detailed_title = f"{title} - {description}" if title != "N/A" else "N/A"
    
    # Extract product price
    price_whole = product.find("span", class_="a-price-whole")
    price_fraction = product.find("span", class_="a-price-fraction")
    price = f"{price_whole.text.strip()}{price_fraction.text.strip()}" if price_whole and price_fraction else "N/A"
    
    # Extract product rating
    rating_tag = product.find("span", class_="a-icon-alt")
    rating = rating_tag.text.strip() if rating_tag else "N/A"
    
    # Extract additional information
    additional_info = product.find("span", class_="a-size-small")
    additional_details = additional_info.text.strip() if additional_info else "Check each product page for other buying options."

    # Append details to the list
    product_data.append({
        "Product ID": product_id,
        "Title": detailed_title,
        "Price": price,
        "Rating": rating,
        "Additional Details": additional_details
    })

# Convert list of dictionaries to a pandas DataFrame
df = pd.DataFrame(product_data)

# Save DataFrame to an Excel file
output_file = "product_data_with_description.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been saved to {output_file}")
