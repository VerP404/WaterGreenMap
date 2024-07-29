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
});
