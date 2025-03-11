
/**
 * API Client pour la gestion des sites
 */

import type { Site } from "@/types/database";
import { ApiClient, apiClient } from "./client";

export class SitesApi extends ApiClient {
  async getSites(): Promise<Site[]> {
    return this.fetch<Site[]>("/sites");
  }

  async getSiteById(id: string): Promise<Site> {
    return this.fetch<Site>(`/sites/${id}`);
  }

  async createSite(site: Omit<Site, "id" | "created_at" | "updated_at">): Promise<Site> {
    return this.fetch<Site>("/sites", {
      method: "POST",
      body: JSON.stringify(site),
    });
  }

  async updateSite(id: string, site: Partial<Site>): Promise<Site> {
    return this.fetch<Site>(`/sites/${id}`, {
      method: "PUT",
      body: JSON.stringify(site),
    });
  }

  async deleteSite(id: string): Promise<void> {
    await this.fetch(`/sites/${id}`, {
      method: "DELETE",
    });
  }

  async getSiteStats(siteId: string): Promise<{
    equipment: { [key: string]: number };
    alerts: { [key: string]: { [key: string]: number } };
  }> {
    return this.fetch(`/sites/${siteId}/stats`);
  }
}

export const sitesApi = new SitesApi();

// Export des fonctions individuelles
export const getSites = () => sitesApi.getSites();
export const getSiteById = (id: string) => sitesApi.getSiteById(id);
export const createSite = (site: Omit<Site, "id" | "created_at" | "updated_at">) => sitesApi.createSite(site);
export const updateSite = (id: string, site: Partial<Site>) => sitesApi.updateSite(id, site);
export const deleteSite = (id: string) => sitesApi.deleteSite(id);
export const getSiteStats = (siteId: string) => sitesApi.getSiteStats(siteId);
