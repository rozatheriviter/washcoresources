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
                    <div class="map-popup">
                        <div class="popup-category">${categories}</div>
                        <h3>${resource.name}</h3>
                        <p><strong>Address:</strong> ${resource.address}</p>
                        ${resource.phone ? `<p><strong>Phone:</strong> ${resource.phone}</p>` : ''}
                        <div class="popup-actions">
                            <a href="index.html?search=${encodeURIComponent(resource.name)}" class="popup-link">View Details</a>
                            ${resource.website ? `<a href="${resource.website}" target="_blank" class="popup-link">Website</a>` : ''}
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
