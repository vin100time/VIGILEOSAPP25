
import { Search, Filter } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { RefreshCcw } from "lucide-react";

interface EquipmentFiltersProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  typeFilter: string;
  onTypeFilterChange: (value: string) => void;
  siteFilter: string;
  onSiteFilterChange: (value: string) => void;
  statusFilter: string;
  onStatusFilterChange: (value: string) => void;
}

export const EquipmentFilters = ({
  searchTerm,
  onSearchChange,
  typeFilter,
  onTypeFilterChange,
  siteFilter,
  onSiteFilterChange,
  statusFilter,
  onStatusFilterChange
}: EquipmentFiltersProps) => {
  return (
    <div className="flex items-center gap-4 pb-4">
      <div className="relative flex-1 max-w-xs">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <Input 
          placeholder="Rechercher un équipement..." 
          className="pl-9"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>
      <div className="relative">
        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
        <Select value={typeFilter} onValueChange={onTypeFilterChange}>
          <SelectTrigger className="pl-9 min-w-[180px]">
            <SelectValue placeholder="Tous les types" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tous les types</SelectItem>
            <SelectItem value="camera">Caméras</SelectItem>
            <SelectItem value="video-recorder">Enregistreurs vidéo</SelectItem>
            <SelectItem value="switch">Switches</SelectItem>
            <SelectItem value="server">Serveurs</SelectItem>
            <SelectItem value="antenna">Antennes/Points d'accès WiFi</SelectItem>
            <SelectItem value="router">Routeurs</SelectItem>
            <SelectItem value="pc">PC</SelectItem>
            <SelectItem value="other">Autres</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="relative">
        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
        <Select value={siteFilter} onValueChange={onSiteFilterChange}>
          <SelectTrigger className="pl-9 min-w-[180px]">
            <SelectValue placeholder="Tous les sites" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tous les sites</SelectItem>
            <SelectItem value="Paris Centre">Paris Centre</SelectItem>
            <SelectItem value="Lyon Sud">Lyon Sud</SelectItem>
            <SelectItem value="Marseille Port">Marseille Port</SelectItem>
            <SelectItem value="Bordeaux Nord">Bordeaux Nord</SelectItem>
            <SelectItem value="Lille Centre">Lille Centre</SelectItem>
            <SelectItem value="Nantes Est">Nantes Est</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="relative">
        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
        <Select value={statusFilter} onValueChange={onStatusFilterChange}>
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
      <Button variant="outline" size="icon" className="ml-auto">
        <RefreshCcw className="w-4 h-4" />
      </Button>
    </div>
  );
};
