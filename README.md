# Fake Weather Flask App for AWS Lambda

## Description
A simple Flask application that displays fake weather data for a list of cities. It's designed to be deployable on AWS Lambda. The app presents a web page showing city names, their weather conditions, and temperatures.

## Running Locally

1.  **Create and activate a Python virtual environment:**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Flask application:**
    You might need to set the `FLASK_APP` environment variable first:
    *   On macOS/Linux: `export FLASK_APP=app/app.py`
    *   On Windows: `set FLASK_APP=app/app.py`

    Then run:
    ```bash
    flask run
    ```
    Alternatively, you can run `python -m flask run --debug` (the `--debug` flag enables debug mode).

4.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Packaging for AWS Lambda

To deploy this application to AWS Lambda, you need to create a deployment package (`.zip` file).

1.  **Create a `package` directory:**
    ```bash
    mkdir package
    ```

2.  **Install dependencies into the `package` directory:**
    ```bash
    pip install -r requirements.txt -t ./package
    ```

3.  **Copy your application code into the `package` directory:**
    *   On macOS/Linux:
        ```bash
        cp -r app/* ./package/
        # If you have static and template files directly under app/, ensure they are copied too.
        # For this project structure, app/* should be sufficient.
        # If app.py was in the root, you would also do: cp app.py ./package/
        ```
    *   On Windows (using Command Prompt):
        ```bash
        xcopy app .\package /E /I /Y
        # If app.py was in the root, you would also do: xcopy app.py .\package /Y
        ```
    *   On Windows (using PowerShell):
        ```powershell
        Copy-Item -Path app\* -Destination .\package\ -Recurse -Force
        # If app.py was in the root, you would also do: Copy-Item -Path app.py -Destination .\package\ -Force
        ```
    *Ensure your `app.py` and any directories like `templates` are inside the `package` directory.*
    For this project, all application code is under the `app` directory, so copying `app/*` (or its contents) is key. The `lambda_handler` is in `app/app.py`.

4.  **Create the ZIP file:**
    Navigate into the `package` directory and zip its contents.
    *   On macOS/Linux:
        ```bash
        cd package
        zip -r ../lambda_package.zip .
        cd ..
        ```
    *   On Windows (using PowerShell):
        ```powershell
        Compress-Archive -Path .\package\* -DestinationPath .\lambda_package.zip -Force
        ```
        (Note: For PowerShell, ensure you are zipping the *contents* of the `package` directory, not the directory itself if the handler path is set to `app.lambda_handler`.)

5.  **Upload to AWS Lambda:**
    *   Upload the generated `lambda_package.zip` to your AWS Lambda function.
    *   Set the Lambda runtime to a compatible Python version (e.g., Python 3.8, 3.9, 3.10, etc.).
    *   Set the Lambda handler to `app.lambda_handler`. This tells Lambda to look for a file named `app.py` (which will be at the root of the zip) and a function named `lambda_handler` within that file.

This `README.md` provides instructions for both local development and AWS Lambda deployment.
Remember to deactivate your virtual environment when you're done: `deactivate`.
