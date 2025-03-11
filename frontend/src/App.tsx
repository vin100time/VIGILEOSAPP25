import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider, useAuth } from "@/components/AuthProvider";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Index from "./pages/Index";
import Sites from "./pages/Sites";
import DetectedSites from "./pages/DetectedSites";
import Equipment from "./pages/Equipment";
import SiteEquipment from "./pages/SiteEquipment";
import EquipmentDetail from "./pages/EquipmentDetail";
import Alerts from "./pages/Alerts";
import Settings from "./pages/Settings";
import Account from "./pages/Account";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

// Composant de protection des routes
const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  // Si l'authentification est en cours de chargement, afficher un indicateur de chargement
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#0e3175]"></div>
      </div>
    );
  }

  // Si l'utilisateur n'est pas authentifié, rediriger vers la page de connexion
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  // Si l'utilisateur est authentifié, afficher les routes enfants
  return <Outlet />;
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Page d'accueil */}
          <Route path="/" element={<Landing />} />

          {/* Routes protégées avec Layout */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="dashboard" element={<Index />} />
              <Route path="sites" element={<Sites />} />
              <Route path="sites/detected" element={<DetectedSites />} />
              <Route path="sites/:siteId/equipment" element={<SiteEquipment />} />
              <Route path="equipements" element={<Equipment />} />
              <Route path="equipements/:id" element={<EquipmentDetail />} />
              <Route path="alertes" element={<Alerts />} />
              <Route path="configuration" element={<Settings />} />
              <Route path="compte" element={<Account />} />
            </Route>
          </Route>

          {/* Page 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Toaster />
        <Sonner />
      </AuthProvider>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
