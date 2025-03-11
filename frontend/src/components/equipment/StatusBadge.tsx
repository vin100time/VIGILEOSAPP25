
import { cn } from "@/lib/utils";

type StatusType = 'online' | 'offline' | 'warning';

interface StatusBadgeProps {
  status: StatusType;
  className?: string;
}

export const StatusBadge = ({ status, className }: StatusBadgeProps) => {
  return (
    <div className={cn(
      "status-badge inline-flex",
      status === 'online' && "status-online",
      status === 'offline' && "status-offline",
      status === 'warning' && "status-warning",
      className
    )}>
      {status === 'online' && "En ligne"}
      {status === 'offline' && "Hors ligne"}
      {status === 'warning' && "Attention"}
    </div>
  );
};
