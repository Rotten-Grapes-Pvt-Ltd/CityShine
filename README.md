# CityShine

A Django-based civic issue management system that enables citizens to report civic issues and authorities to manage them efficiently.

## Features

- **User Roles**:
  - Citizens: Report issues and track their status
  - Field Staff: Update issue status and manage on-ground operations
  - Officers: Access analytics and oversee all operations

- **Issue Management**:
  - Report civic issues with location, photos, and descriptions
  - Real-time status updates
  - Interactive map interface
  - Date and time-based filtering

- **Analytics**:
  - Issue type distribution visualization
  - Status distribution by issue type
  - Interactive charts and filters

## Tech Stack

- Django
- PostGIS for spatial data
- OpenLayers for maps
- Chart.js for analytics
- Bootstrap 5 for UI
- PostgreSQL database

## Setup

1. Install PostgreSQL and PostGIS:
```bash
# For macOS using Homebrew
brew install postgresql
brew install postgis

# For Ubuntu
sudo apt install postgresql postgresql-contrib
sudo apt install postgis
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r req.txt
```

3. Create database and enable PostGIS:
```sql
CREATE DATABASE cityshine;
\c cityshine;
CREATE EXTENSION postgis;
```

4. Configure environment:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Usage

1. **Citizens**:
   - Register/Login
   - Report new issues
   - Track reported issues
   - View issues map

2. **Field Staff**:
   - Update issue status
   - View assigned issues
   - Filter issues by type/status/date

3. **Officers**:
   - Access analytics dashboard
   - View issue distribution
   - Monitor field staff performance
   - Generate insights

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request