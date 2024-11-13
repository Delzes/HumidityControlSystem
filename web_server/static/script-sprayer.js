async function fetchSprayer() {
    const response = await fetch('/get_sprayer');
    const data = await response.json();
    document.getElementById("currentSprayer").textContent = data.sprayer;
}

setInterval(fetchSprayer, 2000);  // Обновление влажности каждые 5 секунд

document.getElementById("sprayerThresholdForm").onsubmit = async function(e) {
    e.preventDefault();
    const sprayer_threshold = document.getElementById("sprayer_threshold").value;

    const response = await fetch('/update_sprayer_threshold', {
        method: 'POST',
        body: new URLSearchParams({ 'sprayer_threshold': sprayer_threshold }),
    });
    const data = await response.json();

    if (data.status === 'success') {
        alert("Threshold updated to: " + data.new_sprayer_threshold);
        document.getElementById("currentSprayerThreshold").textContent = data.new_sprayer_threshold;
    }
}