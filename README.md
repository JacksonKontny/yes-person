# yes-person
Script for auto-approving PRs based on criteria

# Requirements
- Pipenv

# Getting Started
Install dependencies
`pipenv sync`

Create dotenv file (and edit with token and other configurations)
`cp .env.example .env`

Create github token with `project` access and repo read access

Update `.env` file with github token and other configurations

Run
`make run`
