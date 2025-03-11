import { useParams, Link } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ExternalLink, Edit2Icon, Trash2Icon, CameraIcon, VideoIcon, NetworkIcon, ServerIcon, WifiIcon, RouterIcon, MonitorIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { EditEquipmentForm } from "@/components/equipment/EditEquipmentForm";
import { Equipment } from "@/types/database";

const EquipmentDetail = () => {
  const { id } = useParams();
  const [selectedPort, setSelectedPort] = useState<string>("");
  const [customPort, setCustomPort] = useState<string>("");
  const [isEditing, setIsEditing] = useState(false);
  const { toast } = useToast();

  const getIcon = (type: string) => {
    switch(type) {
      case 'camera':
        return <CameraIcon className="w-5 h-5" />;
      case 'video-recorder':
        return <VideoIcon className="w-5 h-5" />;
      case 'switch':
        return <NetworkIcon className="w-5 h-5" />;
      case 'server':
        return <ServerIcon className="w-5 h-5" />;
      case 'antenna':
        return <WifiIcon className="w-5 h-5" />;
      case 'router':
        return <RouterIcon className="w-5 h-5" />;
      case 'pc':
        return <MonitorIcon className="w-5 h-5" />;
      default:
        return <ServerIcon className="w-5 h-5" />;
    }
  };

  const handleAccess = () => {
    const portToUse = selectedPort === "custom" ? customPort : selectedPort;
    
    if (!portToUse) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner ou saisir un port",
        variant: "destructive",
      });
      return;
    }

    if (portToUse === "22") {
      toast({
        title: "Information",
        description: "L'accès SSH via terminal web sera bientôt disponible",
      });
      return;
    }
    
    const baseUrl = equipment.ip_address;
    const url = `http://${baseUrl}:${portToUse}`;
    window.open(url, '_blank');
  };

  const equipment: Equipment = {
    id: "1",
    site_id: "1",
    name: "Router-01",
    type: "router",
    status: "online",
    ip_address: "192.168.1.1",
    last_maintenance: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  const availablePorts = [
    { value: "80", label: "HTTP (80)" },
    { value: "443", label: "HTTPS (443)" },
    { value: "8080", label: "HTTP Alt (8080)" },
    { value: "8443", label: "HTTPS Alt (8443)" },
    { value: "22", label: "SSH (22) - Terminal Web" },
    { value: "custom", label: "Port personnalisé" },
  ];

  if (isEditing) {
    return (
      <EditEquipmentForm
        equipment={equipment}
        onClose={() => setIsEditing(false)}
      />
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/sites" className="text-muted-foreground hover:text-foreground">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-2xl font-bold">{equipment.name}</h1>
        </div>
        <div className="flex items-center gap-2">
          <Dialog>
            <DialogTrigger asChild>
              <Button className="bg-[#0e3175] hover:bg-[#0e3175]/90">
                <ExternalLink className="w-4 h-4 mr-2" />
                Accéder
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Sélectionner un port d'accès</DialogTitle>
              </DialogHeader>
              <div className="py-4 space-y-4">
                <div className="space-y-2">
                  <Label>Port</Label>
                  <Select
                    value={selectedPort}
                    onValueChange={(value) => {
                      setSelectedPort(value);
                      if (value !== "custom") {
                        setCustomPort("");
                      }
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Choisir un port" />
                    </SelectTrigger>
                    <SelectContent>
                      {availablePorts.map((port) => (
                        <SelectItem key={port.value} value={port.value}>
                          {port.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {selectedPort === "custom" && (
                  <div className="space-y-2">
                    <Label>Port personnalisé</Label>
                    <Input
                      type="number"
                      placeholder="Entrez le numéro de port"
                      value={customPort}
                      onChange={(e) => setCustomPort(e.target.value)}
                      min="1"
                      max="65535"
                    />
                  </div>
                )}

                {selectedPort === "22" && (
                  <p className="text-sm text-muted-foreground">
                    Le terminal web vous permettra d'accéder à l'équipement via SSH directement depuis votre navigateur.
                  </p>
                )}

                <div className="mt-4 flex justify-end">
                  <Button
                    onClick={handleAccess}
                    className="bg-[#0e3175] hover:bg-[#0e3175]/90"
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Accéder
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
          <Button 
            variant="outline"
            onClick={() => setIsEditing(true)}
          >
            <Edit2Icon className="w-4 h-4 mr-2" />
            Modifier
          </Button>
          <Button variant="destructive">
            <Trash2Icon className="w-4 h-4 mr-2" />
            Supprimer
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Informations générales</h2>
          <dl className="space-y-4">
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Type</dt>
              <dd className="font-medium capitalize">{equipment.type}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Statut</dt>
              <dd>
                <span className={cn(
                  "status-badge",
                  equipment.status === 'online' && "status-online",
                  equipment.status === 'offline' && "status-offline",
                  equipment.status === 'maintenance' && "status-maintenance"
                )}>
                  {equipment.status === 'online' && "En ligne"}
                  {equipment.status === 'offline' && "Hors ligne"}
                  {equipment.status === 'maintenance' && "Maintenance"}
                </span>
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Adresse IP</dt>
              <dd className="font-medium">{equipment.ip_address}</dd>
            </div>
            {/* <div className="flex justify-between">
              <dt className="text-muted-foreground">Adresse MAC</dt>
              <dd className="font-medium">{equipment.mac}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Modèle</dt>
              <dd className="font-medium">{equipment.model}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Localisation</dt>
              <dd className="font-medium">{equipment.location}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-muted-foreground">Temps de fonctionnement</dt>
              <dd className="font-medium">{equipment.uptime}</dd>
            </div> */}
          </dl>
        </Card>

        {/* <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Performances</h2>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-muted-foreground">CPU</span>
                <span className="font-medium">{equipment.cpu}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{ width: `${equipment.cpu}%` }}
                />
              </div>
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-muted-foreground">Mémoire</span>
                <span className="font-medium">{equipment.memory}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full" 
                  style={{ width: `${equipment.memory}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-muted-foreground">Température</span>
                <span className="font-medium">{equipment.temperature}°C</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-yellow-500 h-2 rounded-full" 
                  style={{ width: `${(equipment.temperature / 100) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </Card> */}

        {/* <Card className="p-6 md:col-span-2">
          <h2 className="text-lg font-semibold mb-4">Interfaces réseau</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b">
                  <th className="pb-2">Interface</th>
                  <th className="pb-2">Statut</th>
                  <th className="pb-2">Vitesse</th>
                </tr>
              </thead>
              <tbody>
                {equipment.interfaces.map((interface_, index) => (
                  <tr key={index} className="border-b last:border-0">
                    <td className="py-3 font-medium">{interface_.name}</td>
                    <td className="py-3">
                      <span className={cn(
                        "status-badge",
                        interface_.status === 'up' && "status-online",
                        interface_.status === 'down' && "status-offline"
                      )}>
                        {interface_.status === 'up' ? 'Actif' : 'Inactif'}
                      </span>
                    </td>
                    <td className="py-3">{interface_.speed}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card> */}
      </div>
    </div>
  );
};

export default EquipmentDetail;
