# FinanceHub
The Demo is now active on [alphex.pythonanywhere.com](alphex.pythonanywhere.com)
## Overview

FinanceHub is a comprehensive Django-based financial tracking and conversion platform designed to provide real-time market data for precious metals and currencies. The application offers user authentication, a universal conversion dashboard, and a personal net worth tracking system that aggregates holdings across multiple asset classes.

The platform scrapes live pricing data from external market sources and enables users to monitor their portfolio valuation in Iranian Rials (IRR) with historical tracking capabilities.

## Core Features

### Authentication System
- Secure user registration with form validation
- Login and logout functionality with session management
- Password change interface for authenticated users
- Complete password reset workflow with email-based token verification
- Custom authentication forms with enhanced security measures

### Universal Conversion Dashboard
- Real-time market price retrieval from tgju.org
- Support for multiple asset classes:
  - Gold (18K, 24K, and troy ounce)
  - Silver (gram and troy ounce)
  - US Dollar (USD to IRR conversion)
- Live calculation engine with instant conversion results
- Clean, responsive user interface with gradient design elements
- Login-protected access to ensure data security

### Net Worth Tracking System
- Personal portfolio management for multiple asset types
- Real-time net worth calculation in IRR
- Historical snapshot functionality with timestamp tracking
- Interactive Chart.js visualization showing 30-day trends
- Asset breakdown display showing value contribution per holding
- User-initiated snapshot creation for performance monitoring
- Database-backed persistence with indexed queries for efficiency

### Web Scraping Engine
- Robust price scraping system using requests and BeautifulSoup4
- Error handling with custom exception classes
- Support for Persian and Arabic numeral conversion
- Configurable timeout and retry mechanisms
- User-agent spoofing to ensure reliable data retrieval
- Regular expression-based price extraction and cleaning

## Technology Stack

### Backend Framework
- **Django 5.2.7**: Core web framework providing ORM, routing, and authentication
- **Python 3.x**: Primary programming language

### Database
- **SQLite3**: Default relational database for development and small-scale deployments
- **Django ORM**: Database abstraction layer with migration support

### Data Processing
- **BeautifulSoup4 4.13.3**: HTML parsing for web scraping operations
- **requests 2.32.3**: HTTP library for external API communication
- **lxml 5.3.2**: XML and HTML processing engine

### Frontend Technologies
- **HTML5/CSS3**: Semantic markup and modern styling
- **JavaScript ES6+**: Client-side interactivity and real-time calculations
- **Chart.js 4.4.0**: Data visualization library for historical trend charts

### Additional Dependencies
- **django-allauth 65.16.1**: Extended authentication and account management
- **cryptography 44.0.2**: Secure password hashing and encryption utilities
- **PyYAML 6.0.2**: Configuration file parsing

## Project Architecture

### Directory Structure

```
FinanceHub/
├── bkiblog/                    # Main Django project directory
│   ├── bkiblog/                # Project configuration package
│   │   ├── settings.py         # Django settings and configuration
│   │   ├── urls.py             # Root URL configuration
│   │   ├── wsgi.py             # WSGI application entry point
│   │   └── asgi.py             # ASGI application for async support
│   │
│   ├── blog/                   # Authentication and landing page app
│   │   ├── views.py            # Login, logout, registration views
│   │   ├── forms.py            # Custom authentication forms
│   │   ├── urls.py             # URL patterns for auth routes
│   │   ├── models.py           # User-related models (if extended)
│   │   ├── templates/blog/     # Authentication templates
│   │   │   ├── main-page.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── password_change_form.html
│   │   │   ├── password_reset.html
│   │   │   └── ...
│   │   └── static/blog/        # CSS files for auth pages
│   │
│   ├── conversionapp/          # Conversion and net worth tracking app
│   │   ├── views.py            # Converter and NetWorth views
│   │   ├── models.py           # UserHolding and NetWorthHistory models
│   │   ├── scraper.py          # Web scraping engine for market data
│   │   ├── urls.py             # URL patterns for conversion routes
│   │   ├── admin.py            # Django admin configuration
│   │   ├── migrations/         # Database migration files
│   │   ├── templates/conversionapp/
│   │   │   ├── converter.html
│   │   │   └── networth.html
│   │   └── static/             # CSS for conversion pages
│   │
│   ├── templates/              # Shared templates
│   │   ├── base.html           # Base template with common structure
│   │   └── 404.html            # Custom error page
│   │
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies
│   ├── db.sqlite3              # SQLite database file (generated)
│   └── NETWORTH_FEATURE.md     # Net worth feature documentation
│
└── README.md                   # Project documentation
```

