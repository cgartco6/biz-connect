# CapeBiz Connect - AI-Powered Business Directory

A comprehensive, AI-managed business directory for the Western Cape, supporting businesses of all sizes from home-based to large enterprises.

## Features

- Free and paid listing options (R199-R1599/month)
- R99 boost option for increased visibility
- AI-powered management system
- Secure payment processing
- Responsive design for all devices
- Business owner dashboard with analytics
- Complete town/city coverage of Western Cape

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL database
- Aftihost hosting account (or similar)

### Installation

1. Clone the repository to your local machine
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see Configuration section)
6. Initialize the database: `flask db init && flask db migrate && flask db upgrade`
7. Run the application: `python run.py`

### Configuration

Create a `.env` file in the root directory with the following variables:

```ini
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost/capebiz
PAYFAST_MERCHANT_ID=your-merchant-id
PAYFAST_MERCHANT_KEY=your-merchant-key
PAYFAST_SANDBOX=True
MAIL_SERVER=smtp.aftihost.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@yourdomain.com
MAIL_PASSWORD=your-email-password
