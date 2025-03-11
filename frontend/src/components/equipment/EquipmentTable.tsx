
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Trash2Icon, ArrowRight } from "lucide-react";
import { EquipmentIcon } from "./EquipmentIcon";
import { StatusBadge } from "./StatusBadge";

interface Equipment {
  id: number;
  name: string;
  type: string;
  site: string;
  status: 'online' | 'offline' | 'warning';
  ip: string;
  lastMaintenance: string;
}

interface EquipmentTableProps {
  equipment: Equipment[];
}

export const EquipmentTable = ({ equipment }: EquipmentTableProps) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Équipement</TableHead>
          <TableHead>Type</TableHead>
          <TableHead>Site</TableHead>
          <TableHead>Statut</TableHead>
          <TableHead>IP</TableHead>
          <TableHead>Dernière maintenance</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {equipment.map((item) => (
          <TableRow key={item.id}>
            <TableCell className="font-medium">
              <div className="flex items-center gap-2">
                <EquipmentIcon type={item.type} />
                {item.name}
              </div>
            </TableCell>
            <TableCell className="capitalize">{item.type}</TableCell>
            <TableCell>{item.site}</TableCell>
            <TableCell>
              <StatusBadge status={item.status} />
            </TableCell>
            <TableCell>{item.ip}</TableCell>
            <TableCell>{item.lastMaintenance}</TableCell>
            <TableCell className="text-right">
              <div className="flex justify-end gap-2">
                <Link to={`/equipements/${item.id}`}>
                  <Button variant="ghost" size="icon">
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </Link>
                <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-600">
                  <Trash2Icon className="w-4 h-4" />
                </Button>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