### Application Components

#### Blog Application
Handles all authentication-related functionality and serves the public landing page. Includes custom forms for user registration and login with enhanced validation.

#### Conversion Application
Core business logic for market data retrieval, conversion calculations, and net worth tracking. Implements the scraping engine and provides login-protected views for financial data.

## Database Schema

### UserHolding Model
Stores individual user holdings for net worth calculation.

```python
- user: OneToOneField(User) - Links to Django User model
- gold18: DecimalField - Gold 18K holdings in grams
- gold24: DecimalField - Gold 24K holdings in grams
- usd: DecimalField - US Dollar holdings
- calculate_net_worth() - Method to compute total value in IRR
```

### NetWorthHistory Model
Maintains timestamped snapshots of user net worth for historical analysis.

```python
- user: ForeignKey(User) - Links to Django User model
- net_worth: DecimalField - Total portfolio value in IRR
- gold18_amount: DecimalField - Gold 18K amount at snapshot time
- gold24_amount: DecimalField - Gold 24K amount at snapshot time
- usd_amount: DecimalField - USD amount at snapshot time
- timestamp: DateTimeField - When snapshot was created
- Index on (user_id, timestamp) - Optimized for historical queries
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment tool (venv or virtualenv)
- Active internet connection for market data retrieval

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd FinanceHub
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
cd bkiblog
pip install -r requirements.txt
```

Note: The requirements.txt file contains all necessary dependencies. Core requirements include:
- Django==5.2.7
- beautifulsoup4==4.13.3
- requests==2.32.3
- lxml==5.3.2

#### 4. Configure Database
```bash
# Apply all migrations to create database schema
python manage.py migrate
```

This will create the SQLite database file at `bkiblog/db.sqlite3` and set up all required tables.

#### 5. Create Administrative User
```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password (must meet Django's security requirements)

#### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`

### Initial Configuration

After starting the server:

1. Navigate to `http://127.0.0.1:8000/` to view the landing page
2. Register a new user account or use the superuser credentials
3. Log in to access protected features
4. Visit `/hub/` for the conversion dashboard
5. Visit `/hub/networth/` for the net worth tracker

## Usage Guide

### Accessing the Conversion Dashboard

1. Log in with valid credentials
2. Navigate to the conversion hub at `/hub/`
3. View real-time market prices displayed in the interface
4. Use the calculator tools to perform conversions
5. All calculations use live data fetched from tgju.org

### Managing Net Worth

#### Adding Holdings
1. Navigate to `/hub/networth/`
2. Enter your holdings in the input fields:
   - Gold 18K (in grams)
   - Gold 24K (in grams)
   - US Dollars
3. Net worth updates automatically as you type
4. Click "Update Holdings" to save changes

#### Creating Historical Snapshots
1. After updating holdings, click "Save Snapshot"
2. Current net worth and holdings are recorded with timestamp
3. The chart automatically updates to show new data point
4. Historical data persists across sessions

#### Viewing Performance
- The Chart.js visualization displays the last 30 days of snapshots
- X-axis shows dates, Y-axis shows net worth in IRR
- Hover over data points to see exact values
- Asset breakdown shows value contribution from each holding type

### Administrative Interface

Access the Django admin panel at `/admin/` using superuser credentials:

- **User Management**: Create, modify, and delete user accounts
- **Holdings Management**: View and edit user holdings directly
- **History Records**: View net worth history (read-only for data integrity)

