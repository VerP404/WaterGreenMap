document.addEventListener('DOMContentLoaded', function () {
    var map = L.map('map').setView([55.755811, 37.617617], 5);

    var streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var satelliteLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    map.zoomControl.setPosition('topright');

    L.control.locate({
        position: 'topright',
        strings: {
            title: "Показать мое местоположение"
        },
        locateOptions: {
            maxZoom: 16
        }
    }).addTo(map);

    var controlLayers = L.control.layers({
        'карта 1': streetLayer,
        'карта 2': satelliteLayer
    }, {}, {
        position: 'topright'
    }).addTo(map);

    var selectedPoint = null;
    var addProjectButton = document.getElementById('add-project-button');
    var mapOverlay = document.getElementById('map-overlay');
    var confirmPointBtn = document.getElementById('confirm-point-btn');

    function onMapClick(e) {
        if (selectedPoint) {
            map.removeLayer(selectedPoint);
        }
        selectedPoint = L.marker(e.latlng).addTo(map);
        confirmPointBtn.style.display = 'block';
    }

    addProjectButton.addEventListener('click', function () {
        mapOverlay.style.display = 'block';
        map.getContainer().style.cursor = 'crosshair';
        map.on('click', onMapClick);
    });

    confirmPointBtn.addEventListener('click', function () {
        if (selectedPoint) {
            var latlng = selectedPoint.getLatLng();
            window.location.href = `/add_project/?lat=${latlng.lat}&lng=${latlng.lng}`;
        }
    });

    function createDropIcon(fillColor, strokeColor) {
        return L.divIcon({
            html: `
                <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 0C9.82 0 4 9.92 4 13.92 4 17.74 7.22 21 12 21s8-3.26 8-7.08C20 9.92 14.18 0 12 0z"
                          fill="${fillColor}" stroke="${strokeColor}" stroke-width="2"/>
                </svg>`,
            className: '',
            iconSize: [24, 24],
            iconAnchor: [12, 24]
        });
    }

    var markers = L.markerClusterGroup();

    if (projects.length > 0) {
        projects.forEach(function (project) {
            var fillColor = project.main_type__color;
            var strokeColor = project.main_type__category__color;
            var marker = L.marker([project.latitude, project.longitude], {
                icon: createDropIcon(fillColor, strokeColor)
            });
            marker.bindPopup(`<b>${project.title}</b><br>${project.description}`);
            markers.addLayer(marker);
        });
    }

    map.addLayer(markers);

    window.updateMarkers = function(data) {
        markers.clearLayers();
        data.forEach(function (project) {
            var fillColor = project.main_type__color;
            var strokeColor = project.main_type__category__color;
            var marker = L.marker([project.latitude, project.longitude], {
                icon: createDropIcon(fillColor, strokeColor)
            });
            marker.bindPopup(`<b>${project.title}</b><br>${project.description}`);
            markers.addLayer(marker);
        });
    }
});
