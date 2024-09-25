# Health Tracker

Health Tracker is a patient assessment system that allows clinicians to administer, track, and manage patient
assessments. This project includes user authentication, patient management, and assessment management with features like
multi-tenancy, filtering, pagination, sorting, and search functionality.

**Technology Stack**
-------------------

* Backend:
    - Django
    - Django Rest Framework
    - Djoser
  
* Database: PostgreSQL

## Project Setup Instructions

1. Clone the repository using

```
git clone https://github.com/Hosseinht/health_track.git
```

2. Navigate to the project directory:
   ```
   cd health_track
   ```
3. Set up:
    - Create a virtual environment and activate it.
    - Install the required dependencies using `pip install -r requirements.txt`.
    - In the backend folder, rename .env.example to .env and set all the environment variables
    - Configure the database settings in `settings/local.py`.
    - Apply the database migrations using `python manage.py migrate`.
    - Create a superuser using `python manage.py createsuperuser`
    - Start the Django development server using `python manage.py runserver`.

4. Access the application:
    - Open your web browser and visit `http://localhost:8000` to access the Health Tracker application.

**API Documentation**
-------------------

The API documentation can be accessed
at

[http://127.0.0.1:8000/api//swagger-ui/](http://127.0.0.1:8000/api/swagger-ui/)

**Features**
-------------------

- **Multi-tenancy**: Implemented to ensure data isolation between different clinicians.
- **Filtering, Pagination, and Sorting**: Available for both patient and assessment management endpoints.
- **Search Functionality**: Added search capability for patients, allowing clinicians to easily find specific records.

### API Endpoints

- **User Authentication** (via Djoser):
    - Register: `api/auth/users/`
    - Login: `/auth/jwt/create/`

- **Patient Management**:
    - Create Patient: `POST /api/patients/`
    - List Patients: `GET /api/patients/` (with filtering, pagination, sorting, and search)
    - Retrieve, Update, Delete Patient: `GET|PUT|DELETE /api/patients/<int:pk>/`

- **Assessment Management**:
    - Create Assessment: `POST /patient/<int:pk>/assessment/create`
    - List Assessments: `GET /api/assessments/` (with filtering, pagination, sorting)
    - Retrieve, Update, Delete Assessment: `GET|PUT|DELETE /api/assessments/<int:pk>/`
    - List of Assessments for a specific patient: `GET patient/<int:pk>/assessment/` (with filtering, pagination,
      sorting)
    - Retrieve, Update and Delete a specific Assessment of a specific
      patient `GET|PUT|DELETE patient/<int:patient_pk>/assessment/<int:assessment_pk>/`
  