## Configuration Options

### Database Configuration

To use a different database backend, modify `bkiblog/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or mysql, oracle
        'NAME': 'financehub_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration

For password reset functionality, configure email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@financehub.com'
```

### Security Settings

For production deployment, update these settings:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-production-secret-key'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## API Endpoints

### Authentication Endpoints
- `GET /` - Landing page
- `GET /login/` - User login form
- `POST /login/` - Authenticate user credentials
- `GET /logout/` - Log out current user
- `GET /register/` - User registration form
- `POST /register/` - Create new user account
- `GET /password-change/` - Password change form
- `POST /password-change/` - Update user password
- `GET /password-reset/` - Password reset request form
- `POST /password-reset/` - Send password reset email

### Conversion Endpoints
- `GET /hub/` - Conversion dashboard (requires authentication)
- `GET /hub/networth/` - Net worth tracker (requires authentication)
- `POST /hub/networth/` - Update holdings or save snapshot

### Admin Endpoints
- `GET /admin/` - Django admin interface (requires superuser)

## Data Flow Architecture

### Market Data Retrieval Flow
```
1. User accesses conversion dashboard
2. ConversionViewView.get_context_data() is called
3. scrape_market_prices() fetches data from tgju.org
4. BeautifulSoup parses HTML content
5. clean_price() extracts and normalizes numeric values
6. Prices are passed to template context
7. JavaScript receives data and enables calculations
```

### Net Worth Calculation Flow
```
1. User inputs holdings in NetWorth interface
2. JavaScript calculates live net worth (client-side preview)
3. User clicks "Update Holdings"
4. POST request sent to NetWorthView
5. UserHolding model updated in database
6. calculate_net_worth() method called
7. Latest market prices fetched from scraper
8. Net worth computed: (gold18 × rate) + (gold24 × rate) + (usd × rate)
9. Result returned to template and displayed
```

### Snapshot Creation Flow
```
1. User clicks "Save Snapshot"
2. POST request with action="save_snapshot"
3. NetWorthHistory record created with current timestamp
4. Current holdings and net worth stored
5. Chart.js data updated via JavaScript
6. New data point appears on historical chart
```

## Security Considerations

### Authentication Security
- Password hashing using Django's PBKDF2 algorithm with SHA256
- CSRF protection on all POST requests
- Session-based authentication with secure cookies
- LoginRequiredMixin prevents unauthorized access to financial data

### Data Security
- SQL injection prevention through Django ORM parameterized queries
- XSS protection via Django's template auto-escaping
- Decimal field usage prevents floating-point precision errors in financial calculations
- One-to-one relationship ensures single holding record per user

### Web Scraping Security
- User-agent header prevents blocking by target website
- Timeout mechanisms prevent hanging requests
- Exception handling for network failures
- No sensitive data exposed in scraper logs

## Performance Optimization

### Database Optimization
- Indexed queries on NetWorthHistory (user_id, timestamp)
- One-to-one relationship reduces JOIN operations
- Selective field loading in queries
- Connection pooling for concurrent requests

### Caching Strategies
Consider implementing caching for production:

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# In views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def cached_view(request):
    # Market prices cached to reduce scraping frequency
    pass
