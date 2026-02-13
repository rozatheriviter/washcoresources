document.addEventListener('DOMContentLoaded', () => {
    // Initialize the map centered on Washington County, OR
    // Hillsboro/Beaverton area is roughly 45.5, -122.9
    const map = L.map('map').setView([45.48, -122.9], 11);

    // Add Tile Layer (CartoDB Positron for a cleaner, brand-aligned look)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Define custom marker icon (Deep Forest Green)
    const customIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: #2A4434; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #FDFCF8; box-shadow: 0 2px 5px rgba(0,0,0,0.4);"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],
        popupAnchor: [0, -7]
    });

    // Add markers for resources with geodata
    if (typeof resources !== 'undefined') {
        resources.forEach(resource => {
            if (resource.lat && resource.lng) {
                const categories = Array.isArray(resource.category) ? resource.category.join(', ') : resource.category;

                const popupContent = `
                    <div style="font-family: 'Inter', sans-serif;">
                        <div class="popup-category">${categories}</div>
                        <h3 style="margin: 4px 0 8px; font-size: 1.1rem; font-family: 'Merriweather', serif; color: #2A4434;">${resource.name}</h3>
                        <p style="margin: 4px 0; font-size: 0.9rem; color: #5C6B5F;"><strong>Address:</strong> ${resource.address}</p>
                        ${resource.phone ? `<p style="margin: 4px 0; font-size: 0.9rem; color: #5C6B5F;"><strong>Phone:</strong> ${resource.phone}</p>` : ''}
                        <div style="margin-top: 12px; display: flex; gap: 12px;">
                            <a href="index.html?search=${encodeURIComponent(resource.name)}" class="popup-link" style="color: #2A4434; font-weight: 600; text-decoration: none; border-bottom: 2px solid #E8C547;">View Details</a>
                            ${resource.website ? `<a href="${resource.website}" target="_blank" class="popup-link" style="color: #2A4434; font-weight: 600; text-decoration: none; border-bottom: 2px solid #E8C547;">Website</a>` : ''}
                        </div>
                    </div>
                `;

                L.marker([resource.lat, resource.lng], { icon: customIcon })
                    .addTo(map)
                    .bindPopup(popupContent);
            }
        });
    } else {
        console.error('Resources not loaded');
    }
});
