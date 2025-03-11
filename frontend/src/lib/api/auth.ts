import { ApiClient, apiClient } from "./client";

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user?: any;
}

export class AuthApi extends ApiClient {
  async login(data: LoginData): Promise<AuthResponse> {
    const response = await this.fetch<AuthResponse>("/api/auth/login/", {
      method: "POST",
      body: JSON.stringify(data),
    });
    
    if (response.access) {
      this.setAuthToken(response.access);
    }
    
    return response;
  }

  async register(data: RegisterData): Promise<AuthResponse> {
    return this.fetch<AuthResponse>("/api/auth/register/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    return this.fetch<AuthResponse>("/api/auth/token/refresh/", {
      method: "POST",
      body: JSON.stringify({ refresh: refreshToken }),
    });
  }

  async getUserProfile(): Promise<any> {
    return this.fetch<any>("/api/auth/profile/");
  }

  logout() {
    this.removeAuthToken();
  }
}

export const authApi = new AuthApi();

// Export des fonctions individuelles
export const login = (data: LoginData) => authApi.login(data);
export const register = (data: RegisterData) => authApi.register(data);
export const refreshToken = (refreshToken: string) => authApi.refreshToken(refreshToken);
export const getUserProfile = () => authApi.getUserProfile();
export const logout = () => authApi.logout();
