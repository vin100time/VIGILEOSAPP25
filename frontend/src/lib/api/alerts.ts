
/**
 * API Client pour la gestion des alertes
 */

import type { Alert } from "@/types/database";
import { ApiClient, apiClient } from "./client";

export class AlertsApi extends ApiClient {
  async getAlerts(): Promise<Alert[]> {
    return this.fetch<Alert[]>("/alerts");
  }

  async getAlertsByEquipment(equipmentId: string): Promise<Alert[]> {
    return this.fetch<Alert[]>(`/equipment/${equipmentId}/alerts`);
  }

  async createAlert(
    alert: Omit<Alert, "id" | "created_at" | "updated_at">
  ): Promise<Alert> {
    return this.fetch<Alert>("/alerts", {
      method: "POST",
      body: JSON.stringify(alert),
    });
  }

  async updateAlert(id: string, alert: Partial<Alert>): Promise<Alert> {
    return this.fetch<Alert>(`/alerts/${id}`, {
      method: "PUT",
      body: JSON.stringify(alert),
    });
  }
}

export const alertsApi = new AlertsApi();

// Export des fonctions individuelles
export const getAlerts = () => alertsApi.getAlerts();
export const getAlertsByEquipment = (equipmentId: string) => alertsApi.getAlertsByEquipment(equipmentId);
export const createAlert = (alert: Omit<Alert, "id" | "created_at" | "updated_at">) => alertsApi.createAlert(alert);
export const updateAlert = (id: string, alert: Partial<Alert>) => alertsApi.updateAlert(id, alert);
