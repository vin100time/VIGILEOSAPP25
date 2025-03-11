
import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";
import { Equipment } from "@/types/api";
import { updateEquipment } from "@/lib/api";

interface EditEquipmentFormProps {
  equipment: Equipment;
  onClose: () => void;
}

export const EditEquipmentForm = ({ equipment, onClose }: EditEquipmentFormProps) => {
  const [name, setName] = useState(equipment.name);
  const [type, setType] = useState<Equipment['type']>(equipment.type);
  const [isLoading, setIsLoading] = useState(false);
  
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await updateEquipment(equipment.id, { name, type });

      toast({
        title: "Équipement mis à jour",
        description: "Les modifications ont été enregistrées avec succès"
      });

      queryClient.invalidateQueries({ queryKey: ['equipment', equipment.site_id] });
      onClose();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erreur",
        description: "Impossible de mettre à jour l'équipement"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="p-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={onClose}
          className="mb-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Retour
        </Button>
        <h2 className="text-2xl font-bold">Modifier l'équipement</h2>
        <p className="text-muted-foreground">
          Modifiez les informations de l'équipement ci-dessous
        </p>
      </div>

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

        <div className="flex justify-end gap-4 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
          >
            Annuler
          </Button>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Enregistrement..." : "Enregistrer"}
          </Button>
        </div>
      </form>
    </Card>
  );
};
