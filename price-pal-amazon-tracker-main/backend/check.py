import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from pydantic import BaseModel
import re


class ProductResponse(BaseModel):
    product_name: str
    current_price: float
    image_url: str
    asin: str
    amazon_url: str
    availability: str


class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def extract_asin(self, url: str) -> str:
        """Extract ASIN from Amazon URL"""
        match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
        if match:
            return match.group(1)
        raise ValueError("ASIN not found in URL")

    def scrape_product(self, url: str) -> ProductResponse:
        """Scrape product details from Amazon"""
        try:
            asin = self.extract_asin(url)
            clean_url = f"https://www.amazon.in/dp/{asin}"
            response = requests.get(clean_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Product Title
            title_selectors = [
                '#productTitle',
                '.product-title',
                '[data-automation-id="product-title"]'
            ]
            product_name = "Product Name Not Found"
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    product_name = title_elem.get_text().strip()
                    break

            # Price
            price_selectors = [
                '.a-price-whole',
                '.a-offscreen',
                '.a-price .a-offscreen',
                '[data-automation-id="price"]',
                '.a-price-range .a-offscreen'
            ]
            current_price = 0.0
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if price_match:
                        current_price = float(price_match.group())
                        break

            # Image
            image_selectors = [
                '#landingImage',
                '.a-dynamic-image',
                '[data-automation-id="product-image"]'
            ]
            image_url = ""
            for selector in image_selectors:
                img_elem = soup.select_one(selector)
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src', '')
                    if image_url:
                        break

            # Availability
            availability = "In Stock"
            availability_elem = soup.select_one('#availability span')
            if availability_elem:
                availability_text = availability_elem.get_text().strip()
                if "out of stock" in availability_text.lower():
                    availability = "Out of Stock"

            return ProductResponse(
                product_name=product_name,
                current_price=current_price,
                image_url=image_url or "",
                asin=asin,
                amazon_url=clean_url,
                availability=availability
            )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error scraping product: {str(e)}"
            )


# Sample usage
if __name__ == "__main__":
    scraper = AmazonScraper()
    test_url = input("Enter Amazon product URL: ")

    try:
        result = scraper.scrape_product(test_url)
        print("\nProduct Details:")
        print(f"Name: {result.product_name}")
        print(f"Price: ₹{result.current_price}")
        print(f"Image URL: {result.image_url}")
        print(f"ASIN: {result.asin}")
        print(f"Amazon URL: {result.amazon_url}")
        print(f"Availability: {result.availability}")
    except HTTPException as e:
        print(f"Failed to fetch product details: {e.detail}")
