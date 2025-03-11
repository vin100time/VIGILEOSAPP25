
/**
 * Types de données pour l'application de surveillance réseau
 */

/**
 * Représente un site physique
 */
export interface Site {
  id: string;
  name: string;
  address: string;
  city?: string;
  postal_code?: string;
  status: 'online' | 'offline' | 'warning' | 'pending';
  created_at: string;
  updated_at: string;
}

/**
 * Représente un équipement réseau
 */
export interface Equipment {
  id: string;
  site_id: string;
  name: string;
  type: 'camera' | 'video-recorder' | 'switch' | 'server' | 'access_point' | 'router' | 'other';
  status: 'online' | 'offline' | 'maintenance';
  ip_address: string | null;
  last_maintenance: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Représente une alerte système
 */
export interface Alert {
  id: string;
  equipment_id: string;
  type: 'error' | 'warning' | 'info';
  title: string;
  message: string;
  description?: string;
  status: 'active' | 'resolved' | 'acknowledged';
  created_at: string;
  resolved_at: string | null;
  updated_at?: string;
}

