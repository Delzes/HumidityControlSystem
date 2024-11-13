async function fetchHumidity() {
    const response = await fetch('/get_humidity');
    const data = await response.json();
    document.getElementById("currentHumidity").textContent = data.humidity;
}

setInterval(fetchHumidity, 2000);  // Обновление влажности каждые 5 секунд

document.getElementById("thresholdForm").onsubmit = async function(e) {
    e.preventDefault();
    const threshold = document.getElementById("threshold").value;

    const response = await fetch('/update_threshold', {
        method: 'POST',
        body: new URLSearchParams({ 'threshold': threshold }),
    });

    const data = await response.json();

    if (data.status === 'success') {
        alert("Threshold updated to: " + data.new_threshold);
        document.getElementById("currentThreshold").textContent = data.new_threshold;
    }
}