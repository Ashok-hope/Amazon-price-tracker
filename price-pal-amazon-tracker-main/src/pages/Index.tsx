
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, ShoppingCart, TrendingDown, Zap, Star } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import { useAuthStore } from '@/store/authStore';

const Index = () => {
  const [productUrl, setProductUrl] = useState('');
  const [productData, setProductData] = useState(null);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();
  const { user } = useAuthStore();

  const fetchProductDetails = async () => {
    if (!productUrl.trim()) {
      toast({
        title: "Error",
        description: "Please enter a valid Amazon URL",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/price/fetch-product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amazon_url: productUrl }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch product details');
      }

      const data = await response.json();
      setProductData(data);
      
      toast({
        title: "Success",
        description: "Product details fetched successfully!",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch product details. Please check the URL.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchProductDetails();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Navbar />
      
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Smart Price Tracking for
            <span className="text-blue-600"> Amazon India</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Never miss a deal again! Track your favorite Amazon products and get instant notifications when prices drop to your target range.
          </p>
          
          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
              <div className="bg-blue-100 p-3 rounded-full mb-3">
                <Search className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Smart Tracking</h3>
              <p className="text-sm text-gray-600 text-center">Advanced price monitoring</p>
            </div>
            
            <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
              <div className="bg-green-100 p-3 rounded-full mb-3">
                <TrendingDown className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Price Alerts</h3>
              <p className="text-sm text-gray-600 text-center">Instant email notifications</p>
            </div>
            
            <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
              <div className="bg-yellow-100 p-3 rounded-full mb-3">
                <Zap className="h-6 w-6 text-yellow-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Lightning Fast</h3>
              <p className="text-sm text-gray-600 text-center">Real-time price updates</p>
            </div>
            
            <div className="flex flex-col items-center p-4 bg-white rounded-lg shadow-sm">
              <div className="bg-purple-100 p-3 rounded-full mb-3">
                <Star className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-800">Free Forever</h3>
              <p className="text-sm text-gray-600 text-center">No hidden charges</p>
            </div>
          </div>
        </div>

        {/* URL Input Section */}
        <Card className="max-w-4xl mx-auto mb-8 shadow-lg border-0 bg-white">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2 text-2xl">
              <ShoppingCart className="h-6 w-6 text-blue-600" />
              Track Any Amazon Product
            </CardTitle>
            <p className="text-gray-600">Paste the Amazon product URL below to get started</p>
          </CardHeader>
          <CardContent>
            <div className="flex gap-3 mb-4">
              <Input
                type="url"
                placeholder="https://www.amazon.in/product-name/dp/XXXXXXXXXX"
                value={productUrl}
                onChange={(e) => setProductUrl(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1 h-12 text-lg border-2 border-gray-200 focus:border-blue-500 transition-colors"
              />
              <Button 
                onClick={fetchProductDetails}
                disabled={loading}
                className="h-12 px-8 bg-blue-600 hover:bg-blue-700 text-white font-semibold"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Fetching...
                  </div>
                ) : (
                  <>
                    <Search className="h-4 w-4 mr-2" />
                    Get Details
                  </>
                )}
              </Button>
            </div>
            
            <div className="text-center text-sm text-gray-500">
              <p>✅ Works with all Amazon India products</p>
              <p>✅ Real-time price tracking</p>
              <p>✅ Email notifications when price drops</p>
            </div>
          </CardContent>
        </Card>

        {/* Product Display */}
        {productData && (
          <div className="max-w-4xl mx-auto">
            <ProductCard 
              product={productData} 
              onAddToCart={() => {
                if (!user) {
                  toast({
                    title: "Login Required",
                    description: "Please login to add products to your cart",
                    variant: "destructive",
                  });
                  return;
                }
                // Handle add to cart
              }}
            />
          </div>
        )}

        {/* Stats Section */}
        <div className="mt-16 bg-white rounded-xl p-8 shadow-lg">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Join Thousands of Smart Shoppers</h2>
            <p className="text-gray-600">See why people love our price tracking service</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">50K+</div>
              <div className="text-gray-600">Products Tracked</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">₹2.5L+</div>
              <div className="text-gray-600">Money Saved</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">10K+</div>
              <div className="text-gray-600">Happy Users</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
