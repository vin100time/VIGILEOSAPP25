
/**
 * Point d'entrée principal de l'API
 * Configuration et exports des fonctions API
 */

import { Site, Equipment } from "@/types/api";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:3000/api";

// Configuration de base pour fetch
const fetchConfig = {
  headers: {
    'Content-Type': 'application/json',
  },
};

// Fonctions API pour les sites
export const getSites = async () => {
  try {
    console.log('Fetching sites from:', `${API_URL}/sites`);
    const response = await fetch(`${API_URL}/sites`, fetchConfig);
    if (!response.ok) throw new Error('Failed to fetch sites');
    return await response.json();
  } catch (error) {
    console.error('Error fetching sites:', error);
    return [];
  }
};

export const createSite = async (site: Omit<Site, "id" | "created_at" | "updated_at">) => {
  const response = await fetch(`${API_URL}/sites`, {
    ...fetchConfig,
    method: 'POST',
    body: JSON.stringify(site),
  });
  if (!response.ok) throw new Error('Failed to create site');
  return await response.json();
};

export const updateSite = async (id: string, site: Partial<Site>) => {
  const response = await fetch(`${API_URL}/sites/${id}`, {
    ...fetchConfig,
    method: 'PUT',
    body: JSON.stringify(site),
  });
  if (!response.ok) throw new Error('Failed to update site');
  return await response.json();
};

export const deleteSite = async (id: string) => {
  const response = await fetch(`${API_URL}/sites/${id}`, {
    ...fetchConfig,
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete site');
};

// Fonctions API pour les équipements
export const getEquipment = async () => {
  const response = await fetch(`${API_URL}/equipment`, fetchConfig);
  if (!response.ok) throw new Error('Failed to fetch equipment');
  return await response.json();
};

export const getEquipmentBySite = async (siteId: string) => {
  const response = await fetch(`${API_URL}/sites/${siteId}/equipment`, fetchConfig);
  if (!response.ok) throw new Error('Failed to fetch site equipment');
  return await response.json();
};

export const createEquipment = async (equipment: Omit<Equipment, "id" | "created_at" | "updated_at">) => {
  const response = await fetch(`${API_URL}/equipment`, {
    ...fetchConfig,
    method: 'POST',
    body: JSON.stringify(equipment),
  });
  if (!response.ok) throw new Error('Failed to create equipment');
  return await response.json();
};

export const updateEquipment = async (id: string, equipment: Partial<Equipment>) => {
  const response = await fetch(`${API_URL}/equipment/${id}`, {
    ...fetchConfig,
    method: 'PUT',
    body: JSON.stringify(equipment),
  });
  if (!response.ok) throw new Error('Failed to update equipment');
  return await response.json();
};

export const deleteEquipment = async (id: string) => {
  const response = await fetch(`${API_URL}/equipment/${id}`, {
    ...fetchConfig,
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete equipment');
};

// Fonctions API pour les alertes
export const getAlerts = async () => {
  const response = await fetch(`${API_URL}/alerts`, fetchConfig);
  if (!response.ok) throw new Error('Failed to fetch alerts');
  return await response.json();
};
