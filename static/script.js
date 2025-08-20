document.addEventListener("DOMContentLoaded", function () {
    const servoControls = document.getElementById("servoControls");
    const status = document.getElementById("status");
    const numServos = 7;

    function createServoUI(id) {
        const container = document.createElement("div");
        container.className = "servo-container";

        container.innerHTML = `
            <h2>Servo ${id}</h2>
            <label>Angle: <span id="angleValue${id}">135</span>°</label>
            <input type="range" id="angle${id}" min="0" max="270" value="135">
            <br>
            <label>Speed: <span id="speedValue${id}">10</span> ms/°</label>
            <input type="range" id="speed${id}" min="0" max="100" value="10">
        `;

        servoControls.appendChild(container);

        const angleSlider = container.querySelector(`#angle${id}`);
        const speedSlider = container.querySelector(`#speed${id}`);
        const angleValue = container.querySelector(`#angleValue${id}`);
        const speedValue = container.querySelector(`#speedValue${id}`);

        function sendCommand() {
            const angle = angleSlider.value;
            const speed = speedSlider.value;
            angleValue.textContent = angle;
            speedValue.textContent = speed;

            status.textContent = `Servo ${id} → Angle: ${angle}°, Speed: ${speed} ms/°`;

            fetch(`/move?servo=${id}&angle=${angle}&speed=${speed}`)
                .then(response => {
                    if (!response.ok) {
                        status.textContent = `Error sending command to servo ${id}`;
                    }
                })
                .catch(() => {
                    status.textContent = "Connection error";
                });
        }

        angleSlider.addEventListener("input", sendCommand);
        speedSlider.addEventListener("input", sendCommand);
    }

    for (let i = 1; i <= numServos; i++) {
        createServoUI(i);
    }
});
