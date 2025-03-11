import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { login as apiLogin, logout as apiLogout, getUserProfile, refreshToken as apiRefreshToken } from "@/lib/api/auth";

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
  login: async () => {},
  logout: () => {},
  loading: true,
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const refreshTokenValue = localStorage.getItem('refresh_token');
    
    const fetchUserProfile = async () => {
      try {
        if (token) {
          const userData = await getUserProfile();
          setUser(userData);
          setIsAuthenticated(true);
        } else if (refreshTokenValue) {
          // Si pas de token d'accès mais un refresh token, essayer de rafraîchir
          try {
            const response = await apiRefreshToken(refreshTokenValue);
            if (response.access) {
              localStorage.setItem('access_token', response.access);
              const userData = await getUserProfile();
              setUser(userData);
              setIsAuthenticated(true);
            }
          } catch (error) {
            console.error("Erreur lors du rafraîchissement du token:", error);
            localStorage.removeItem('refresh_token');
          }
        }
      } catch (error) {
        console.error("Erreur lors de la récupération du profil:", error);
        localStorage.removeItem('access_token');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      const response = await apiLogin({ username, password });
      
      if (response.access) {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        
        // Si l'API de login retourne les informations utilisateur
        if (response.user) {
          setUser(response.user);
        } else {
          // Sinon, faire une requête séparée pour obtenir le profil
          const userData = await getUserProfile();
          setUser(userData);
        }
        
        setIsAuthenticated(true);
        navigate('/dashboard');
      }
    } catch (error) {
      console.error("Erreur de connexion:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    apiLogout();
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
