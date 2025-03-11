
/**
 * API Client pour la gestion des équipements
 */

import type { Equipment } from "@/types/database";
import { ApiClient, apiClient } from "./client";

export class EquipmentApi extends ApiClient {
  async getEquipment(): Promise<Equipment[]> {
    return this.fetch<Equipment[]>("/equipment");
  }

  async getEquipmentBySite(siteId: string): Promise<Equipment[]> {
    return this.fetch<Equipment[]>(`/sites/${siteId}/equipment`);
  }

  async createEquipment(
    equipment: Omit<Equipment, "id" | "created_at" | "updated_at">
  ): Promise<Equipment> {
    return this.fetch<Equipment>("/equipment", {
      method: "POST",
      body: JSON.stringify(equipment),
    });
  }

  async updateEquipment(
    id: string,
    equipment: Partial<Equipment>
  ): Promise<Equipment> {
    return this.fetch<Equipment>(`/equipment/${id}`, {
      method: "PUT",
      body: JSON.stringify(equipment),
    });
  }

  async deleteEquipment(id: string): Promise<void> {
    await this.fetch(`/equipment/${id}`, {
      method: "DELETE",
    });
  }
}

export const equipmentApi = new EquipmentApi();

// Export des fonctions individuelles
export const getEquipment = () => equipmentApi.getEquipment();
export const getEquipmentBySite = (siteId: string) => equipmentApi.getEquipmentBySite(siteId);
export const createEquipment = (equipment: Omit<Equipment, "id" | "created_at" | "updated_at">) => equipmentApi.createEquipment(equipment);
export const updateEquipment = (id: string, equipment: Partial<Equipment>) => equipmentApi.updateEquipment(id, equipment);
export const deleteEquipment = (id: string) => equipmentApi.deleteEquipment(id);
