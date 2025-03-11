
import { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface Site {
  name: string;
  coordinates: [number, number];
  status: 'online' | 'offline' | 'warning';
}

const SitesMap = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);

  const sites: Site[] = [
    { name: "Site Paris Centre", coordinates: [2.3522, 48.8566], status: 'online' },
    { name: "Site Lyon Sud", coordinates: [4.8357, 45.7640], status: 'online' },
    { name: "Site Marseille Port", coordinates: [5.3698, 43.2965], status: 'offline' },
    { name: "Site Bordeaux Nord", coordinates: [0.5792, 44.8378], status: 'online' },
    { name: "Site Lille Centre", coordinates: [3.0573, 50.6292], status: 'online' },
    { name: "Site Nantes Est", coordinates: [-1.5534, 47.2184], status: 'warning' }
  ];

  useEffect(() => {
    if (!mapContainer.current) return;
    if (map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm': {
            type: 'raster',
            tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap Contributors',
            maxzoom: 19
          }
        },
        layers: [{
          id: 'osm',
          type: 'raster',
          source: 'osm',
          minzoom: 0,
          maxzoom: 19
        }]
      },
      center: [2.3522, 46.8566], // Centre de la France
      zoom: 5,
      pitch: 0,
      bearing: 0
    });

    // Ajout des contrôles de navigation
    map.current.addControl(new maplibregl.NavigationControl(), 'top-right');

    const addMarkers = () => {
      sites.forEach((site) => {
        // Création du marker personnalisé
        const el = document.createElement('div');
        el.className = 'custom-marker';
        const color = site.status === 'online' ? '#22c55e' : 
                     site.status === 'offline' ? '#ef4444' : '#f59e0b';
        
        el.style.cssText = `
          background-color: ${color};
          width: 16px;
          height: 16px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
          cursor: pointer;
        `;

        // Ajout du popup avec un style amélioré
        const popup = new maplibregl.Popup({ 
          offset: 25,
          closeButton: false,
          className: 'custom-popup'
        }).setHTML(`
          <div class="p-3 bg-white rounded-lg shadow-lg">
            <h3 class="font-semibold text-gray-800">${site.name}</h3>
            <p class="text-sm text-gray-600 mt-1">
              Statut: 
              <span class="font-medium ${
                site.status === 'online' ? 'text-green-600' :
                site.status === 'offline' ? 'text-red-600' : 'text-amber-600'
              }">
                ${
                  site.status === 'online' ? 'En ligne' :
                  site.status === 'offline' ? 'Hors ligne' : 'Attention'
                }
              </span>
            </p>
          </div>
        `);

        // Ajout du marker à la carte
        new maplibregl.Marker(el)
          .setLngLat(site.coordinates)
          .setPopup(popup)
          .addTo(map.current!);
      });
    };

    map.current.on('load', addMarkers);

    return () => {
      map.current?.remove();
    };
  }, []);

  return (
    <div style={{ height: '400px', width: '100%', borderRadius: '0.5rem', overflow: 'hidden' }}>
      <div ref={mapContainer} style={{ height: '100%', width: '100%' }} />
    </div>
  );
};

export default SitesMap;
