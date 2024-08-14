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

    var selectedPoint = null;
    var addProjectButton = document.getElementById('add-project-button');
    var mapOverlay = document.getElementById('map-overlay');
    var confirmPointBtn = document.getElementById('confirm-point-btn');
    var cancelSelectionBtn = document.getElementById('cancel-selection-btn');
    var buttonContainer = document.querySelector('.button-container');

    function onMapClick(e) {
        if (selectedPoint) {
            map.removeLayer(selectedPoint);
        }
        selectedPoint = L.marker(e.latlng).addTo(map);
        buttonContainer.style.display = 'flex'; // Показываем кнопки
        addProjectButton.style.display = 'none'; // Скрываем кнопку "Добавить объект"
    }

    if (addProjectButton) {
        addProjectButton.addEventListener('click', function () {
            mapOverlay.style.display = 'block';
            map.getContainer().style.cursor = 'crosshair';
            map.on('click', onMapClick);
        });
    }

    if (confirmPointBtn) {
        confirmPointBtn.addEventListener('click', function () {
            if (selectedPoint) {
                var latlng = selectedPoint.getLatLng();
                window.location.href = `/add_project/?lat=${latlng.lat}&lng=${latlng.lng}`;
            }
        });
    }

    if (cancelSelectionBtn) {
        cancelSelectionBtn.addEventListener('click', function () {
            if (selectedPoint) {
                map.removeLayer(selectedPoint);
                selectedPoint = null;
            }
            buttonContainer.style.display = 'none'; // Скрываем кнопки
            addProjectButton.style.display = 'block'; // Показываем кнопку "Добавить объект"
            map.getContainer().style.cursor = '';
            map.off('click', onMapClick);
            mapOverlay.style.display = 'none';
        });
    }

    // Функция для создания иконок маркеров
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

    // Группа для кластеризации маркеров
    var markers = L.markerClusterGroup();

    // Функция для загрузки маркеров на карту
    function loadMarkers(projects) {
        projects.forEach(function (project) {
            var fillColor = project.main_type__color;
            var strokeColor = project.main_type__category__color;
            var marker = L.marker([project.latitude, project.longitude], {
                icon: createDropIcon(fillColor, strokeColor)
            });
            var popupContent = `
                <div>
                    <h3>${project.title}</h3>
                    <a href="/project/${project.id}">Открыть объект</a>
                </div>`;
            marker.bindPopup(popupContent);
            markers.addLayer(marker);
        });
    }

    // Попытка загрузки маркеров
    try {
        loadMarkers(projects);
    } catch (error) {
        console.error("Ошибка при загрузке маркеров:", error);
    }

    // Добавление маркеров на карту
    map.addLayer(markers);

    // Функция обновления маркеров
    window.updateMarkers = function (data) {
        markers.clearLayers();
        try {
            loadMarkers(data);
        } catch (error) {
            console.error("Ошибка при обновлении маркеров:", error);
        }
    };
});
