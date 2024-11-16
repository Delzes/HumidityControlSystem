async function fetchTemperature() {
    const response = await fetch('/get_temperature');
    const data = await response.json();
    document.getElementById("currentTemperature").textContent = data.temperature;
}

setInterval(fetchTemperature, 2000);  // Обновление влажности каждые 5 секунд

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
    if (isNaN(min) || isNaN(max)) {
        alert("Оба значения должны быть числами!");
        return false;
    }
    if (min > max) {
        alert("Минимальное значение не может быть больше максимального!");
        return false;
    }
    return true;
}