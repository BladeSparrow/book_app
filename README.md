# 📚 Books Project — Simple JWT Authentication & Frontend

---

## ⚙️ Requirements
- Python 3.10+  
- All dependencies are in `requirements.txt`

---

## 🚀 How to Run

1. **Create and activate a virtual environment, then install dependencies:**
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Apply database migrations:**
   ```
   python manage.py migrate
   ```

3. **(Optional) Create an admin user:**
   ```
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```
   python manage.py runserver
   ```

5. **Open the app:**
   👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🌐 Frontend Pages
- `/accounts/pages/public/` — public page  
- `/accounts/pages/register/` — user registration  
- `/accounts/pages/login/` — login (stores JWT tokens)  
- `/accounts/pages/protected/` — requires login  

---

## 🔑 API Endpoints (base: `/api/accounts/`)
- **POST** `/register/` → create a new user  
- **POST** `/login/` → get `access` + `refresh` tokens  
- **POST** `/token/refresh/` → refresh `access` token  
- **POST** `/logout/` → blacklist refresh token  

Example response:
```json
{ "access": "<access_token>", "refresh": "<refresh_token>" }
```

---

## 🔐 JWT Settings
- Access token lifetime: 15 minutes  
- Refresh token lifetime: 7 days  
- Token rotation enabled (old refresh tokens are blacklisted)

---

## 🧾 Permissions
- Default: `IsAuthenticatedOrReadOnly`  
- Protected views require authentication

---

## 🪵 Logging
Logs go to console and `logs/app.log` (registration, login, logout, errors)

---
