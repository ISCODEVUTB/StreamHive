<p align="center">
  <a href="https://thehive.up.railway.app/">
    <img src="https://github.com/AnaSMH5/thehive_frontend/blob/master/assets/icons/logo%2Btitle.svg" height="100"/>
  </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
    <img src="https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3">
    <img src="https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white">
    <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
    <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white">
</p>

<p align="center">
    <a href="https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_StreamHive">
        <img src="https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_StreamHive&metric=alert_status">
    </a>
    <a href="https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_StreamHive">
        <img src="https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_StreamHive&metric=coverage">
    </a>
</p>

# THE HIVE

The Hive is a comprehensive web application designed to unify and streamline data across streaming services, digital advertising, online publications, and press outlets. Its core mission is to deliver a seamless, secure, and enriched experience for film enthusiasts by integrating entertainment content discovery with personalized tools and industry insights. The platform not only facilitates movie exploration and management but also fosters a digital ecosystem that connects users with the latest in film culture and trends.

[**WEBPAGE**](https://thehive.up.railway.app/)

[API Page](https://thehive.up.railway.app/docs)

## Overview

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
  - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- ✅ Tests with
- ✅ Tests:
  - 🧪 [Pytest](https://pytest.org).
  - 📊 Stress/load testing with [Apache JMeter](https://jmeter.apache.org/)
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.
- 📱 [Flutter](https://flutter.dev/) frontend application using:
  - 🎯 Dart as the programming language.
  - 📦 State management via setState and custom widgets.
  - 🔗 Consumes the FastAPI backend via HTTP (http package).
  - 🎨 Material Design UI with theming and form validation.

## 📈 Project Status

> **Current Phase:** In Development

## ⚙️ Installation & Setup

### Requirements

- Python 3.9+
- Docker (for containerized environments)
- Flutter (for mobile/web frontend)

### Local Setup

1. Clone the repository.
2. Backend setup (FastAPI)

   1. Go to the backend directory
   2. Create and activate a virtual environment
   3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   > Required libraries include:

   ```text
   fastapi
   uvicorn
   sqlmodel
   pydantic
   pytest
   pytest-cov
   passlib + bcrypt
   PyJWT
   ```

   4. Run the server:

   ```bash
   uvicorn backend.main:app --reload
   ```

3. Frontend setup (Flutter)
   1. Go to the frontend directory
   2. Install dependencies
   3. Run the flutter app

## 👥 Development Team

- **Ana Meza**
- **Isabella Ordosgoitia**
- **Alejandro Villarreal**

---
