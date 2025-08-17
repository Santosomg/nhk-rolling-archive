name: Update NHK Feed

on:
  schedule:
    # Runs every 2 hours
    - cron: '0 */2 * * *'
  workflow_dispatch:  # Allows manual trigger

jobs:
  update-feed:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout the repo
      - name: Checkout repository
        uses: actions/checkout@v3

      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # Step 3: Install dependencies
      - name: Install dependencies
        run: pip install requests

      # Step 4: Run the update script
      - name: Run update.py
        run: python update.py

      # Step 5: Configure Git (needed for commit)
      - name: Configure Git
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"

      # Step 6: Commit and push changes
      - name: Commit and push feed.xml
        run: |
          git add feed.xml
          git commit -m "Update NHK feed" || echo "No changes to commit"
          git push
