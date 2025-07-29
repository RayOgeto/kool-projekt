# 🤝 Kool Projekt - Donation Platform

A Flask-based web application that connects donors with recipients in need. This platform facilitates charitable giving by allowing users to post needs and make donations.

## 🚀 Features

- **User Authentication**: Secure registration and login system
- **Role-based Access**: Separate interfaces for donors and recipients
- **Need Management**: Recipients can post requests for help
- **Donation System**: Donors can contribute to specific needs
- **Real-time Updates**: Track donation status and fulfillment
- **RESTful API**: Complete API for frontend integration

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with bcrypt password hashing
- **CORS**: Cross-origin resource sharing enabled
- **Frontend**: HTML/CSS/JavaScript (static files)

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kool-projekt
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python src/app.py
   ```

6. **Access the application**
   - Web interface: http://localhost:5000
   - API base URL: http://localhost:5000/api

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "donor",
  "phone_number": "+1234567890"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

### User Management

#### Get All Users
```http
GET /api/users
Authorization: Bearer <token>
```

#### Get User Profile
```http
GET /api/profile
Authorization: Bearer <token>
```

#### Update User
```http
PUT /api/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Updated Name",
  "phone_number": "+1234567890"
}
```

### Needs Management

#### Get All Needs
```http
GET /api/needs?category=food&urgency=high&status=active
```

#### Create Need (Recipients only)
```http
POST /api/needs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Need for Food",
  "description": "I need food assistance for my family",
  "category": "food",
  "urgency_level": "high",
  "amount_needed": 50.0,
  "unit": "kg",
  "location": "Nairobi, Kenya"
}
```

#### Get My Needs
```http
GET /api/my-needs
Authorization: Bearer <token>
```

### Donations Management

#### Get All Donations
```http
GET /api/donations
Authorization: Bearer <token>
```

#### Create Donation (Donors only)
```http
POST /api/donations
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 25.0,
  "unit": "kg",
  "description": "Rice and beans",
  "donation_type": "goods",
  "need_id": 1,
  "delivery_address": "123 Main St",
  "delivery_instructions": "Leave at gate"
}
```

#### Get Need Donations
```http
GET /api/needs/{need_id}/donations
```

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Hashed password
- `first_name`: User's first name
- `last_name`: User's last name
- `phone_number`: Contact number
- `user_type`: 'donor', 'recipient', or 'admin'
- `verification_status`: 'pending', 'verified', or 'rejected'
- `is_active`: Account status
- `created_at`: Registration timestamp
- `updated_at`: Last update timestamp

### Needs Table
- `id`: Primary key
- `title`: Need title
- `description`: Detailed description
- `category`: Need category (food, clothing, etc.)
- `urgency_level`: 'low', 'medium', 'high', 'critical'
- `status`: 'active', 'fulfilled', 'cancelled'
- `amount_needed`: Required amount
- `unit`: Unit of measurement
- `location`: Location information
- `recipient_id`: Foreign key to users table
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Donations Table
- `id`: Primary key
- `amount`: Donation amount
- `unit`: Unit of measurement
- `description`: Donation description
- `status`: 'pending', 'accepted', 'delivered', 'cancelled'
- `donation_type`: 'monetary', 'goods', 'services'
- `need_id`: Foreign key to needs table
- `donor_id`: Foreign key to users table
- `delivery_address`: Delivery location
- `delivery_instructions`: Special instructions
- `delivery_date`: Scheduled delivery date
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## 🔧 Configuration

The application uses the following configuration:

- **Database**: SQLite database located at `src/database/needs.db`
- **Secret Key**: Configured in `app.py`
- **CORS**: Enabled for cross-origin requests
- **Port**: 5000 (configurable in `app.py`)

## 🧪 Testing

To test the API endpoints, you can use tools like:
- Postman
- curl
- Insomnia
- Any HTTP client

Example curl commands:

```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User","user_type":"donor"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions, please:
1. Check the existing issues
2. Create a new issue with detailed information
3. Contact the development team

## 🗺️ Roadmap

- [ ] Email verification system
- [ ] Password reset functionality
- [ ] File upload for donation images
- [ ] Real-time notifications
- [ ] Mobile app integration
- [ ] Payment gateway integration
- [ ] Advanced search and filtering
- [ ] Admin dashboard
- [ ] Analytics and reporting

---

**Made with ❤️ for making the world a better place** 