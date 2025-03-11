import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { User, Lock, Wifi } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/components/AuthProvider";
import { register } from "@/lib/api/auth";

const Landing = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isLogin) {
        // Connexion
        await login(username, password);
        toast({
          title: "Connexion réussie",
          description: "Bienvenue !",
        });
      } else {
        // Inscription
        if (password !== confirmPassword) {
          throw new Error("Les mots de passe ne correspondent pas");
        }
        
        const response = await register({
          username,
          email,
          password,
          password_confirm: confirmPassword,
        });
        
        if (response.access) {
          // Connexion automatique après inscription
          await login(username, password);
          toast({
            title: "Inscription réussie",
            description: "Votre compte a été créé avec succès !",
          });
        }
      }
    } catch (error: any) {
      toast({
        title: "Erreur",
        description: error.message || "Une erreur est survenue",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-[#0e3175]/5 via-white to-[#0e3175]/5">
      <nav className="border-b bg-white/50 backdrop-blur-sm sticky top-0 z-50 animate-fade-in">
        <div className="mx-auto px-4 sm:px-6 max-w-screen-2xl">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <span className="text-xl sm:text-2xl font-bold text-[#0e3175] tracking-tight hover:scale-105 transition-transform duration-300">Vigileos.</span>
            </div>
            <div className="flex items-center gap-2">
              <Button 
                variant={isLogin ? "default" : "outline"}
                onClick={() => setIsLogin(true)}
                className={`${isLogin ? "bg-[#0e3175] hover:bg-[#0e3175]/90" : ""} text-sm transition-all duration-300 hover:-translate-y-0.5 px-3 sm:px-4`}
              >
                Connexion
              </Button>
              <Button 
                variant={!isLogin ? "default" : "outline"}
                onClick={() => setIsLogin(false)}
                className={`${!isLogin ? "bg-[#0e3175] hover:bg-[#0e3175]/90" : ""} text-sm transition-all duration-300 hover:-translate-y-0.5 px-3 sm:px-4`}
              >
                S'inscrire
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex-1 flex items-center">
        <div className="w-full">
          <div className="mx-auto px-4 sm:px-6 max-w-screen-2xl">
            <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
              <div className="space-y-6 lg:space-y-8 animate-fade-in [animation-delay:200ms] max-w-xl mx-auto lg:mx-0">
                <div className="space-y-4">
                  <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold leading-tight text-gray-900 tracking-tight">
                    Supervision à distance de vos sites en <span className="text-[#0e3175] animate-pulse">temps réel</span>
                  </h1>
                  <p className="text-base sm:text-lg text-gray-600 leading-relaxed animate-fade-in [animation-delay:400ms]">
                    Vigileos vous permet de surveiller tous vos sites et équipements depuis une interface unique, 
                    avec des alertes en temps réel et des analyses détaillées.
                  </p>
                </div>
                
                <div className="space-y-3">
                  <div className="transform hover:scale-[1.02] transition-all duration-300 animate-fade-in [animation-delay:600ms]">
                    <div className="flex items-center gap-3 p-4 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                      <div className="bg-[#0e3175]/10 p-2 rounded-xl shrink-0">
                        <User className="h-5 w-5 text-[#0e3175]" />
                      </div>
                      <span className="text-sm text-gray-700 font-medium">Sécurité renforcée et monitoring 24/7</span>
                    </div>
                  </div>

                  <div className="transform hover:scale-[1.02] transition-all duration-300 animate-fade-in [animation-delay:800ms]">
                    <div className="flex items-center gap-3 p-4 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                      <div className="bg-[#0e3175]/10 p-2 rounded-xl shrink-0">
                        <Lock className="h-5 w-5 text-[#0e3175]" />
                      </div>
                      <span className="text-sm text-gray-700 font-medium">Alertes en temps réel sur tous vos appareils</span>
                    </div>
                  </div>

                  <div className="transform hover:scale-[1.02] transition-all duration-300 animate-fade-in [animation-delay:1000ms]">
                    <div className="flex items-center gap-3 p-4 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                      <div className="bg-[#0e3175]/10 p-2 rounded-xl shrink-0">
                        <Wifi className="h-5 w-5 text-[#0e3175]" />
                      </div>
                      <span className="text-sm text-gray-700 font-medium">Accès à distance à vos équipements où que vous soyez</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-center lg:justify-end">
                <Card className="p-6 shadow-2xl bg-white border-0 rounded-2xl transform hover:scale-[1.01] transition-all duration-300 animate-fade-in [animation-delay:400ms] w-full max-w-md">
                  <div className="mb-6">
                    <h2 className="text-2xl font-bold mb-2 text-[#0e3175] tracking-tight">
                      {isLogin ? "Connexion" : "Créer un compte"}
                    </h2>
                    <p className="text-gray-600 text-sm">
                      {isLogin 
                        ? "Accédez à votre tableau de bord" 
                        : "Commencez à superviser vos sites"}
                    </p>
                  </div>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    {isLogin ? (
                      <>
                        <div className="space-y-2 animate-fade-in [animation-delay:200ms]">
                          <Label htmlFor="username" className="text-sm font-medium">Nom d'utilisateur</Label>
                          <Input 
                            id="username" 
                            type="text" 
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="nom_utilisateur"
                            required
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>

                        <div className="space-y-2 animate-fade-in [animation-delay:400ms]">
                          <Label htmlFor="password" className="text-sm font-medium">Mot de passe</Label>
                          <Input 
                            id="password" 
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={6}
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="space-y-2 animate-fade-in [animation-delay:200ms]">
                          <Label htmlFor="username" className="text-sm font-medium">Nom d'utilisateur</Label>
                          <Input 
                            id="username" 
                            type="text" 
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="nom_utilisateur"
                            required
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>

                        <div className="space-y-2 animate-fade-in [animation-delay:300ms]">
                          <Label htmlFor="email" className="text-sm font-medium">Email</Label>
                          <Input 
                            id="email" 
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="contact@entreprise.fr"
                            required
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>

                        <div className="space-y-2 animate-fade-in [animation-delay:400ms]">
                          <Label htmlFor="password" className="text-sm font-medium">Mot de passe</Label>
                          <Input 
                            id="password" 
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={6}
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>

                        <div className="space-y-2 animate-fade-in [animation-delay:500ms]">
                          <Label htmlFor="confirmPassword" className="text-sm font-medium">Confirmer le mot de passe</Label>
                          <Input 
                            id="confirmPassword" 
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            minLength={6}
                            className="h-10 px-4 bg-white text-sm focus:ring-2 focus:ring-[#0e3175] focus:ring-offset-0"
                          />
                        </div>
                      </>
                    )}

                    <Button 
                      type="submit"
                      disabled={isLoading}
                      className="w-full bg-[#0e3175] hover:bg-[#0e3175]/90 h-10 text-sm font-medium transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5 animate-fade-in [animation-delay:800ms]"
                    >
                      {isLogin ? (
                        <User className="mr-2 h-4 w-4" />
                      ) : (
                        <Lock className="mr-2 h-4 w-4" />
                      )}
                      {isLoading ? "Chargement..." : (isLogin ? "Se connecter" : "Créer un compte")}
                    </Button>
                  </form>

                  <p className="text-center text-xs text-gray-600 mt-4 animate-fade-in [animation-delay:1000ms]">
                    {isLogin ? (
                      <>
                        Pas encore de compte ?{" "}
                        <button
                          type="button"
                          onClick={() => setIsLogin(false)}
                          className="text-[#0e3175] font-medium hover:underline transition-all hover:-translate-y-0.5"
                        >
                          S'inscrire
                        </button>
                      </>
                    ) : (
                      <>
                        Déjà un compte ?{" "}
                        <button
                          type="button"
                          onClick={() => setIsLogin(true)}
                          className="text-[#0e3175] font-medium hover:underline transition-all hover:-translate-y-0.5"
                        >
                          Se connecter
                        </button>
                      </>
                    )}
                  </p>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
