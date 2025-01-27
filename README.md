# Andreia Teofilo Confeitaria - FastAPI Application

This repository contains a FastAPI application for managing a confectionery business. The application provides endpoints for user registration, login, client management, and order management.

## Endpoints

### Root

- `GET /`
  - Renders the index page.

### Authentication

- `GET /login`
  - Renders the login page.

- `GET /register`
  - Renders the registration page.

- `POST /register`
  - Registers a new user.
  - Parameters: `usuario`, `email`, `senha`, `senha_confirmar`

- `POST /login`
  - Logs in a user.
  - Parameters: `usuario`, `senha`

### Clients

- `GET /clientes`
  - Retrieves all clients.

- `POST /clientes/criar`
  - Creates a new client.
  - Parameters: `ClienteBase`

- `GET /clientes/{cliente_id}`
  - Retrieves a client by ID.
  - Parameters: `cliente_id`

- `PUT /clientes/{cliente_id}`
  - Updates client data.
  - Parameters: `cliente_id`, `ClienteBase`

### Orders

- `POST /encomendas`
  - Creates a new order.
  - Parameters: `EncomendaBase`, `ClienteBase`

- `GET /encomendas`
  - Retrieves all orders.

- `GET /encomendas/{encomenda_id}`
  - Retrieves an order by ID.
  - Parameters: `encomenda_id`

- `DELETE /encomendas/delete/{encomenda_id}`
  - Deletes an order by ID.
  - Parameters: `encomenda_id`

- `PUT /encomendas/{encomenda_id}`
  - Updates an order by ID.
  - Parameters: `encomenda_id`, `EncomendaBase`

## Dependencies

- FastAPI
- Jinja2Templates
- argon2

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/GalderioJaguara/target-teste-js.git
    ```
2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

## License

This project is licensed under the MIT License.
