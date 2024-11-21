# [Title]

## Description

[Project Description]

## Setup and Run the Project Locally

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Generate Virtual Environment

Create a virtual environment to ensure consistency in dependencies.

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r path/to/requirement/file
```

### 4. Environment variables

create `.env` file on the root of the project and copy the variables from `.env.template` file and replace the values with your values.

### 5. Run Migrations

Apply the database migrations to set up the initial schema for the database:

```bash
python manage.py migrate
```

### 6. Run the Server

Start the development server to test the application locally:

```bash
python manage.py runserver
```

By default, the application will run using an SQLite database.

## Alternative: Run the Project Using Docker and Docker-Compose with PostgreSQL

To run the project using Docker and PostgreSQL, follow these steps:

### 1. Create Docker Configuration

Make sure you have a `Dockerfile` and `docker-compose.yml` in your project root.

### 2. Create `.env`

check **Environment variables** section.

### 3. Build and Start the Containers

Run the following Docker commands to build the images and start the containers:

```bash
docker-compose up --build
```

This command will build the Docker images and start both the Django app and PostgreSQL container.

### 4. Access the Application

Once the containers are up and running, you can access the application by navigating to:

```bash
http://localhost:running_port
```

## Workflow

**Note: Ensure to run `pre-commit install` command before doing your first commit.**

The project follows a Gitflow workflow for version control and collaboration. Key aspects of the workflow include:

- Feature Branches: Each new feature should be developed in a dedicated branch named `feature/{Clickup-task-id}`

- Main Branch: The `main` branch holds the stable, production-ready code.

- Development Branch: The `dev` branch serves as an integration branch for feature branches. Regular updates from `dev` are merged into `main` when a new release is ready.

- Pull Requests: All changes should go through a pull request for code review before merging into the `dev` branch.

## Naming Syntax

### Branch Naming

- Feature Branches: `feature/{Clickup-task-id}`

- Bugfix Branches: `bugfix/{Clickup-task-id}`

- Hotfix Branches: `hotfix/issue-description` (e.g., `hotfix/critical-database-fix`)

### File Naming

- Python Files: Use lowercase letters with underscores (e.g., `license_management.py`).

- Templates: Use lowercase letters with hyphens (e.g., `user-profile.html`).

- Static Files: Organize by type (e.g., css, js, images) and use lowercase letters with hyphens.

- URL: Use lowercase letters with hyphens and it must end with forward slash (e.g., `/manage-users/`).

## Commit Message Format

Use a consistent commit message structure:

Format: `[TYPE] [SCOPE]: [SUMMARY]`

### Types

- feat: For new features (e.g., `feat(module): add health certification module`)

- fix: For bug fixes (e.g., `fix(database): resolve database connection issue`)

- docs: For documentation updates (e.g., `docs(README): update README file`)

- style: For code style improvements (e.g., `style(flake8): format code according to PEP8`)

- refactor: For refactoring code (e.g., `refactor(users): improve data handling logic`)

- test: For adding or modifying tests (e.g., `test(license): add unit tests for license module`)

- chore: For maintenance and other tasks (e.g., `chore(dependencies): update dependencies`)

### Commit template (On the remote git host)

```markdown
# Commit Message Template

[TYPE] [SCOPE]: [SUMMARY]

# Description

[Provide a brief explanation of the change. Include what was done, why it was done, and any relevant context.]

# Ticket URL

[TICKET_URL]

# Changes Made

- [List the key changes made in the codebase, bullet-point style.]

# Checklist

- [ ] Code is properly formatted.
- [ ] Tests have been added or updated (if applicable).
- [ ] Documentation has been updated (if applicable).
- [ ] No breaking changes introduced.

# Examples

# A commit with this template might look like:

feat(auth): add JWT-based authentication

# Description

Added support for JWT-based authentication to improve security and support stateless authentication.

# Ticket URL

https://example.com/tickets/123

# Changes Made

- Added a `login` endpoint to generate JWTs.
- Created middleware to validate JWTs on protected routes.
- Updated user model to include refresh token support.

# Testing

- Verified successful login with valid credentials.
- Tested token validation for expired and malformed tokens.
- Updated existing unit tests and added new ones for authentication flows.

# Checklist

