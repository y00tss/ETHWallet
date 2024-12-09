
# y00tss


<br>

# Kauri API

[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![FastAPI Version](https://img.shields.io/badge/FastAPI-0.95.0-blue.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-15-green.svg)](https://www.postgresql.org/docs/15/release-15-0.html)
[![SQLAlchemy Version](https://img.shields.io/badge/SQLAlchemy-2.0.0-blue.svg)](https://docs.sqlalchemy.org/en/20/)
[![Alembic Version](https://img.shields.io/badge/Alembic-1.10.4-yellow.svg)](https://alembic.sqlalchemy.org/)
[![Uvicorn Version](https://img.shields.io/badge/Uvicorn-0.22.0-yellow.svg)](https://www.uvicorn.org/)
[![Docker Version](https://img.shields.io/badge/Docker-20.10.8-blue.svg)](https://www.docker.com/)
[![Docker Compose Version](https://img.shields.io/badge/Docker%20Compose-1.29.2-blue.svg)](https://docs.docker.com/compose/)

[![web3 Version](https://img.shields.io/badge/Web3-5.0.0-blue.svg)](https://web3py.readthedocs.io/en/stable/)
[![pytest Version](https://img.shields.io/badge/pytest-7.2.1-yellow.svg)](https://docs.pytest.org/en/stable/)
[![pytest-cov Version](https://img.shields.io/badge/pytest--cov-4.0.0-yellow.svg)](https://pytest-cov.readthedocs.io/en/latest/)

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/y00tss)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mykhailoshepelenko/)

## Description
his project is a RESTful API built with FastAPI that interacts with Ethereum blockchain, performs wallet operations, and handles transactions. It uses SQLAlchemy with PostgreSQL as the database backend. It supports wallet management, transaction processing, and integration with Web3 technologies.

## Running the Project Locally

1. Open your terminal and put the command:
```bash
git clone https://github.com/y00tss/ETHWallet
```
2. Open Docker Desktop on your Windows and after use next command:
```bash
cd ETHWallet
```
3. Creation .env file
Go back to Notion and copy the ENV content. Create a new file called .env in the root directory of the project and paste the content into it.

4. Next step is creating the container and start the app by following command:
```bash
docker-compose up --build
```
5. Press the bottom below to open the app in your browser:

<a href="http://localhost:8001/docs" target="_blank">WebApp</a>