```

### Frontend Optimization
- Chart.js loads only last 30 days of data
- Real-time calculations performed client-side
- Minimal DOM manipulation for better performance
- CSS and JavaScript minification recommended for production

## Testing

### Running Unit Tests
```bash
cd bkiblog
python manage.py test
```

### Test Coverage
The project includes test files:
- `test_networth.py` - Unit tests for net worth functionality
- `blog/tests.py` - Authentication flow tests
- `conversionapp/tests.py` - Conversion logic tests

### Manual Testing Checklist
- [ ] User registration with valid/invalid data
- [ ] Login with correct/incorrect credentials
- [ ] Password reset email flow
- [ ] Market price scraping functionality
- [ ] Conversion calculations accuracy
- [ ] Holdings update and persistence
- [ ] Snapshot creation and chart rendering
- [ ] Admin interface accessibility
- [ ] Responsive design on mobile devices
- [ ] Error handling for network failures

## Troubleshooting

### Common Issues

#### Market Prices Not Loading
**Symptom**: Conversion dashboard shows no prices or "N/A" values

**Solutions**:
1. Check internet connection
2. Verify tgju.org is accessible
3. Review scraper.py for URL changes
4. Check Django logs for PriceScraperError exceptions
5. Increase timeout value in scraper configuration

#### Database Migration Errors
**Symptom**: `python manage.py migrate` fails

**Solutions**:
1. Delete `db.sqlite3` and re-run migrations
2. Check for conflicting migration files
3. Run `python manage.py makemigrations` first
4. Verify database permissions

#### Static Files Not Loading
**Symptom**: CSS/JavaScript not applied

**Solutions**:
1. Run `python manage.py collectstatic`
2. Verify STATIC_URL and STATIC_ROOT in settings.py
3. Check browser console for 404 errors
4. Ensure DEBUG=True for development

#### Chart Not Displaying
**Symptom**: Net worth history chart is blank

**Solutions**:
1. Create at least one snapshot
2. Check browser console for JavaScript errors
3. Verify Chart.js CDN is accessible
4. Ensure historical data exists in database

## Deployment

### Production Deployment Checklist

#### 1. Environment Configuration
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Generate new `SECRET_KEY`
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure email backend for password resets
- [ ] Enable SSL/TLS with proper certificates

#### 2. Static Files
```bash
python manage.py collectstatic
```

#### 3. Database Migration
```bash
python manage.py migrate --no-input
```

#### 4. Create Superuser
```bash
python manage.py createsuperuser --no-input --username admin --email admin@example.com
```

#### 5. Web Server Configuration

**Using Gunicorn:**
```bash
pip install gunicorn
gunicorn bkiblog.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Using uWSGI:**
```bash
pip install uwsgi
uwsgi --http :8000 --module bkiblog.wsgi --workers 4
```

#### 6. Reverse Proxy (Nginx Example)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/FinanceHub/bkiblog/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY bkiblog/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bkiblog/ .

RUN python manage.py collectstatic --no-input
RUN python manage.py migrate --no-input

EXPOSE 8000
CMD ["gunicorn", "bkiblog.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t financehub:latest .
docker run -p 8000:8000 financehub:latest
```

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make changes and test thoroughly
4. Commit with descriptive messages (`git commit -m 'Add feature: description'`)
5. Push to your fork (`git push origin feature/your-feature`)
6. Submit a pull request

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Write unit tests for new features

## License

This project is provided as-is for educational and personal use. Please review and comply with the terms of service for any external data sources used (such as tgju.org).

## Support and Contact

For issues, questions, or feature requests, please open an issue in the project repository or contact the development team.

## Acknowledgments

- Django framework for robust web development tools
- BeautifulSoup4 for HTML parsing capabilities
- Chart.js for data visualization
- tgju.org for providing market data access
- The open-source community for continuous inspiration and support

## Version History

### Version 1.0.0 (Current)
- Initial release with authentication system
- Universal conversion dashboard
- Net worth tracking with historical snapshots
- Web scraping engine for real-time market data
- Chart.js integration for data visualization
- SQLite database with optimized schema
- Responsive UI with custom CSS styling

## Roadmap

### Planned Features
- Automated snapshot scheduling (daily/weekly)
- Export functionality (CSV, PDF reports)
- Email notifications for price alerts
- Cryptocurrency support (Bitcoin, Ethereum)
- Multi-currency portfolio support
- Mobile application (React Native)
- RESTful API for third-party integrations
- Advanced analytics and comparative reports
- Portfolio allocation pie charts
- Multi-language support (English, Persian)

### Under Consideration
- Social features (portfolio sharing)
- Investment recommendations based on trends
- Integration with banking APIs
- Real-time price change notifications
- Historical data archival strategies
- Advanced charting options (candlestick, line)
- Dark mode theme option
