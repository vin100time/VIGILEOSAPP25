/**
 * Client API de base avec la configuration commune
 */

// @ts-ignore - Vite fournit cette variable d'environnement
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class ApiClient {
  private baseUrl: string;
  private token: string | null;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
    // Récupérer le token du localStorage au démarrage
    this.token = localStorage.getItem('access_token');
  }

  setAuthToken(token: string) {
    this.token = token;
    localStorage.setItem('access_token', token);
  }

  removeAuthToken() {
    this.token = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  private get headers() {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };
    
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  protected async fetch<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...this.headers,
          ...options.headers,
        },
      });

      if (response.status === 401) {
        // Token expiré, essayer de rafraîchir le token
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            const refreshResponse = await fetch(`${this.baseUrl}/api/auth/token/refresh/`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ refresh: refreshToken }),
            });
            
            if (refreshResponse.ok) {
              const data = await refreshResponse.json();
              this.setAuthToken(data.access);
              
              // Réessayer la requête originale avec le nouveau token
              return this.fetch(endpoint, options);
            } else {
              // Si le rafraîchissement échoue, déconnexion
              this.removeAuthToken();
              window.location.href = '/';
              throw new Error('Session expirée. Veuillez vous reconnecter.');
            }
          } catch (error) {
            this.removeAuthToken();
            window.location.href = '/';
            throw new Error('Session expirée. Veuillez vous reconnecter.');
          }
        } else {
          // Pas de refresh token, déconnexion
          this.removeAuthToken();
          window.location.href = '/';
          throw new Error('Session expirée. Veuillez vous reconnecter.');
        }
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || 
                            errorData.non_field_errors?.[0] || 
                            Object.values(errorData)[0]?.[0] || 
                            `API Error: ${response.statusText}`;
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }
}

// Export une instance par défaut
export const apiClient = new ApiClient();
