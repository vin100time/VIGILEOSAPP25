import { Card } from "@/components/ui/card";
import { AlertCircleIcon, CheckCircleIcon, XCircleIcon, UserIcon, LogOut } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Alerts = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleLogout = async () => {
    try {
      logout();
      toast({
        title: "Déconnexion réussie",
        description: "À bientôt !",
      });
      navigate('/');
    } catch (error: any) {
      console.error("Erreur lors de la déconnexion:", error);
      toast({
        title: "Erreur",
        description: "Un problème est survenu lors de la déconnexion.",
        variant: "destructive",
      });
    }
  };

  const alerts = [
    {
      id: 1,
      title: "Serveur principal inaccessible",
      description: "Le serveur ne répond plus depuis 5 minutes",
      type: "error",
      timestamp: new Date().toLocaleString(),
      source: "Serveur principal"
    },
    {
      id: 2,
      title: "Trafic réseau anormal",
      description: "Pic de trafic détecté sur le switch principal",
      type: "warning",
      timestamp: new Date().toLocaleString(),
      source: "Switch principal"
    },
    {
      id: 3,
      title: "Connexion rétablie",
      description: "La connexion avec l'imprimante RH a été rétablie",
      type: "success",
      timestamp: new Date().toLocaleString(),
      source: "Imprimante RH"
    }
  ];

  const getIcon = (type: string) => {
    switch(type) {
      case 'error':
        return <XCircleIcon className="w-6 h-6 text-danger" />;
      case 'warning':
        return <AlertCircleIcon className="w-6 h-6 text-warning" />;
      case 'success':
        return <CheckCircleIcon className="w-6 h-6 text-success" />;
      default:
        return <AlertCircleIcon className="w-6 h-6" />;
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Alertes</h1>
          <p className="text-muted-foreground">
            Suivi des alertes et notifications
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm">Global Secure SARL</span>
          <DropdownMenu>
            <DropdownMenuTrigger className="focus:outline-none">
              <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center hover:bg-secondary/80 transition-colors">
                <UserIcon className="w-4 h-4 text-muted-foreground" />
              </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleLogout} className="text-red-600 focus:text-red-600 focus:bg-red-50">
                <LogOut className="w-4 h-4 mr-2" />
                Se déconnecter
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      <div className="grid gap-4">
        {alerts.map((alert) => (
          <Card key={alert.id} className="p-4 glass card-hover">
            <div className="flex items-center gap-4">
              {getIcon(alert.type)}
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold">{alert.title}</h3>
                  <span className="text-sm text-muted-foreground">{alert.timestamp}</span>
                </div>
                <p className="text-sm text-muted-foreground">{alert.description}</p>
                <p className="text-xs text-muted-foreground mt-1">Source: {alert.source}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Alerts;
