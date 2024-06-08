# Social Network Assignment

This is a Django project for a social network assignment.

## Setup

### Local Setup

1. Clone the repository:
    ```
    git clone https://github.com/spk61023/social_network_assignment.git
    ```
2. Navigate to the project directory:
    ```
    cd social_network_assignment
    ```
3. Install the requirements:
    ```
    pip install -r requirements.txt
    ```
4. Run the migrations:
    ```
    python manage.py migrate
    ```
5. Start the server:
    ```
    python manage.py runserver
    ```

### Docker Setup

1. Install Docker: Download and install Docker from the official website: https://www.docker.com/get-started
2. Build the Docker image:
    ```
    docker build -t social_network_assignment .
    ```
3. Run the Docker container:
    ```
    docker run -p 8000:8000 social_network_assignment
    ```
