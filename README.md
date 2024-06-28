# Rubies & Jewels

Welcome to Rubies & Jewels, a Django-based project for a jewelry shopping startup. This repository contains the source code for the Rubies & Jewels website, allowing customers to browse and purchase a variety of jewelry items.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- User authentication and authorization
- Product catalog with detailed descriptions and images
- Shopping cart and checkout process
- Order management for customers and administrators
- Search functionality to find products easily
- Responsive design for mobile and desktop views

## Requirements

- Python 3.10+
- Django 5.0+
- SQLite
- Virtualenv (optional but recommended)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mogomaa79/rubies_jewels.git
    cd rubies_jewels
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000` to see the website.

## Usage

- To access the admin panel, go to `http://127.0.0.1:8000/admin` and log in with your superuser credentials.
- Add new products, manage orders, and customize the website content through the admin panel.

## Contributing

We welcome contributions to enhance the Rubies & Jewels project! To contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them with clear and concise messages.
4. Push your changes to your fork.
5. Create a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or support, please contact us at:

- Email: support@rubiesjewels.com
- GitHub: [mogomaa79](https://github.com/mogomaa79)

We hope you enjoy using Rubies & Jewels! Happy shopping!

