async function fetchLight() {
    const response = await fetch('/get_light');
    const data = await response.json();
    document.getElementById("currentLight").textContent = data.light;
}

async function GetLightStatus() {
    const response = await fetch('/get_light_status');
    const data = await response.json();
    const statusElement = document.getElementById("statusLight");
    const statusBtn = document.getElementById("lightStatusBtn");
    statusElement.textContent = data.lightStatus;
    statusElement.classList.remove("status_off", "status_on");
        if (data.lightStatus === "OFF") {
            statusElement.classList.add("status_off");
            statusBtn.classList.remove("switch-on");
        } else if (data.lightStatus === "ON") {
            statusElement.classList.add("status_on");
            statusBtn.classList.add("switch-on");
        }
}

setInterval(fetchLight, 2000);
setInterval(GetLightStatus, 2100);

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