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

    document.getElementById('addObjectButton').addEventListener('click', function () {
        map.once('click', function (e) {
            var lat = e.latlng.lat;
            var lng = e.latlng.lng;
            window.location.href = `/projects/add/${lat}/${lng}`;
        });
    });
});
