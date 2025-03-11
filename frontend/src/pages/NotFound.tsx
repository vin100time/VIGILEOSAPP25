
import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: Page non trouvée:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] animate-fade-in">
      <div className="text-center space-y-6 max-w-lg mx-auto p-6">
        <h1 className="text-7xl font-bold text-[#0e3175]">404</h1>
        <h2 className="text-2xl font-semibold text-gray-900">Page non trouvée</h2>
        <p className="text-gray-600 mt-2">
          Désolé, la page que vous recherchez n'existe pas ou a été déplacée.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
          <Button 
            variant="default" 
            className="bg-[#0e3175] hover:bg-[#0e3175]/90"
            asChild
          >
            <Link to="/dashboard">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour au tableau de bord
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
