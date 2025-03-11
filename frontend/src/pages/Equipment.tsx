
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { EquipmentFilters } from "@/components/equipment/EquipmentFilters";
import { EquipmentTable } from "@/components/equipment/EquipmentTable";
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

const Equipment = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [siteFilter, setSiteFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
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

  const equipment = [
    {
      id: 1,
      name: "Camera IP-01",
      type: "camera",
      site: "Paris Centre",
      status: "online" as const,
      ip: "192.168.1.101",
      lastMaintenance: "2024-02-15"
    },
    {
      id: 2,
      name: "Switch SW-02",
      type: "switch",
      site: "Lyon Sud",
      status: "online" as const,
      ip: "192.168.1.102",
      lastMaintenance: "2024-02-20"
    },
    {
      id: 3,
      name: "Routeur RT-01",
      type: "router",
      site: "Marseille Port",
      status: "offline" as const,
      ip: "192.168.1.103",
      lastMaintenance: "2024-02-10"
    },
    {
      id: 4,
      name: "Serveur SV-01",
      type: "server",
      site: "Bordeaux Nord",
      status: "online" as const,
      ip: "192.168.1.104",
      lastMaintenance: "2024-02-25"
    },
    {
      id: 5,
      name: "Camera IP-02",
      type: "camera",
      site: "Lille Centre",
      status: "warning" as const,
      ip: "192.168.1.105",
      lastMaintenance: "2024-02-18"
    },
    {
      id: 6,
      name: "Switch SW-03",
      type: "switch",
      site: "Nantes Est",
      status: "online" as const,
      ip: "192.168.1.106",
      lastMaintenance: "2024-02-22"
    },
    {
      id: 7,
      name: "Point d'accès AP-01",
      type: "access_point",
      site: "Paris Centre",
      status: "online" as const,
      ip: "192.168.1.107",
      lastMaintenance: "2024-02-23"
    },
    {
      id: 8,
      name: "NVR-01",
      type: "video-recorder",
      site: "Lyon Sud",
      status: "online" as const,
      ip: "192.168.1.108",
      lastMaintenance: "2024-02-24"
    },
    {
      id: 9,
      name: "PC-01",
      type: "pc",
      site: "Marseille Port",
      status: "warning" as const,
      ip: "192.168.1.109",
      lastMaintenance: "2024-02-26"
    },
    {
      id: 10,
      name: "Device-01",
      type: "other",
      site: "Bordeaux Nord",
      status: "online" as const,
      ip: "192.168.1.110",
      lastMaintenance: "2024-02-27"
    }
  ];

  const filteredEquipment = equipment.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.ip.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === "all" || item.type === typeFilter;
    const matchesSite = siteFilter === "all" || item.site === siteFilter;
    const matchesStatus = statusFilter === "all" || item.status === statusFilter;
    return matchesSearch && matchesType && matchesSite && matchesStatus;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Équipements</h1>
          <p className="text-muted-foreground">
            Gestion et surveillance des équipements réseau
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

      <EquipmentFilters 
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        typeFilter={typeFilter}
        onTypeFilterChange={setTypeFilter}
        siteFilter={siteFilter}
        onSiteFilterChange={setSiteFilter}
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
      />

      <Card className="glass">
        <EquipmentTable equipment={filteredEquipment} />
      </Card>
    </div>
  );
};

export default Equipment;
