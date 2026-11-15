# GitHub and Streamlit Community Cloud Deployment

## Before pushing

The deployable model bundle is already included. The raw OSHA CSV is not included and is not needed to run the website.

1. Do not add the raw OSHA CSV to the public repository. It includes establishment/location fields and incident narratives.
2. Keep `artifacts/models/incident_review_engine.joblib`. The fitted bundle is required by the deployed Incident Review Desk.
3. Check that `.env`, credentials, reviewer worksheets and local databases are not staged.
4. If testing locally, use Python 3.13 to match `.python-version` and the model build runtime:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps
pytest -q
streamlit run app/streamlit_app.py
```

## Create the GitHub repository

1. Sign in to GitHub and create a new empty repository, for example `safety-incident-review-desk`.
2. Do not initialize it with a README, license or `.gitignore` because those files already exist in this project.
3. Open a terminal in the project root (the directory containing `README.md`).
4. Initialize Git if this folder is not already a Git repository:

```powershell
git init
git branch -M main
```

5. Review what will be committed:

```powershell
git status --short
```

The raw OSHA CSV is not included in this deployable package and must stay out of the public repository. The fitted model bundle at `artifacts/models/incident_review_engine.joblib` must remain tracked.

6. Commit and push:

```powershell
git add .
git status --short
git commit -m "Build operational workplace incident review workflow"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the remote URL with the repository URL shown by GitHub. If `origin` already exists, inspect `git remote -v` and update it only if necessary.

## Deploy to Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Authorize Streamlit Community Cloud to access the repository.
3. Choose **Create app** and select the existing app option.
4. Select the repository, branch `main`, and entrypoint file `app/streamlit_app.py`.
5. Open **Advanced settings** and select Python 3.13 to match `.python-version` and the runtime used to build the included model. Streamlit documents Python 3.12 as the default, so explicitly select 3.13 when it is available in the version list.
6. Choose an available app subdomain, save the advanced settings and select **Deploy**.
7. Watch the deployment logs. Resolve dependency or import errors before sharing the URL.
8. Open the live app and test the complete workflow: create an incident, screen it, inspect similar records, tick checklist items, save a session case and download its JSON file.
9. Copy the final `https://...streamlit.app` URL into the PPT's final **Project Links** slide and README.

## Production warning

The current prototype stores cases in Streamlit session state only. It does not provide user accounts, secure multi-user records, persistent storage, role-based permissions or audit logs. Do not deploy it for real confidential incident records without adding those controls and reviewing privacy, retention and applicable legal requirements.

## Official deployment documentation

- Streamlit Community Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Deploy an app: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- App dependencies: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- GitHub remotes: https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
