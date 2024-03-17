# Flask App

This is a Flask application that displays a block of text with various parameters and provides an API endpoint to update those parameters.

## Project Structure

```
flask-app
├── app.py
├── templates
│   └── index.html
├── static
│   └── css
│       └── style.css
├── api
│   └── update_parameters.py
└── README.md
```

## Files

### `app.py`

This file is the main entry point of the Flask application. It sets up the Flask app, defines routes, and handles requests. It imports the necessary modules and functions from Flask and other files.

### `templates/index.html`

This file is an HTML template that displays the block of text with the parameters. It uses placeholders or variables to dynamically update the values of the parameters.

### `static/css/style.css`

This file contains the CSS styles for the HTML page. It is used to customize the appearance of the block of text and other elements on the page.

### `api/update_parameters.py`

This file contains the API endpoint for updating the parameters in the block of text. It defines a route and handles the request to update the parameters. It may import necessary modules and functions to update the parameters.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/flask-app.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask application:

   ```bash
   python app.py
   ```

4. Access the application in your web browser at `http://localhost:5000`.

## API Endpoint

The API endpoint for updating the parameters is `/api/update-parameters`. You can send a POST request to this endpoint with the updated parameter values in the request body.

Example request:

```bash
POST /api/update-parameters
Content-Type: application/json

{
  "robot_ip_address": "192.168.1.100",
  "robot_id": "12345",
  "first_motor_speed": 50,
  "second_motor_speed": 75,
  "third_motor_speed": 100,
  "kicker_status": true,
  "battery_life": 80
}
```

The parameters will be updated in the block of text on the HTML page.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create a new issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.