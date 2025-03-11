import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useState } from "react";
import { CreditCard, Wallet, UserIcon, LogOut } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/components/AuthProvider";
import { useNavigate } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const Settings = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      logout();
      toast.success("Déconnexion réussie");
      navigate('/');
    } catch (error: any) {
      console.error("Erreur lors de la déconnexion:", error);
      toast.error("Un problème est survenu lors de la déconnexion.");
    }
  };

  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState<"card" | "paypal" | null>(null);
  const [siteCount, setSiteCount] = useState(3);
  const [cardInfo, setCardInfo] = useState({
    number: "",
    name: "",
    expiry: "",
    cvc: ""
  });
  const [paypalInfo, setPaypalInfo] = useState({
    email: ""
  });

  const pricePerSite = 15;
  const totalHT = siteCount * pricePerSite;
  const totalTTC = totalHT * 1.2; // TVA 20%

  const handlePayment = () => {
    if (!selectedPaymentMethod) {
      toast.error("Veuillez sélectionner une méthode de paiement");
      return;
    }

    if (selectedPaymentMethod === "card" && (!cardInfo.number || !cardInfo.name || !cardInfo.expiry || !cardInfo.cvc)) {
      toast.error("Veuillez remplir tous les champs de la carte");
      return;
    }

    if (selectedPaymentMethod === "paypal" && !paypalInfo.email) {
      toast.error("Veuillez remplir votre email PayPal");
      return;
    }

    toast.success("Paiement simulé avec succès !");
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Souscription</h1>
          <p className="text-muted-foreground">
            Gérez votre abonnement
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm">Global Secure SARL</span>
          <DropdownMenu>
            <DropdownMenuTrigger className="focus:outline-none">
              <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center hover:bg-secondary/80 transition-colors">
                <UserIcon className="w-4 h-4 text-muted-foreground" />
              </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleLogout} className="text-red-600 focus:text-red-600 focus:bg-red-50">
                <LogOut className="w-4 h-4 mr-2" />
                Se déconnecter
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      <div className="grid gap-4">
        <Card className="p-6 glass">
          <h2 className="text-lg font-semibold mb-4">Abonnement et Facturation</h2>
          <div className="space-y-6">
            <div className="bg-muted/50 p-4 rounded-lg">
              <h3 className="font-medium mb-2">Résumé de l'abonnement</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Nombre de sites</span>
                  <span>{siteCount}</span>
                </div>
                <div className="flex justify-between">
                  <span>Prix par site / mois</span>
                  <span>{pricePerSite}€ HT</span>
                </div>
                <div className="flex justify-between font-medium">
                  <span>Total HT / mois</span>
                  <span>{totalHT}€</span>
                </div>
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>TVA (20%)</span>
                  <span>{(totalTTC - totalHT).toFixed(2)}€</span>
                </div>
                <div className="flex justify-between font-semibold text-lg pt-2 border-t">
                  <span>Total TTC / mois</span>
                  <span>{totalTTC.toFixed(2)}€</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-medium">Méthode de paiement</h3>
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setSelectedPaymentMethod("card")}
                  className={`p-4 border rounded-lg flex items-center gap-3 hover:border-primary transition-colors ${
                    selectedPaymentMethod === "card" ? "border-primary bg-primary/5" : ""
                  }`}
                >
                  <CreditCard className="w-5 h-5" />
                  <span>Carte bancaire</span>
                </button>
                <button
                  onClick={() => setSelectedPaymentMethod("paypal")}
                  className={`p-4 border rounded-lg flex items-center gap-3 hover:border-primary transition-colors ${
                    selectedPaymentMethod === "paypal" ? "border-primary bg-primary/5" : ""
                  }`}
                >
                  <Wallet className="w-5 h-5" />
                  <span>PayPal</span>
                </button>
              </div>

              {selectedPaymentMethod === "card" && (
                <div className="space-y-4 border rounded-lg p-4">
                  <div className="space-y-2">
                    <Label htmlFor="cardNumber">Numéro de carte</Label>
                    <Input
                      id="cardNumber"
                      placeholder="4242 4242 4242 4242"
                      value={cardInfo.number}
                      onChange={(e) => setCardInfo({...cardInfo, number: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="cardName">Nom sur la carte</Label>
                    <Input
                      id="cardName"
                      placeholder="JOHN DOE"
                      value={cardInfo.name}
                      onChange={(e) => setCardInfo({...cardInfo, name: e.target.value})}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="cardExpiry">Date d'expiration</Label>
                      <Input
                        id="cardExpiry"
                        placeholder="MM/AA"
                        value={cardInfo.expiry}
                        onChange={(e) => setCardInfo({...cardInfo, expiry: e.target.value})}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="cardCVC">CVC</Label>
                      <Input
                        id="cardCVC"
                        placeholder="123"
                        value={cardInfo.cvc}
                        onChange={(e) => setCardInfo({...cardInfo, cvc: e.target.value})}
                      />
                    </div>
                  </div>
                </div>
              )}

              {selectedPaymentMethod === "paypal" && (
                <div className="space-y-4 border rounded-lg p-4">
                  <div className="space-y-2">
                    <Label htmlFor="paypalEmail">Email PayPal</Label>
                    <Input
                      id="paypalEmail"
                      type="email"
                      placeholder="john.doe@example.com"
                      value={paypalInfo.email}
                      onChange={(e) => setPaypalInfo({...paypalInfo, email: e.target.value})}
                    />
                  </div>
                </div>
              )}

              <Button onClick={handlePayment} className="w-full">
                Payer {totalTTC.toFixed(2)}€
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Settings;
