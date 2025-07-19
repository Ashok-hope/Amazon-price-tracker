
import { useState } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { ShoppingCart, ExternalLink, Target, TrendingDown } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuthStore } from '@/store/authStore';

const ProductCard = ({ product, onAddToCart }) => {
  const [targetPrice, setTargetPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();
  const { user, token } = useAuthStore();

  const handleAddToCart = async () => {
    if (!user) {
      toast({
        title: "Login Required",
        description: "Please login to add products to your cart",
        variant: "destructive",
      });
      return;
    }

    if (!targetPrice || parseFloat(targetPrice) <= 0) {
      toast({
        title: "Invalid Target Price",
        description: "Please enter a valid target price",
        variant: "destructive",
      });
      return;
    }

    if (parseFloat(targetPrice) >= product.current_price) {
      toast({
        title: "Target Price Too High",
        description: "Target price should be lower than current price",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/price/add-to-cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          amazon_url: product.amazon_url,
          target_price: parseFloat(targetPrice),
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
      }

      // Send tracking started email after successful add-to-cart
      try {
        await fetch("http://localhost:8000/auth/send-tracking-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: user.email,
            name: user.name,
            product_name: product.product_name,
            current_price: product.current_price,
            target_price: parseFloat(targetPrice),
            image_url: product.image_url,
            amazon_url: product.amazon_url,
          }),
        });
      } catch (err) {
        console.error("Failed to send tracking started email:", err);
      }

      toast({
        title: "Success",
        description: "Product added to cart! You'll be notified when price drops.",
      });
      
      setTargetPrice('');
      if (onAddToCart) onAddToCart();
      
    } catch (error) {
      toast({
        title: "Error",
        description: error.message || "Failed to add product to cart",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto shadow-lg border-0 bg-white">
      <CardHeader>
        <div className="flex items-center justify-between mb-4">
          <Badge variant="secondary" className="bg-green-100 text-green-800">
            {product.availability}
          </Badge>
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.open(product.amazon_url, '_blank')}
            className="flex items-center gap-2"
          >
            <ExternalLink className="h-4 w-4" />
            View on Amazon
          </Button>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="flex justify-center">
            <div className="w-full max-w-md">
              <img
                src={product.image_url || '/placeholder.svg'}
                alt={product.product_name}
                className="w-full h-auto rounded-lg shadow-md"
                onError={(e) => {
                  e.target.src = '/placeholder.svg';
                }}
              />
            </div>
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                {product.product_name}
              </h2>
              <p className="text-sm text-gray-600 mb-4">ASIN: {product.asin}</p>
            </div>

            {/* Price Section */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingDown className="h-5 w-5 text-blue-600" />
                <span className="text-lg font-semibold text-gray-700">Current Price</span>
              </div>
              <div className="text-4xl font-bold text-blue-600 mb-4">
                ₹{product.current_price.toLocaleString('en-IN')}
              </div>
              
              {/* Target Price Input */}
              <div className="space-y-4">
                <div>
                  <Label htmlFor="target-price" className="flex items-center gap-2 text-sm font-medium">
                    <Target className="h-4 w-4" />
                    Set Your Target Price
                  </Label>
                  <div className="flex gap-3 mt-2">
                    <div className="flex-1">
                      <Input
                        id="target-price"
                        type="number"
                        placeholder="Enter target price"
                        value={targetPrice}
                        onChange={(e) => setTargetPrice(e.target.value)}
                        className="h-12 text-lg"
                        min="1"
                        max={product.current_price - 1}
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Should be less than current price
                      </p>
                    </div>
                    <Button
                      onClick={handleAddToCart}
                      disabled={loading || !user}
                      className="h-12 px-6 bg-orange-500 hover:bg-orange-600 text-white font-semibold"
                    >
                      {loading ? (
                        <div className="flex items-center gap-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                          Adding...
                        </div>
                      ) : (
                        <>
                          <ShoppingCart className="h-4 w-4 mr-2" />
                          Track Price
                        </>
                      )}
                    </Button>
                  </div>
                </div>
                
                {!user && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                    <p className="text-sm text-yellow-800">
                      <strong>Login required:</strong> Sign in to track this product and get price alerts.
                    </p>
                  </div>
                )}
                
                {targetPrice && parseFloat(targetPrice) > 0 && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                    <p className="text-sm text-green-800">
                      <strong>Savings:</strong> You'll save ₹{(product.current_price - parseFloat(targetPrice)).toLocaleString('en-IN')} when price drops to your target!
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Features */}
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="font-semibold text-gray-800">✅ Real-time Tracking</div>
                <div className="text-sm text-gray-600">Updated 3x daily</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="font-semibold text-gray-800">📧 Email Alerts</div>
                <div className="text-sm text-gray-600">Instant notifications</div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
