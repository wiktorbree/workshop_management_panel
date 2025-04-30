# 🛠️ Serwis Samochodowy — Management Panel

Welcome to **Serwis Samochodowy — Panel Zarządzania**!

This project is a web-based management panel designed to streamline automotive service operations. It provides an intuitive interface for handling key service-related tasks, including managing orders, customers, vehicles, parts, and employees — all in one place.

This system is built using Python and the Reflex library, and it is **still in active development**.

> 🏫 This project was created as part of my studies at university.
---

## ✨ Features

- **Dashboard:** A centralized overview with easy navigation to key functionalities.
- **Order Management:** View and manage service orders efficiently.
- **Customer Management:** Keep a list of your customers and their details.
- **Vehicle Management:** Maintain a record of all vehicles associated with your services.
- **Parts Inventory:** Manage and track inventory for parts in your warehouse.
- **Employee Directory:** Organize and access employee information quickly.

---

## 🚀 Tech Stack

The project is built using **[Reflex](https://reflex.dev)**, a Python framework for developing modern reactive UI applications. It follows a component-based design, ensuring modularity and reusability of UI elements.

### Key Python Libraries:
- **`reflex`**: Used for reactive user interface development.
- **Custom UI Components**: Navbar and gradient button components were designed specifically for the project.

---

## 🖥️ Running the Project Locally

Follow these steps to run the project on your development machine:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install reflex
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   reflex run
   ```

   The app should now be available at [http://localhost:8000](http://localhost:8000).

---

## 📂 Project Structure

- **`SerwisUI.py`**: The main application that defines the UI pages and routes.
- **`UI/`**: Contains reusable UI elements such as the navigation bar and buttons.
- **`Pages/`**: Contains modules for each page (Orders, Customers, Vehicles, etc.).

---

## 🗺️ Navigation

The application includes the following pages for streamlined management:

| Page               | Route          |
|--------------------|----------------|
| Home               | `/`            |
| Customers          | `/klienci`     |
| Vehicles           | `/pojazdy`     |
| Inventory (Parts)  | `/magazyn`     |
| Employees          | `/pracownicy`  |
| Service Orders     | `/zlecenie`    |
| Parts              | `/czesci`      |


---

## 🛠️ Future Plans
- Add the ability to edit the database.
- Add a reporting section for service performance analytics.
- Add a main dashboard with analytics and a summary of all aspects beneficial to a car workshop.
- Add the ability to search and filter the database.
- Improve how vehicles owned by a specific client are displayed.
- Introduce user authentication and role-based access control.