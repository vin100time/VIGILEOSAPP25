
import { Card } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { cn } from "@/lib/utils";
import SitesMap from "@/components/SitesMap";
import { UserIcon, LogOut } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Index = () => {
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

  const equipmentData = [
    { name: 'Caméras', value: 35, color: '#2196F3' },
    { name: 'Routeurs', value: 15, color: '#FFA726' },
    { name: 'Switches', value: 20, color: '#7E69AB' },
    { name: 'Serveurs', value: 10, color: '#78909C' },
    { name: 'Points d\'accès', value: 10, color: '#66BB6A' },
    { name: 'Autres', value: 10, color: '#8E9196' }
  ];

  const stats = [
    { 
      label: "Total des sites", 
      value: "12",
      subtext: "Sites surveillés",
      textColor: "#1A1F2C",
      delay: "0ms"
    },
    { 
      label: "En ligne", 
      value: "10", 
      subtext: "Sites actifs",
      textColor: "#4CAF50",
      delay: "100ms"
    },
    { 
      label: "Hors ligne", 
      value: "1", 
      subtext: "Sites inactifs",
      textColor: "#F44336",
      delay: "200ms"
    },
    { 
      label: "Alertes", 
      value: "6", 
      subtext: "Dernières 24h",
      textColor: "#FF9800",
      delay: "300ms"
    },
    { 
      label: "Disponibilité", 
      value: "99.4%", 
      subtext: "Temps de service",
      textColor: "#1A1F2C",
      delay: "400ms"
    }
  ];

  const alerts = [
    {
      title: "Perte de connexion - Site Marseille Port",
      time: "2024-03-13 10:30",
      status: "Nouveau",
      type: "error"
    },
    {
      title: "Utilisation CPU élevée - Serveur SV-01",
      time: "2024-03-13 10:25",
      status: "En cours",
      type: "warning"
    },
    {
      title: "Échec de la sauvegarde - Caméra IP-02",
      time: "2024-03-13 10:20",
      status: "Résolu",
      type: "success"
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Tableau de bord</h1>
          <p className="text-sm text-muted-foreground">
            Dernière mise à jour : 5 février 2025 à 15:14
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

      <div className="grid grid-cols-5 gap-4">
        {stats.map((stat) => (
          <Card 
            key={stat.label} 
            className="p-4 bg-white transform hover:scale-105 transition-all duration-300 animate-fade-in cursor-pointer"
            style={{ animationDelay: stat.delay }}
          >
            <p className="text-sm text-muted-foreground">{stat.label}</p>
            <p 
              className="text-2xl font-bold mt-2 animate-[counter_2s_ease-out_1] transform hover:translate-y-[-2px] transition-transform" 
              style={{ color: stat.textColor }}
            >
              {stat.value}
            </p>
            <p className="text-xs text-muted-foreground mt-1">{stat.subtext}</p>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Card className="p-4 bg-white">
          <h2 className="text-lg font-semibold mb-4">Répartition géographique des sites</h2>
          <SitesMap />
        </Card>

        <Card className="p-4 bg-white">
          <h2 className="text-lg font-semibold mb-4">Répartition des équipements</h2>
          <div style={{ width: '100%', height: '400px' }}>
            <ResponsiveContainer>
              <BarChart
                data={equipmentData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 60
                }}
              >
                <XAxis 
                  dataKey="name"
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  interval={0}
                />
                <YAxis />
                <Tooltip />
                <Bar 
                  dataKey="value" 
                  fill="#2196F3"
                  label={{ 
                    position: 'top',
                    content: ({ value }) => `${value}%`
                  }}
                >
                  {equipmentData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.color}
                      className="transition-all duration-300 hover:opacity-80"
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card className="p-4 bg-white">
        <h2 className="text-lg font-semibold mb-4">Dernières alertes</h2>
        <div className="space-y-2">
          {alerts.map((alert, index) => (
            <div
              key={index}
              className="p-3 rounded-lg transform hover:scale-[1.02] transition-all duration-300"
              style={{
                backgroundColor: alert.type === 'error' ? '#FEF2F2' : 
                                alert.type === 'warning' ? '#FEF3C7' : 
                                '#F0FDF4'
              }}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">{alert.title}</p>
                  <p className="text-sm text-muted-foreground">{alert.time}</p>
                </div>
                <span 
                  className={cn(
                    "px-2 py-1 rounded text-xs font-medium",
                    alert.type === 'error' ? "bg-red-100 text-red-800" :
                    alert.type === 'warning' ? "bg-amber-100 text-amber-800" :
                    "bg-green-100 text-green-800"
                  )}
                >
                  {alert.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default Index;
