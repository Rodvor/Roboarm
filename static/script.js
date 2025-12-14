const servos = [
    "base",
    "shoulder",
    "elbow",
    "forearm",
    "wrist",
    "end_effector_base"
];

servos.forEach(name => {
    const slider = document.getElementById(name);
    const value = document.getElementById(name + "_value");

    slider.addEventListener("input", () => {
        value.textContent = slider.value;
    });
});

function sendMove() {
    const payload = {};

    servos.forEach(name => {
        payload[name] = document.getElementById(name).value;
    });

    payload["duration"] = document.getElementById("duration").value;

    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}
