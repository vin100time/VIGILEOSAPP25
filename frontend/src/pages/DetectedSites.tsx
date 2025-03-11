import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSites } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { Site } from "@/types/database";
import { ArrowLeft } from "lucide-react";

const DetectedSites = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: sites = [], isLoading } = useQuery({
    queryKey: ['pending-sites'],
    queryFn: async () => {
      // Simulation de données locales
      return [] as Site[];
    },
  });

  const handleAssignSite = async (id: string) => {
    try {
      // Simulation d'assignation locale
      toast({
        title: "Succès",
        description: "Le site a été assigné avec succès.",
      });
      queryClient.invalidateQueries({ queryKey: ['pending-sites'] });
      queryClient.invalidateQueries({ queryKey: ['sites'] });
    } catch (error: any) {
      toast({
        title: "Erreur",
        description: "Impossible d'assigner le site. Veuillez réessayer.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => navigate('/sites')}
            >
              <ArrowLeft className="w-4 h-4" />
            </Button>
            <h1 className="text-2xl font-bold">Sites détectés</h1>
          </div>
          <p className="text-muted-foreground mt-1">
            Nouveaux sites en attente d'assignation
          </p>
        </div>
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
        ) : sites.length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-muted-foreground">Aucun nouveau site détecté</p>
          </Card>
        ) : (
          sites.map((site) => (
            <Card key={site.id} className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold">{site.name}</h3>
                  <p className="text-sm text-muted-foreground">{site.address}</p>
                </div>
                <Button
                  onClick={() => handleAssignSite(site.id)}
                  className="bg-[#0e3175] hover:bg-[#0e3175]/90"
                >
                  Assigner
                </Button>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default DetectedSites;
