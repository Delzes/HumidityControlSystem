async function fetchTemperature() {
    const response = await fetch('/get_temperature');
    const data = await response.json();
    document.getElementById("currentTemperature").textContent = data.temperature;
}
document.getElementById("temperatureThresholdFormMin").onsubmit = async function(e) {
    e.preventDefault();
    const temperature_threshold_min = document.getElementById("temperature_threshold_min").value;

    const response = await fetch('/update_temperature_threshold_min', {
        method: 'POST',
        body: new URLSearchParams({ 'temperature_threshold_min': temperature_threshold_min }),
    });
    const data = await response.json();

    if (data.status === 'success') {
        alert("Threshold updated to: " + data.new_temperature_threshold_min);
        document.getElementById("currentTemperatureThresholdMin").textContent = data.new_temperature_threshold_min;
    }
}

document.getElementById("temperatureThresholdFormMax").onsubmit = async function(e) {
    e.preventDefault();
    const temperature_threshold_max = document.getElementById("temperature_threshold_max").value;

    const response = await fetch('/update_temperature_threshold_max', {
        method: 'POST',
        body: new URLSearchParams({ 'temperature_threshold_max': temperature_threshold_max }),
    });
    const data = await response.json();

    if (data.status === 'success') {
        alert("Threshold updated to: " + data.new_temperature_threshold_max);
        document.getElementById("currentTemperatureThresholdMax").textContent = data.new_temperature_threshold_max;
    }
}

function validateThresholds() {
    const minInput = document.getElementById('temperature_threshold_min');
    const maxInput = document.getElementById('temperature_threshold_max');
    const min = parseFloat(minInput.value);
    const max = parseFloat(maxInput.value);
    if (min > max) {
        minInput.setCustomValidity("Минимальное значение не может быть больше максимального!");
        maxInput.setCustomValidity("Максимальное значение не может быть меньше минимального!");
    } else {
        minInput.setCustomValidity("");
        maxInput.setCustomValidity("");
    }
}

let temperatureData = [];

const ctx = document.getElementById('temperatureChart').getContext('2d');
const temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Температура (°C)',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 1)',
            borderColor: 'rgba(75, 192, 192, 1)',
            pointRadius: 5,
        }]
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Время (секунды)'
                },
                ticks: {
                    callback: function(value) {
                        const date = new Date(value);
                        return date.toLocaleTimeString();
                    }
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Температура (°C)'
                }
            }
        }
    }
});


async function updateTemperatureChart() {
    const response = await fetch('/temperature/history');
    const history = await response.json();

    const now = Date.now();
    temperatureData = history.map((temp, index) => ({
        x: now - (history.length - 1 - index) * 5000,
        y: temp,
    }));
    temperatureChart.data.datasets[0].data = temperatureData;
    temperatureChart.update();
}



let temperature_threshold_min = document.getElementById("temperature_threshold_min").value;
let temperature_threshold_max = document.getElementById("temperature_threshold_max").value;
const addedRecords = JSON.parse(localStorage.getItem('addedRecords')) || [];

function updateTemperatureTable(temperature, timestamp) {
    const tableBody = document.getElementById('temperatureTable').querySelector('tbody');

    const dateObj = new Date(timestamp);
    const date = dateObj.toLocaleDateString(); // Формат: ДД.ММ.ГГГГ
    const time = dateObj.toLocaleTimeString(); // Формат: ЧЧ:ММ:СС

    const roundedTemp = temperature.toFixed(1);
    if (addedRecords.some(record => record.temperature === roundedTemp && record.timestamp === timestamp)) {
        return;
    }
    addedRecords.push({ temperature: roundedTemp, timestamp });
    localStorage.setItem('addedRecords', JSON.stringify(addedRecords));

    const row = `
        <tr>
            <td>${date}</td>
            <td>${time}</td>
            <td>${roundedTemp}°C</td>
        </tr>
    `;

    tableBody.insertAdjacentHTML('beforeend', row);
}

async function checkTemperatureThresholds() {
    const response = await fetch('/get_temperature');
    const data = await response.json();
    const currentTemperature = data.temperature;

    const timestamp = Date.now();
    if (currentTemperature > temperature_threshold_max || currentTemperature < temperature_threshold_min) {
        updateTemperatureTable(currentTemperature, timestamp);
    }
}

function loadSavedData() {
    const tableBody = document.getElementById('temperatureTable').querySelector('tbody');
    addedRecords.forEach(record => {
        const dateObj = new Date(record.timestamp);
        const date = dateObj.toLocaleDateString();
        const time = dateObj.toLocaleTimeString();
        const row = `
            <tr>
                <td>${date}</td>
                <td>${time}</td>
                <td>${record.temperature}°C</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

const clearStorageButton = document.getElementById('clearStorageButton');

clearStorageButton.addEventListener('click', () => {
    localStorage.clear();
    const tableBody = document.getElementById('temperatureTable').querySelector('tbody');
    tableBody.innerHTML = '';
    addedRecords.length = 0;
});

setInterval(fetchTemperature, 4000);
setInterval(updateTemperatureChart, 3000);
setInterval(checkTemperatureThresholds, 5000);
window.onload = loadSavedData;