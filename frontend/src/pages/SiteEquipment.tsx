
import { useParams, Link } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { getEquipmentBySite } from "@/lib/api";
import { Equipment } from "@/types/database";
import { cn } from "@/lib/utils";
import { ArrowLeft, Search, Filter } from "lucide-react";
import { AddEquipmentDialog } from "@/components/equipment/AddEquipmentDialog";
import { EquipmentIcon } from "@/components/equipment/EquipmentIcon";

const SiteEquipment = () => {
  const { siteId } = useParams();
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const { toast } = useToast();

  const { data: equipment, isLoading, error } = useQuery({
    queryKey: ['equipment', siteId],
    queryFn: () => siteId ? getEquipmentBySite(siteId) : Promise.resolve([]),
  });

  if (error) {
    toast({
      variant: "destructive",
      title: "Erreur",
      description: "Impossible de charger les équipements"
    });
  }

  const filteredEquipment = equipment?.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === "all" || item.type === typeFilter;
    const matchesStatus = statusFilter === "all" || item.status === statusFilter;
    return matchesSearch && matchesType && matchesStatus;
  }) || [];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/sites" className="text-muted-foreground hover:text-foreground">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">Équipements du site</h1>
            <p className="text-muted-foreground">
              Gestion des équipements pour ce site
            </p>
          </div>
        </div>
        {siteId && <AddEquipmentDialog siteId={siteId} />}
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input 
            placeholder="Rechercher un équipement..." 
            className="pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
          <Select value={typeFilter} onValueChange={setTypeFilter}>
            <SelectTrigger className="pl-9 min-w-[180px]">
              <SelectValue placeholder="Tous les types" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tous les types</SelectItem>
              <SelectItem value="camera">Caméras</SelectItem>
              <SelectItem value="video-recorder">Enregistreurs vidéo</SelectItem>
              <SelectItem value="switch">Switches</SelectItem>
              <SelectItem value="server">Serveurs</SelectItem>
              <SelectItem value="access_point">Points d'accès WiFi</SelectItem>
              <SelectItem value="router">Routeurs</SelectItem>
              <SelectItem value="pc">PCs</SelectItem>
              <SelectItem value="other">Autres</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="pl-9 min-w-[180px]">
              <SelectValue placeholder="Tous les statuts" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tous les statuts</SelectItem>
              <SelectItem value="online">En ligne</SelectItem>
              <SelectItem value="offline">Hors ligne</SelectItem>
              <SelectItem value="warning">Attention</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-8">Chargement des équipements...</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredEquipment.map((item) => (
            <Link to={`/equipements/${item.id}`} key={item.id}>
              <Card className="p-4 hover:shadow-lg transition-all">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <EquipmentIcon type={item.type} />
                    <div>
                      <h3 className="font-medium">{item.name}</h3>
                      <p className="text-sm text-muted-foreground">{item.ip_address || 'Pas d\'IP'}</p>
                    </div>
                  </div>
                  <div className={cn(
                    "px-2 py-1 rounded-full text-xs font-medium",
                    item.status === 'online' && "bg-green-100 text-green-700",
                    item.status === 'offline' && "bg-red-100 text-red-700",
                    item.status === 'warning' && "bg-yellow-100 text-yellow-700"
                  )}>
                    {item.status === 'online' && "En ligne"}
                    {item.status === 'offline' && "Hors ligne"}
                    {item.status === 'warning' && "Attention"}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default SiteEquipment;
