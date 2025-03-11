
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useQueryClient } from "@tanstack/react-query";
import { Equipment } from "@/types/api";
import { createEquipment } from "@/lib/api";

interface AddEquipmentDialogProps {
  siteId: string;
}

export const AddEquipmentDialog = ({ siteId }: AddEquipmentDialogProps) => {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [type, setType] = useState<Equipment['type']>("camera");
  const [ipAddress, setIpAddress] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const newEquipment = {
        name,
        type,
        ip_address: ipAddress,
        site_id: siteId,
        status: 'online' as const,
        last_maintenance: null
      };

      await createEquipment(newEquipment);

      toast({
        title: "Équipement ajouté",
        description: "L'équipement a été ajouté avec succès"
      });

      // Rafraîchir la liste des équipements
      queryClient.invalidateQueries({ queryKey: ['equipment', siteId] });
      
      // Réinitialiser le formulaire et fermer la modale
      setName("");
      setType("camera");
      setIpAddress("");
      setOpen(false);
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erreur",
        description: "Impossible d'ajouter l'équipement"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Ajouter un équipement
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Ajouter un équipement</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nom de l'équipement</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Entrez le nom de l'équipement"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="type">Type d'équipement</Label>
            <Select value={type} onValueChange={(value: Equipment['type']) => setType(value)} required>
              <SelectTrigger>
                <SelectValue placeholder="Sélectionnez un type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="camera">Caméra</SelectItem>
                <SelectItem value="video-recorder">Enregistreur vidéo</SelectItem>
                <SelectItem value="switch">Switch</SelectItem>
                <SelectItem value="server">Serveur</SelectItem>
                <SelectItem value="access_point">Point d'accès WiFi</SelectItem>
                <SelectItem value="router">Routeur</SelectItem>
                <SelectItem value="other">Autre</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="ip">Adresse IP</Label>
            <Input
              id="ip"
              value={ipAddress}
              onChange={(e) => setIpAddress(e.target.value)}
              placeholder="Entrez l'adresse IP"
            />
          </div>

          <div className="flex justify-end gap-4 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
            >
              Annuler
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Ajout en cours..." : "Ajouter"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};
