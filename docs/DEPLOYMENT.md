# Deploy the existing SIH26165 repository

This project is already maintained in the public repository:

https://github.com/Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection

Do not create a second repository, delete the existing repository, or initialise a new Git history. The current GitHub repository contains the project history, research notebooks, fitted model and application.

## Current repository settings

- Repository: `Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection`
- Branch: `main`
- Streamlit entrypoint: `app/streamlit_app.py`
- Python version: `3.13` (see `.python-version`)
- Dependency file: `requirements.txt`
- Required fitted model: `artifacts/models/incident_review_engine.joblib`

## Updating the existing repository from a local copy

If you are working in the existing clone, keep its hidden `.git` directory. Copy the updated project files into that working directory, replacing matching files, but never overwrite or delete `.git`.

Then run in PowerShell from the repository root:

```powershell
git status
git add -A
git status
git commit -m "Update SIH26165 incident intelligence application"
git push origin main
```

Review the staged file list before committing. Do not commit the raw OSHA CSV, private reviewer worksheets, local environment files, credentials or confidential incident records. Confirm the fitted model is tracked:

```powershell
git ls-files artifacts/models/incident_review_engine.joblib
```

The command should print the model path. The repository's `.gitignore` contains an explicit exception for this deployment model.

## Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app**.
3. Select the existing repository `Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection`.
4. Select branch `main`.
5. Set the app file path to `app/streamlit_app.py`.
6. Open **Advanced settings** and choose Python 3.13, matching `.python-version` and the fitted model build environment.
7. Choose an available app subdomain and deploy.
8. Check the build logs. Resolve installation or import errors before sharing the deployment.
9. Test incident intake, screening, pattern group, historical matches, checklist, session register and JSON export.

The repository contains a `requirements.txt` file with the dependencies and pinned scikit-learn/joblib versions used by the serialized model.

## After deployment

Copy the generated `https://<app-name>.streamlit.app` URL into the PowerPoint's **Project Links** slide and the README. Verify both the repository and deployment links from a signed-out browser window.

## Prototype limitations

The current case register is held in Streamlit session state. It is not a secure multi-user case-management system and does not provide authentication, persistent storage, role-based access, audit logs or retention controls. Do not enter confidential or identifiable workplace incident information. Organisational use requires those controls and a privacy/safety review.

## Official deployment documentation

- https://docs.streamlit.io/deploy/streamlit-community-cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
