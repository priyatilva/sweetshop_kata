[README.MD](https://github.com/user-attachments/files/22431163/README.MD)
## Project : Sweet Shop Management System

A full-stack Sweet Shop Management System where users can browse, search, and purchase sweets, while admins can manage inventory.  

**Tech Stack**: FastAPI (Python) backend, React frontend, SQLite database.

### Features

#### Backend
- User registration and login with JWT authentication
- Role-based access (Admin / User)
- Admin can add, update, delete, and restock sweets
- Users can view, search, and purchase sweets
- Database persists all data

#### Frontend
- React-based SPA
- Dynamic dashboard based on user role
- Responsive, Indian-themed UI
- Sweet cards with name, category, price, and quantity
- Disabled purchase button if quantity is zero

### Installation

**Backend**
```bash
cd sweetshop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs at: http://127.0.0.1:8000

Frontend

cd sweetshop-frontend-fixed
npm install
npm start

Frontend runs at: http://localhost:3000
Usage

    Register a user (normal user) via frontend form

    Login to receive JWT token

    Access user/admin dashboard based on role

    Users: search, list, and purchase sweets

    Admins: add, update, delete, restock, search, and list sweets

API Endpoints

Auth

    POST /api/auth/register - Register user

    POST /api/auth/login - Login user (returns JWT token & role)

Sweets (Protected)

    GET /api/sweets - List all sweets

    GET /api/sweets/search - Search sweets

    POST /api/sweets - Add sweet (Admin only)

    PUT /api/sweets/:id - Update sweet (Admin only)

    DELETE /api/sweets/:id - Delete sweet (Admin only)

    POST /api/sweets/:id/purchase - Purchase sweet

    POST /api/sweets/:id/restock - Restock sweet (Admin only)
