
import { useState } from "react";
import { Menu, Home, Users, Monitor, Bell, Settings, User } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

interface SidebarProps {
  isCollapsed: boolean;
  onCollapse: (collapsed: boolean) => void;
}

export const Sidebar = ({ isCollapsed, onCollapse }: SidebarProps) => {
  const location = useLocation();
  
  const links = [
    { name: "Tableau de bord", icon: Home, path: "/dashboard" },
    { name: "Sites clients", icon: Users, path: "/sites" },
    { name: "Équipements", icon: Monitor, path: "/equipements" },
    { name: "Alertes", icon: Bell, path: "/alertes" },
    { name: "Configuration", icon: Settings, path: "/configuration" },
    { name: "Compte", icon: User, path: "/compte" }
  ];

  return (
    <aside className={cn(
      "fixed left-0 top-0 h-screen bg-white border-r border-border/50 transition-all duration-300",
      isCollapsed ? "w-20" : "w-64"
    )}>
      <div className="flex items-center gap-3 p-4 border-b border-border/50">
        <button 
          onClick={() => onCollapse(!isCollapsed)} 
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Menu size={20} />
        </button>
        {!isCollapsed && (
          <h1 className="text-xl font-bold text-[#0e3175]">Vigileos</h1>
        )}
      </div>
      
      <nav className="p-3 space-y-1">
        {links.map((link) => {
          const isActive = location.pathname === link.path;
          const Icon = link.icon;
          
          return (
            <Link
              key={link.path}
              to={link.path}
              className={cn(
                "flex items-center gap-3 px-4 py-2.5 rounded-lg transition-colors",
                isActive 
                  ? "bg-[#0e3175] text-white" 
                  : "hover:bg-gray-100"
              )}
            >
              <Icon size={20} />
              {!isCollapsed && <span>{link.name}</span>}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};