- [x] Code is properly formatted.
- [x] Tests have been added or updated.
- [x] Documentation has been updated.
- [ ] No breaking changes introduced.
```

## Tools used

| Package Name                     | Usage                                                                                                                                                                                                                                                                                                                                                                                                                       | Installation                              |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Django                           | Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.                                                                                                                  | pip install django                        |
| Django Rest Framework            | Django REST framework is a powerful and flexible toolkit for building Web APIs.                                                                                                                                                                                                                                                                                                                                             | pip install djangorestframework           |
| Django Rest Framework Simple JWT | Simple JWT provides a JSON Web Token authentication backend for the Django REST Framework. It aims to cover the most common use cases of JWTs by offering a conservative set of default features. It also aims to be easily extensible in case a desired feature is not present.                                                                                                                                            | pip install djangorestframework-simplejwt |
| Django Environ                   | Python package that allows you to use Twelve-factor methodology to configure your Django application with environment variables.                                                                                                                                                                                                                                                                                            | pip install django-environ                |
| Django Split Settings            | Organize Django settings into multiple files and directories. Easily override and modify settings. Use wildcards in settings file paths and mark settings files as optional.                                                                                                                                                                                                                                                | pip install django-split-settings         |
| Whitenoise                       | With a couple of lines of config WhiteNoise allows your web app to serve its own static files, making it a self-contained unit that can be deployed anywhere without relying on nginx, Amazon S3 or any other external service. (Especially useful on Heroku, OpenShift and other PaaS providers.)                                                                                                                          | pip install whitenoise                    |
| Gunicorn                         | Gunicorn `Green Unicorn` is a Python WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.                                                                                                                                                   | pip install gunicorn                      |
| Django Cors Headers              | A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses. This allows in-browser requests to your Django application from other origins.                                                                                                                                                                                                                                                            | pip install django-cors-headers           |
| Psycopg2 Binary                  | Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent `INSERTs`s or `UPDATE`s. | pip install psycopg2-binary               |
| Flake8                           | Command-line utility for enforcing style consistency across Python projects                                                                                                                                                                                                                                                                                                                                                 | pip install flake8                        |
| Flake8 DocStrings                | A simple module that adds an extension for the fantastic `pydocstyle` tool to flake8.                                                                                                                                                                                                                                                                                                                                       | pip install flake8-docstrings             |
| Flake8 BugBear                   | A plugin for Flake8 finding likely bugs and design problems in your program.                                                                                                                                                                                                                                                                                                                                                | pip install flake8-bugbear                |
| Flake8 MyPy                      | A plugin that combines flake8 and mypy, letting developers check code style and type consistency in one tool. It helps catch both linting and type-related issues, improving code quality.                                                                                                                                                                                                                                  | pip install flake8-mypy                   |
| Flake8 Annotations               | A plugin that detects the absence of PEP 3107-style function annotations.                                                                                                                                                                                                                                                                                                                                                   | pip install flake8-annotations            |
| Flake8 Commas                    | Extension for enforcing trailing commas.                                                                                                                                                                                                                                                                                                                                                                                    | pip install flake8-commas                 |
| Flake8 Sort                      | To check if the imports on your python files are sorted the way you expect.                                                                                                                                                                                                                                                                                                                                                 | pip install flake8-isort                  |
| Flake8 Simplify                  | A flake8 plugin designed to identify and suggest simpler alternatives for common code patterns in Python.                                                                                                                                                                                                                                                                                                                   | pip install flake8_simplify               |
| Flake8 Pytest Style              | A plugin checking common style issues or inconsistencies with pytest-based tests.                                                                                                                                                                                                                                                                                                                                           | pip install flake8 Pytest Style           |
| Flake8 Comprehensions            | A plugin that helps you write better list/set/dict comprehensions.                                                                                                                                                                                                                                                                                                                                                          | pip install flake8-comprehensions         |
| Flake8 Debugger                  | A plugin that helps developers catch and remove debugger statements, like pdb and ipdb, in Python code.                                                                                                                                                                                                                                                                                                                     | pip install flake8-debugger               |
| Flake8 Eradicate                 | A plugin to find commented out (or so called "dead") code.                                                                                                                                                                                                                                                                                                                                                                  | pip install flake8-eradicate              |
| Flake8 rst docstrings            | A flake8 plugin that checks Python docstrings formatted in reStructuredText (reST) for syntax correctness.                                                                                                                                                                                                                                                                                                                  | pip install flake8-rst-docstrings         |
| Flake8 Quotes                    | A plugin that enforces consistency in the use of quote marks for strings in Python code.                                                                                                                                                                                                                                                                                                                                    | pip install flake8-quotes                 |
| Black                            | A Python code formatter that automatically formats Python code to comply with its style guide called PEP 8.                                                                                                                                                                                                                                                                                                                 | pip install black                         |
| Isort                            | A Python utility that helps in sorting and organizing import statements in Python code to create readable and consistent code.                                                                                                                                                                                                                                                                                              | pip install isort                         |
| Django-stubs                     | A type-checking plugin for Django that provides type annotations for Django's built-in classes, models, and other components.                                                                                                                                                                                                                                                                                               | pip install django-stubs                  |
| Bandit                           | A tool designed to find common security issues in Python code.                                                                                                                                                                                                                                                                                                                                                              | pip install bandit                        |
| Coverage                         | A tool that measures code coverage, helping developers understand which parts of the code are executed during tests and identify untested areas.                                                                                                                                                                                                                                                                            | pip install coverage                      |
| Django Coverage Plugin           | A plugin that integrates Coverage with Django, enabling measurement of coverage for Django templates, views, and code.                                                                                                                                                                                                                                                                                                      | pip install django_coverage_plugin        |
| Django Debug Toolbar             | configurable set of panels that display debug information for Django during development, useful for profiling and optimizing your application.                                                                                                                                                                                                                                                                              | pip install django-debug-toolbar          |
| Pytest                           | A powerful testing framework for Python that simplifies writing tests with features like fixtures, parameterization, and assert rewriting.                                                                                                                                                                                                                                                                                  | pip install pytest                        |
| Pytest Cov                       | A pytest plugin for measuring code coverage using Coverage and integrating the results with pytest’s test reports.                                                                                                                                                                                                                                                                                                          | pip install pytest-cov                    |
| Pytest Deadfixtures              | A plugin for identifying unused pytest fixtures, helping to keep your test suite clean and maintainable.                                                                                                                                                                                                                                                                                                                    | pip install pytest-deadfixtures           |
| Pytest Django                    | A pytest plugin that provides tools for testing Django applications, including database fixtures and environment setup.                                                                                                                                                                                                                                                                                                     | pip install pytest-django                 |
| Pytest Mock                      | A pytest plugin that integrates Python’s `unittest.mock` module, simplifying mocking and patching in tests.                                                                                                                                                                                                                                                                                                                 | pip install pytest-mock                   |
