# 🎓 Student Management System

A comprehensive, modern Student Management System built with React and FastAPI, featuring a beautiful responsive UI and robust backend architecture.

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [📖 Detailed Setup](#-detailed-setup)
- [🔧 Configuration](#-configuration)
- [📊 API Documentation](#-api-documentation)
- [🎨 UI Components](#-ui-components)
- [🔐 Database Schema](#-database-schema)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## 🌟 Features

### 📚 Core Functionality
- **Student Management**: Complete CRUD operations for student records
- **Course Management**: Create, read, update, and delete courses
- **Enrollment System**: Manage student enrollments in courses
- **Dashboard**: Real-time statistics and overview
- **Search & Filter**: Advanced search capabilities
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### 🎨 User Experience
- **Modern UI**: Clean, professional interface with Tailwind CSS
- **Real-time Updates**: Instant feedback and loading states
- **Error Handling**: Comprehensive error messages and recovery
- **Navigation**: Intuitive routing and user flow
- **Data Validation**: Form validation and data integrity

### 🔧 Technical Features
- **RESTful API**: Well-structured API endpoints
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing configured
- **Health Checks**: API health monitoring
- **Development Tools**: Hot reload, debugging, and development server

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern JavaScript library for building UIs
- **React Router** - Declarative routing for React applications
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Vite** - Fast build tool and development server
- **Axios** - Promise-based HTTP client for API requests

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL** - Powerful, open-source object-relational database system
- **Uvicorn** - ASGI server implementation for FastAPI
- **Pydantic** - Data validation using Python type annotations

### Development Tools
- **Git** - Version control system
- **Node.js** - JavaScript runtime environment
- **Python 3.11+** - Programming language
- **npm** - Package manager for JavaScript

## 📁 Project Structure

```
Student_Management_System/
├── frontend/                    # React frontend application
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Layout.jsx     # Main layout component
│   │   │   ├── StudentForm.jsx # Student creation/edit form
│   │   │   └── CourseForm.jsx  # Course creation/edit form
│   │   ├── pages/              # Page components
│   │   │   ├── HomePage.jsx    # Dashboard/home page
│   │   │   ├── StudentsPage.jsx # Students management page
│   │   │   ├── CoursesPage.jsx  # Courses management page
│   │   │   └── EnrollmentsPage.jsx # Enrollments page
│   │   ├── services/           # API service layer
│   │   │   └── api.js          # API communication
│   │   ├── App.jsx             # Main application component
│   │   ├── main.jsx            # Application entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   │   └── v1/             # API version 1
│   │   │       ├── students.py # Student endpoints
│   │   │       ├── courses.py  # Course endpoints
│   │   │       └── enrollments.py # Enrollment endpoints
│   │   ├── core/               # Core application configuration
│   │   │   ├── config.py       # Settings and configuration
│   │   │   └── database.py     # Database connection
│   │   ├── models/             # Database models
│   │   │   ├── student.py      # Student model
│   │   │   ├── course.py       # Course model
│   │   │   └── enrollment.py   # Enrollment model
│   │   ├── schemas/            # Pydantic schemas
│   │   │   ├── student.py      # Student schema
│   │   │   ├── course.py       # Course schema
│   │   │   └── enrollment.py   # Enrollment schema
│   │   └── main.py             # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   └── alembic/                # Database migrations
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.11+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AaryaDhorje/Student-Management-System.git
   cd Student_Management_System
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb student_management_system
   
   # Update database configuration in backend/app/core/config.py
   # Set your PostgreSQL credentials
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start the Frontend Server**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## 📖 Detailed Setup

### Backend Configuration

1. **Environment Variables**
   Create a `.env` file in the `backend` directory:
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=student_management_system
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   
   # Application Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

2. **Database Migration**
   ```bash
   cd backend
   alembic upgrade head
   ```

### Frontend Configuration

1. **API Base URL**
   Update the API base URL in `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
   ```

2. **Environment Variables**
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
   ```

## 🔧 Configuration

### Backend Configuration (backend/app/core/config.py)

```python
class Settings(BaseSettings):
    # Application
    app_name: str = "Student Management System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "student_management_system"
    db_user: str = "postgres"
    db_password: str = "your_password"
    
    # Security
    secret_key: str = "your-secret-key-here"
    
    # CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
```

### Frontend Configuration (frontend/vite.config.js)

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
});
```

## 📊 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/v1
```

### Health Check
```http
GET /health
```

### Students Endpoints
```http
GET    /students              # Get all students
GET    /students/{id}         # Get specific student
POST   /students              # Create new student
PUT    /students/{id}         # Update student
DELETE /students/{id}         # Delete student
GET    /students/search       # Search students
```

### Courses Endpoints
```http
GET    /courses               # Get all courses
GET    /courses/{id}          # Get specific course
POST   /courses               # Create new course
PUT    /courses/{id}          # Update course
DELETE /courses/{id}          # Delete course
```

### Enrollments Endpoints
```http
GET    /enrollments           # Get all enrollments
GET    /enrollments/{id}      # Get specific enrollment
POST   /enrollments           # Create new enrollment
PUT    /enrollments/{id}      # Update enrollment
DELETE /enrollments/{id}      # Delete enrollment
```

### API Response Format

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error Response Format

```json
{
  "detail": "Error message description",
  "status_code": 400
}
```

## 🎨 UI Components

### Layout Component
- **Header**: Navigation menu and user information
- **Sidebar**: Quick navigation links
- **Footer**: Application information and links

### Forms
- **StudentForm**: Create and edit student information
- **CourseForm**: Create and edit course information
- **SearchForm**: Advanced search functionality

### Pages
- **HomePage**: Dashboard with statistics and overview
- **StudentsPage**: Student management interface
- **CoursesPage**: Course management interface
- **EnrollmentsPage**: Enrollment management interface

### Responsive Design
- **Desktop**: Full-featured interface with sidebar
- **Tablet**: Optimized layout with collapsible navigation
- **Mobile**: Touch-friendly interface with bottom navigation

## 🔐 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(20),
    address TEXT,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Courses Table
```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    credits INTEGER NOT NULL,
    instructor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Enrollments Table
```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    grade VARCHAR(2),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id)
);
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing Checklist

#### Student Management
- [ ] Create new student
- [ ] View student list
- [ ] Edit existing student
- [ ] Delete student
- [ ] Search students

#### Course Management
- [ ] Create new course
- [ ] View course list
- [ ] Edit existing course
- [ ] Delete course

#### Enrollment Management
- [ ] Enroll student in course
- [ ] View enrollments
- [ ] Update enrollment
- [ ] Delete enrollment

#### System Features
- [ ] Dashboard statistics
- [ ] Search functionality
- [ ] Error handling
- [ ] Responsive design

## 🚀 Deployment

### Backend Deployment (Production)

1. **Environment Setup**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   ```

2. **Database Setup**
   ```bash
   # Use production database
   alembic upgrade head
   ```

3. **Server Setup**
   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment (Production)

1. **Build Application**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Static Hosting**
   - Upload `dist/` folder to your hosting provider
   - Configure server to serve `index.html` for all routes

### Docker Deployment

1. **Backend Dockerfile**
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Frontend Dockerfile**
   ```dockerfile
   FROM node:16-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   FROM nginx:alpine
   COPY --from=0 /app/dist /usr/share/nginx/html
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- React team for the amazing framework
- FastAPI team for the excellent web framework
- Tailwind CSS for the utility-first CSS framework
- PostgreSQL team for the robust database system

## 📞 Support

For support, please contact:
- Email: aarya.dhorje@example.com
- GitHub Issues: [Create an issue](https://github.com/AaryaDhorje/Student-Management-System/issues)

## 🔄 Version History

- **v1.0.0** - Initial release with complete student management functionality
  - Student CRUD operations
  - Course management
  - Enrollment system
  - Responsive UI
  - RESTful API
  - Database integration

---

**Built with ❤️ by [Aarya Dhorje](https://github.com/AaryaDhorje)**
