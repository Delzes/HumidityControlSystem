async function fetchLight() {
    const response = await fetch('/get_light');
    const data = await response.json();
    document.getElementById("currentLight").textContent = data.light;
}

setInterval(fetchLight, 2000);  // Обновление влажности каждые 5 секунд

document.getElementById("lightThresholdForm").onsubmit = async function(e) {
    e.preventDefault();
    const light_threshold = document.getElementById("light_threshold").value;

    const response = await fetch('/update_light_threshold', {
        method: 'POST',
        body: new URLSearchParams({ 'light_threshold': light_threshold }),
    });
    const data = await response.json();

    if (data.status === 'success') {
        alert("Threshold updated to: " + data.new_light_threshold);
        document.getElementById("currentLightThreshold").textContent = data.new_light_threshold;
    }
}