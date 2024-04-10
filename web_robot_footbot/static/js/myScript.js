// const spanIds = Array.from(document.getElementsByTagName('span')).map(span => span.id);

function updateParameters() {
    const id = ['_0','_1','_2','_3','_4'];
    for(let i=0; i<5; i++){
        fetch('/get_parameters' + id[i])
        .then(response => response.json())
        .then(data => {
            document.getElementById('status'+id[i]).textContent = data.status;
            document.getElementById('ip_address'+id[i]).textContent = data.robot_ip_address;
            document.getElementById('robot_id'+id[i]).textContent = data.robot_id;
            document.getElementById('first_motor_speed'+id[i]).textContent = data.first_motor_speed;
            document.getElementById('second_motor_speed'+id[i]).textContent = data.second_motor_speed;
            document.getElementById('third_motor_speed'+id[i]).textContent = data.third_motor_speed;
            document.getElementById('kicker_status'+id[i]).textContent = data.kicker_status;
            document.getElementById('battery_life'+id[i]).textContent = data.battery_life;
        });

        const text = document.getElementById('status'+id[i]);
        if(text.textContent === 'Connected'){
            text.style.color = 'green';
        } else {
            text.style.color = 'red';
        }
    }
}

// Call updateParameters every second
setInterval(updateParameters, 1000);