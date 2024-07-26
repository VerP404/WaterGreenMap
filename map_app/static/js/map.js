document.addEventListener('DOMContentLoaded', function () {
    // Инициализация карты Leaflet
    var map = L.map('map').setView([55.755811, 37.617617], 5);

    // Добавление тайл-слоев OpenStreetMap и спутникового слоя
    var streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var satelliteLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    // Позиционирование элементов управления зумом
    map.zoomControl.setPosition('topright');

    // Добавление элемента управления местоположением
    L.control.locate({
        position: 'topright',
        strings: {
            title: "Показать мое местоположение"
        },
        locateOptions: {
            maxZoom: 16
        }
    }).addTo(map);

    // Добавление элемента управления для переключения между уличной и спутниковой картой
    var controlLayers = L.control.layers({
        'карта 1': streetLayer,
        'карта 2': satelliteLayer
    }, {}, {
        position: 'topright'
    }).addTo(map);


    // Экспорт функций для внешнего использования
    window.myMap = map;

});
