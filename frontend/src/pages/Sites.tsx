import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Link } from "react-router-dom";
import { PlusCircle, RefreshCcw, ArrowRight, Trash2Icon, Search, Filter, UserIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSites, createSite, deleteSite } from "@/lib/api";
import { Site } from "@/types/database";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/components/AuthProvider";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Sites = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [isNewSiteDialogOpen, setIsNewSiteDialogOpen] = useState(false);
  const [newSiteName, setNewSiteName] = useState("");
  const [newSiteAddress, setNewSiteAddress] = useState("");
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const { logout } = useAuth();

  const { data: sites = [], isLoading, refetch } = useQuery({
    queryKey: ['sites'],
    queryFn: getSites,
    meta: {
      onError: (error: Error) => {
        toast({
          title: "Erreur",
          description: "Impossible de charger les sites. Veuillez réessayer.",
          variant: "destructive",
        });
        console.error("Error fetching sites:", error);
      },
    },
  });

  const createSiteMutation = useMutation({
    mutationFn: (site: Omit<Site, 'id' | 'created_at' | 'updated_at'>) => createSite(site),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sites'] });
      toast({
        title: "Succès",
        description: "Le site a été créé avec succès.",
      });
      setIsNewSiteDialogOpen(false);
      setNewSiteName("");
      setNewSiteAddress("");
    },
    onError: (error: Error) => {
      toast({
        title: "Erreur",
        description: "Impossible de créer le site. Veuillez réessayer.",
        variant: "destructive",
      });
      console.error("Error creating site:", error);
    },
  });

  const deleteSiteMutation = useMutation({
    mutationFn: async (id: string) => {
      await deleteSite(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sites'] });
      toast({
        title: "Succès",
        description: "Le site a été supprimé avec succès.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Erreur",
        description: "Impossible de supprimer le site. Veuillez réessayer.",
        variant: "destructive",
      });
      console.error("Error deleting site:", error);
    },
  });

  const handleCreateSite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSiteName || !newSiteAddress) {
      toast({
        title: "Erreur",
        description: "Veuillez remplir tous les champs.",
        variant: "destructive",
      });
      return;
    }

    createSiteMutation.mutate({
      name: newSiteName,
      address: newSiteAddress,
      status: 'pending' as const
    });
  };

  const handleDeleteSite = async (id: string) => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer ce site ?")) {
      deleteSiteMutation.mutate(id);
    }
  };

  const handleAssociateSite = async (id: string) => {
    try {
      // Simulation d'assignation locale
      toast({
        title: "Succès",
        description: "Le site a été associé avec succès.",
      });
      
      queryClient.invalidateQueries({ queryKey: ['sites'] });
    } catch (error: any) {
      toast({
        title: "Erreur",
        description: "Impossible d'associer le site. Veuillez réessayer.",
        variant: "destructive",
      });
    }
  };

  const filteredSites = (sites as Site[]).filter(site => {
    const matchesSearch = site.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         site.address.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || site.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

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

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Sites clients</h1>
          <p className="text-muted-foreground">
            Gestion et surveillance des sites
          </p>
        </div>
        <div className="flex items-center gap-4">
          <Button 
            className="bg-[#0e3175] hover:bg-[#0e3175]/90"
            onClick={() => navigate('/sites/detected')}
          >
            <PlusCircle className="w-4 h-4 mr-2" />
            Nouveau site
          </Button>
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

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input 
            placeholder="Rechercher un site..." 
            className="pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
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
              <SelectItem value="pending">Nouveaux sites</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Button 
          variant="outline" 
          size="icon" 
          className="ml-auto"
          onClick={() => refetch()}
          disabled={isLoading}
        >
          <RefreshCcw className={cn("w-4 h-4", isLoading && "animate-spin")} />
        </Button>
      </div>

      <div className="grid gap-4">
        {isLoading ? (
          <Card className="p-4">
            <div className="animate-pulse flex space-x-4">
              <div className="flex-1 space-y-4 py-1">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              </div>
            </div>
          </Card>
        ) : filteredSites.length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">Aucun site trouvé</p>
          </Card>
        ) : (
          filteredSites.map((site) => (
            <Card key={site.id} className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold">{site.name}</h3>
                  <p className="text-sm text-muted-foreground">{site.address}</p>
                </div>
                <div className="flex items-center gap-2">
                  <div className={cn(
                    "px-2 py-1 rounded-full text-xs font-medium",
                    site.status === 'online' && "bg-green-100 text-green-800",
                    site.status === 'offline' && "bg-red-100 text-red-800",
                    site.status === 'warning' && "bg-yellow-100 text-yellow-800",
                    site.status === 'pending' && "bg-blue-100 text-blue-800"
                  )}>
                    {site.status === 'online' && "En ligne"}
                    {site.status === 'offline' && "Hors ligne"}
                    {site.status === 'warning' && "Attention"}
                    {site.status === 'pending' && "Nouveau site détecté"}
                  </div>
                  <div className="flex gap-2">
                    {site.status === 'pending' ? (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleAssociateSite(site.id)}
                        className="text-blue-500 hover:text-blue-600"
                      >
                        Associer
                      </Button>
                    ) : (
                      <>
                        <Link to={`/sites/${site.id}/equipment`}>
                          <Button variant="ghost" size="icon">
                            <ArrowRight className="w-4 h-4" />
                          </Button>
                        </Link>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="text-red-500 hover:text-red-600"
                          onClick={() => handleDeleteSite(site.id)}
                          disabled={deleteSiteMutation.isPending}
                        >
                          <Trash2Icon className="w-4 h-4" />
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default Sites;
