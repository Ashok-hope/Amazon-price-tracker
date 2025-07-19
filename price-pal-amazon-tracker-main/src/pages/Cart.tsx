
import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Trash2, ExternalLink, TrendingDown, TrendingUp, Target } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { useToast } from '@/hooks/use-toast';
import Navbar from '@/components/Navbar';

const Cart = () => {
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user, token, isAuthenticated } = useAuthStore();
  const { toast } = useToast();

  useEffect(() => {
    if (isAuthenticated) {
      fetchCartData();
    }
  }, [isAuthenticated]);

  const fetchCartData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/user/cart', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch cart data');
      }

      const data = await response.json();
      setCartData(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch cart data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (productId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/user/cart/${productId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to remove product');
      }

      toast({
        title: "Success",
        description: "Product removed from cart",
      });

      fetchCartData();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to remove product",
        variant: "destructive",
      });
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="container mx-auto px-4 py-16 text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Please Login</h1>
          <p className="text-gray-600">You need to login to view your cart.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="container mx-auto px-4 py-16">
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">My Price Tracker</h1>
          <p className="text-gray-600">Monitor your favorite products and never miss a deal!</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-blue-50 border-blue-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-600 text-sm font-medium">Total Products</p>
                  <p className="text-2xl font-bold text-blue-800">
                    {cartData?.total_products || 0}
                  </p>
                </div>
                <div className="bg-blue-100 p-3 rounded-full">
                  <Target className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-green-50 border-green-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-600 text-sm font-medium">Active Tracking</p>
                  <p className="text-2xl font-bold text-green-800">
                    {cartData?.active_products || 0}
                  </p>
                </div>
                <div className="bg-green-100 p-3 rounded-full">
                  <TrendingDown className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-purple-50 border-purple-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-600 text-sm font-medium">Completed Alerts</p>
                  <p className="text-2xl font-bold text-purple-800">
                    {(cartData?.total_products || 0) - (cartData?.active_products || 0)}
                  </p>
                </div>
                <div className="bg-purple-100 p-3 rounded-full">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Products List */}
        {cartData?.products?.length > 0 ? (
          <div className="space-y-6">
            {cartData.products.map((product) => (
              <Card key={product.id} className="overflow-hidden">
                <CardContent className="p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {/* Product Image */}
                    <div className="lg:col-span-1">
                      <img
                        src={product.image_url || '/placeholder.svg'}
                        alt={product.product_name}
                        className="w-full h-48 object-cover rounded-lg"
                        onError={(e) => {
                          e.target.src = '/placeholder.svg';
                        }}
                      />
                    </div>

                    {/* Product Details */}
                    <div className="lg:col-span-2">
                      <div className="flex items-start justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">
                          {product.product_name}
                        </h3>
                        <Badge 
                          variant={product.is_active ? "default" : "secondary"}
                          className={product.is_active ? "bg-green-100 text-green-800" : ""}
                        >
                          {product.is_active ? "Tracking" : "Completed"}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-600">Current Price</p>
                          <p className="text-lg font-bold text-gray-800">
                            ₹{product.current_price.toLocaleString('en-IN')}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Target Price</p>
                          <p className="text-lg font-bold text-blue-600">
                            ₹{product.target_price.toLocaleString('en-IN')}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Lowest Price</p>
                          <p className="text-lg font-bold text-green-600">
                            ₹{product.lowest_price.toLocaleString('en-IN')}
                          </p>
                        </div>
                      </div>

                      <div className="text-sm text-gray-600">
                        <p>Added: {new Date(product.created_at).toLocaleDateString()}</p>
                        <p>ASIN: {product.asin}</p>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="lg:col-span-1 flex flex-col gap-3">
                      <Button
                        variant="outline"
                        onClick={() => window.open(product.amazon_url, '_blank')}
                        className="w-full"
                      >
                        <ExternalLink className="h-4 w-4 mr-2" />
                        View on Amazon
                      </Button>
                      
                      <Button
                        variant="destructive"
                        onClick={() => removeFromCart(product.id)}
                        className="w-full"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Remove
                      </Button>

                      {product.current_price <= product.target_price && (
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                          <p className="text-sm text-green-800 font-medium">
                            🎉 Target price reached!
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="text-center py-16">
            <CardContent>
              <div className="max-w-md mx-auto">
                <div className="bg-gray-100 rounded-full p-8 mb-6 w-32 h-32 mx-auto flex items-center justify-center">
                  <Target className="h-16 w-16 text-gray-400" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">No Products Tracked</h2>
                <p className="text-gray-600 mb-6">
                  Start tracking your favorite Amazon products to never miss a deal again!
                </p>
                <Button 
                  onClick={() => window.location.href = '/'}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Start Tracking Products
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Cart;
