
from fastapi import APIRouter, HTTPException, Depends
import requests
from bs4 import BeautifulSoup
import re
from models import ProductCreate, ProductResponse
from auth import get_current_user
from firebase_config import firebase_service
from datetime import datetime
import json

router = APIRouter()

class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    
    def extract_asin(self, url: str) -> str:
        """Extract ASIN from Amazon URL"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("Could not extract ASIN from URL")
    
    def scrape_product(self, url: str) -> ProductResponse:
        """Scrape product details from Amazon"""
        try:
            asin = self.extract_asin(url)
            
            # Clean URL
            clean_url = f"https://www.amazon.in/dp/{asin}"
            
            response = requests.get(clean_url, headers=self.headers, timeout=10)
            print("Status code:", response.status_code)
            print("First 1000 chars of HTML:\n", response.content[:1000])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
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
            
            # Extract price
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
                    # Extract numeric value
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if price_match:
                        current_price = float(price_match.group())
                        break
            
            # Extract image URL
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
            
            # Check availability
            availability = "In Stock"
            availability_elem = soup.select_one('#availability span')
            if availability_elem:
                availability_text = availability_elem.get_text().strip()
                if "out of stock" in availability_text.lower():
                    availability = "Out of Stock"
            
            return ProductResponse(
                product_name=product_name,
                current_price=current_price,
                image_url=str(image_url or ""),
                asin=asin,
                amazon_url=clean_url,
                availability=availability
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error scraping product: {str(e)}"
            )

scraper = AmazonScraper()

@router.post("/fetch-product", response_model=ProductResponse)
async def fetch_product_details(product_data: dict):
    """Fetch product details without authentication"""
    amazon_url = product_data.get("amazon_url")
    if not amazon_url:
        raise HTTPException(
            status_code=400,
            detail="Amazon URL is required"
        )
    
    return scraper.scrape_product(amazon_url)

@router.post("/add-to-cart", response_model=dict)
async def add_product_to_cart(
    product_data: ProductCreate,
    current_user: dict = Depends(get_current_user)
):
    """Add product to user's cart for price tracking"""
    try:
        # Scrape current product details
        product_details = scraper.scrape_product(product_data.amazon_url)
        
        # Check if product already exists for this user
        existing_products = firebase_service.query_documents(
            "products", "user_id", "==", current_user["uid"]
        )
        
        for product in existing_products:
            if product.get("asin") == product_details.asin:
                raise HTTPException(
                    status_code=400,
                    detail="Product already in your cart"
                )
        
        # Create product document
        product_doc = {
            "user_id": current_user["uid"],
            "amazon_url": product_details.amazon_url,
            "product_name": product_details.product_name,
            "current_price": product_details.current_price,
            "target_price": product_data.target_price,
            "lowest_price": product_details.current_price,
            "image_url": product_details.image_url,
            "asin": product_details.asin,
            "created_at": datetime.now(),
            "is_active": True
        }
        
        product_id = firebase_service.add_document("products", product_doc)

        # Send tracking started email to user
        users = firebase_service.query_documents("users", "uid", "==", current_user["uid"])
        if users:
            user = users[0]
            from email_service import send_tracking_started_email
            try:
                result = await send_tracking_started_email(
                    user["email"],
                    user["name"],
                    product_details.product_name,
                    product_details.current_price,
                    product_data.target_price,
                    product_details.image_url,
                    product_details.amazon_url
                )
                print(f"Tracking started email sent: {result}")
            except Exception as e:
                print(f"Failed to send tracking started email: {e}")
        else:
            print("No user found in users collection for tracking email.")

        return {
            "message": "Product added to cart successfully",
            "product_id": product_id,
            "product": product_doc
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

class PriceChecker:
    def __init__(self):
        self.scraper = AmazonScraper()
    
    async def check_all_products(self):
        """Check prices for all active products"""
        try:
            # Get all active products
            products = firebase_service.query_documents("products", "is_active", "==", True)
            
            for product in products:
                await self.check_single_product(product)
                
        except Exception as e:
            print(f"Error checking prices: {e}")
    
    async def check_single_product(self, product: dict):
        """Check price for a single product"""
        try:
            # Scrape current price
            current_details = self.scraper.scrape_product(product["amazon_url"])
            current_price = current_details.current_price
            
            # Update current price and lowest price
            update_data = {"current_price": current_price}
            
            if current_price < product["lowest_price"]:
                update_data["lowest_price"] = current_price
            
            firebase_service.update_document("products", product["id"], update_data)
            
            # Check if price dropped to target
            if current_price <= product["target_price"]:
                await self.trigger_price_alert(product, current_price)
                
        except Exception as e:
            print(f"Error checking product {product['id']}: {e}")
    
    async def trigger_price_alert(self, product: dict, current_price: float):
        """Trigger price alert and send email"""
        try:
            from email_service import send_price_alert_email
            
            # Get user details
            users = firebase_service.query_documents("users", "uid", "==", product["user_id"])
            if not users:
                return
            
            user = users[0]
            
            # Send price alert email
            await send_price_alert_email(
                user["email"],
                user["name"],
                product["product_name"],
                current_price,
                product["target_price"],
                product["lowest_price"],
                product["image_url"],
                product["amazon_url"]
            )
            
            # Deactivate product and send thank you email
            firebase_service.update_document("products", product["id"], {"is_active": False})
            
            from email_service import send_thank_you_email
            await send_thank_you_email(user["email"], user["name"], product["product_name"])
            
        except Exception as e:
            print(f"Error triggering price alert: {e}")

price_checker = PriceChecker()
