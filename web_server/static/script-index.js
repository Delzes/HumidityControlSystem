async function fetchHumidity() {
    const response = await fetch('/get_humidity');
    const data = await response.json();
    document.getElementById("currentHumidity").textContent = data.humidity;
}

async function GetFanStatus() {
    const response = await fetch('/get_fan_status');
    const data = await response.json();
    const statusElement = document.getElementById("statusFan");
    const statusBtn = document.getElementById("fanStatusBtn");
    statusElement.textContent = data.fanStatus;
    statusElement.classList.remove("status_off", "status_on");
        if (data.fanStatus === "OFF") {
            statusElement.classList.add("status_off");
            statusBtn.classList.remove("switch-on");
        } else if (data.fanStatus === "ON") {
            statusElement.classList.add("status_on");
            statusBtn.classList.add("switch-on");
        }
}

setInterval(fetchHumidity, 2000);
setInterval(GetFanStatus, 2100);

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