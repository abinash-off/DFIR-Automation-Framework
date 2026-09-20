# DFIR Automation Framework

A defensive Digital Forensics and Incident Response (DFIR) automation platform for case management, evidence tracking, cryptographic integrity verification, IOC extraction, timeline-ready evidence workflows, and audit logging.

## Features
- Case and evidence management
- SHA-256 evidence integrity tracking
- JWT authentication
- Analyst/admin role model
- IOC extraction utilities
- Audit logging
- REST API with OpenAPI documentation
- Docker support
- Pytest test suite
- SQLite for development and PostgreSQL-compatible configuration for production

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Defensive use
Use only on systems, evidence, and data for which you have explicit authorization. Never commit real credentials, tokens, private keys, or sensitive evidence to the repository.
