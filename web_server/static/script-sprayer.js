async function fetchSprayer() {
    const response = await fetch('/get_sprayer');
    const data = await response.json();
    document.getElementById("currentSprayer").textContent = data.sprayer;
}

async function GetSprayerStatus() {
    const response = await fetch('/get_sprayer_status');
    const data = await response.json();
    const statusElement = document.getElementById("statusSprayer");
    const statusBtn = document.getElementById("sprayerStatusBtn");
    statusElement.textContent = data.sprayerStatus;
    statusElement.classList.remove("status_off", "status_on");
        if (data.sprayerStatus === "OFF") {
            statusElement.classList.add("status_off");
            statusBtn.classList.remove("switch-on");
        } else if (data.sprayerStatus === "ON") {
            statusElement.classList.add("status_on");
            statusBtn.classList.add("switch-on");
        }
}

setInterval(fetchSprayer, 2000);
setInterval(GetSprayerStatus, 2100);

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