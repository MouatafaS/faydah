name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.x  # Replace with the version of Python you're using

      - name: Install dependencies
        run: pip install -r requirements.txt  # Assuming you have a requirements.txt file

      - name: Run Python application
        run: python app.py  # Replace 'app.py' with your actual application file
