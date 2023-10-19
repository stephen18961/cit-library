# Library App

Welcome to the Library App repository! This Flask project is designed to help you manage and organize your personal library collection. Whether you're an avid reader, a book enthusiast, or a librarian, this app will make it easy to keep track of your books, their details, and their availability.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:** Securely manage your library with user authentication and authorization.
- **Book Catalog:** Add, edit, and delete books in your collection.
- **Book Details:** Store essential book information, including title, author, and genre.
- **Availability:** Keep track of the availability status of each book.
- **Filter:** Easily filter your library by various criteria.
- **Responsive Design:** Enjoy a responsive web interface for various devices.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11+
- MySQL Database
### Installation


1. Create a new virtual environment:

    ```shell
    python -m venv .venv
    .venv\scripts\activate
    ```

2. Install project dependencies using PIP:

    ```shell
    pip install -r requirements.txt
    ```

3. Create the database and apply migrations:

    ```shell
    flask db init
    flask db migrate
    flask db upgrade
    ```

4. Start the development server:

    ```shell
    flask run
    ```

Now, you can access the application by opening your web browser and navigating to [http://localhost:5001](http://localhost:5001).

## Usage

- Visit the web application at [http://localhost:5001](http://localhost:5001).
- Sign up and log in to start managing your library collection.
- Add books, update book details, and mark their availability.
- Search and filter your library to find the books you're interested in.

## Contributing

We welcome contributions from the open-source community! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them thoroughly.
4. Ensure your code follows the project's coding style.
5. Create a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Happy reading and library management! If you have any questions or encounter issues, please feel free to open an issue or reach out to us.
