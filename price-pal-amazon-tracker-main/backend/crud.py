
from fastapi import APIRouter, HTTPException, Depends
from auth import get_current_user
from firebase_config import firebase_service
from models import UserUpdate
from typing import List

router = APIRouter()

@router.get("/user/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "uid": current_user["uid"],
        "name": current_user["name"],
        "email": current_user["email"],
        "created_at": current_user.get("created_at")
    }

@router.put("/user/profile")
async def update_user_profile(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        # Get user document
        users = firebase_service.query_documents("users", "uid", "==", current_user["uid"])
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_doc = users[0]
        
        # Update data
        update_data = {}
        if user_data.name:
            update_data["name"] = user_data.name
        if user_data.email:
            update_data["email"] = user_data.email
        
        # Update in Firestore
        firebase_service.update_document("users", user_doc["id"], update_data)
        
        return {"message": "Profile updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/cart")
async def get_user_cart(current_user: dict = Depends(get_current_user)):
    try:
        products = firebase_service.query_documents("products", "user_id", "==", current_user["uid"])
        return {
            "products": products,
            "total_products": len(products),
            "active_products": len([p for p in products if p.get("is_active", True)])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/user/cart/{product_id}")
async def remove_from_cart(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove product from cart"""
    try:
        # Get product
        product = firebase_service.get_document("products", product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Check if product belongs to current user
        if product["user_id"] != current_user["uid"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Delete product
        firebase_service.delete_document("products", product_id)
        
        return {"message": "Product removed from cart"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    try:
        products = firebase_service.query_documents("products", "user_id", "==", current_user["uid"])
        
        active_products = [p for p in products if p.get("is_active", True)]
        total_savings = sum(
            p["lowest_price"] - p["target_price"] 
            for p in products 
            if p["lowest_price"] <= p["target_price"]
        )
        
        return {
            "total_products": len(products),
            "active_products": len(active_products),
            "completed_alerts": len(products) - len(active_products),
            "total_savings": max(0, total_savings)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
