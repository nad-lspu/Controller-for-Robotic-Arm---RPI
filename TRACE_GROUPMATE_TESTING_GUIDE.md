# TRACE Testing Guide para sa Groupmates (Taglish)

**Version:** Draft 3 — November 3, 2026  
**Setup:** Windows PC + VS Code + PowerShell  
**Goal:** Ma-try ninyo mismo ang TRACE Laboratory at Controller, then i-record kung ano ang gumagana at kung ano ang may error.

> **Hi guys!** Ito yung step-by-step guide natin. Sundan lang in order. Hindi kailangan kabisado ang commands—copy-paste lang sa tamang terminal. Kapag may error, huwag agad mag-delete o mag-edit ng random files. Screenshot or copy the *sanitized* error, then send sa group chat.

## Bago tayo magsimula

Kailangan ninyo ng Windows 10/11 PC, internet for initial setup, **VS Code**, **Git**, **Python 3.12**, **Node.js + npm**, at GitHub account na may access sa **both private repositories**:

- Laboratory: https://github.com/nad-lspu/Laboratory-for-Robotic-Arm
- Controller: https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI

**Important:** Kapag `404` ang GitHub link, usually wala pang access or hindi pa accepted ang invitation. Ask the repository owner to invite you under **Settings → Collaborators**, then accept the GitHub invitation.

**Safety muna:** Windows mock-mode testing lang ito. **Huwag muna ikabit o paandarin ang powered robotic arm.** Sa Raspberry Pi, may initialization code na puwedeng gumalaw ang servos. Hindi pa ito hardware testing guide.

**Security:** Huwag mag-share ng `.env`, passwords, tokens, database files, or screenshots na may credentials. Huwag gamitin ang lumang default super-admin password na makikita sa Git history.

## PART 1 — Open VS Code at kunin ang projects

### Step 1 — Open VS Code

1. Click **Start** sa Windows.
2. Search **Visual Studio Code**, then open.
3. Sa menu, click **Terminal → New Terminal**.
4. Check na PowerShell ang terminal (usually may `PS` sa prompt). Kung hindi, click dropdown sa terminal tab at select **PowerShell**.

### Step 2 — Gumawa ng folder para sa TRACE

Sa VS Code terminal, paste:

```powershell
cd $HOME\Downloads
mkdir TRACE-Testing
cd TRACE-Testing
```

Kung existing na ang `TRACE-Testing` folder, okay lang; gamitin ang `cd TRACE-Testing`.

### Step 3 — Clone ang dalawang repositories

```powershell
git clone https://github.com/nad-lspu/Laboratory-for-Robotic-Arm.git
git clone https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI.git
```

**Expected:** May dalawang folders: `Laboratory-for-Robotic-Arm` at `Controller-for-Robotic-Arm---RPI`. If authentication is requested, log in using your own GitHub account. **Do not send your GitHub token sa group chat.**

### Step 4 — Open Laboratory project sa VS Code

```powershell
code .\Laboratory-for-Robotic-Arm
```

If hindi gumana ang `code`, use **File → Open Folder** and select `Downloads\TRACE-Testing\Laboratory-for-Robotic-Arm`.

Sa Explorer sidebar, dapat may `backend` at `frontend` folders. Huwag muna mag-edit ng code.

## PART 2 — Start TRACE Laboratory backend (Terminal 1)

### Step 5 — Open Terminal 1

Sa VS Code: **Terminal → New Terminal**. Make sure nasa Laboratory project root ka. Check using:

```powershell
pwd
```

Then:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Expected:** Dependencies install successfully. First install can take a while. If `py -3.12` is not found, check `py --list` and ask the maintainer before switching Python versions.

### Step 6 — Create your own local `.env` (configuration file)

Guys, ito yung settings file ng backend. **Hindi ito account creation**; dito naka-set kung saan ang database at paano gumagana ang login, email, at storage.

1. Make sure nasa `backend` folder pa rin ang Terminal 1.
2. Check kung kasama na sa cloned repository ang `backend/.env.example`:

```powershell
Test-Path .\.env.example
```

3. Kapag `True`, copy it:

```powershell
Copy-Item .\.env.example .\.env
code .\.env
```

Kapag `False`, **stop muna and ask the maintainer to commit the reviewed `.env.example`**. Huwag mag-imbento ng credentials.

4. Generate a **unique local** authentication secret in PowerShell:

```powershell
$bytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($bytes)
$rng.Dispose()
[Convert]::ToBase64String($bytes)
```

Copy the generated string into `SECRET_KEY=` inside your own `.env`. **Do not send this secret to anyone.**

5. For the initial SQLite setup, the template uses `DATABASE_URL=sqlite:///./robotic_arm.db`. Keep that value when following this guide. The database is local to your own computer, so accounts created on another computer won't automatically appear here.

6. The email and model-storage values in `.env.example` are **placeholders only**. They are not working SMTP or cloud credentials. Basic backend startup may work with placeholders, but **email verification, password recovery, and storage operations may fail**. Do not use real personal/production secrets just to pass this test. Ask the maintainer before testing those features.

7. Save `.env` with **Ctrl+S**. Never commit `.env`, send it to the group chat, or restore the historical default Admin password. Do not uncomment `initial_super_admin_setup()`.

**Expected:** May sariling `backend/.env` ka na. This is a **setup template**, not yet a fully verified clean-install configuration. If startup fails, screenshot only the error without secrets and report `ENV-01 = BLOCKED`.

### Step 7 — Start the Laboratory application (recommended: Electron handles its backend)

**Important:** Sa actual testing natin, `npm run dev` tried to start FastAPI automatically. If you manually start Uvicorn on port `8000` *and then* run `npm run dev`, magkakaroon ng `Errno 10048 / address already in use`.

So **don't manually run Laboratory Uvicorn** for the normal desktop test. Leave Terminal 1 free after dependency installation. We'll start the desktop app in Step 11, and Electron will attempt to launch the backend.

After Step 11, check http://127.0.0.1:8000/ in your browser. **Expected:** `Health Check Complete`. If unreachable, check the `npm run dev` terminal and report the error; don't start random duplicate servers.

**Optional API-only testing:** If you are *not* running Electron, you can start Laboratory manually from the `backend` folder using:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Stop it with **Ctrl+C before launching `npm run dev`**.

## PART 3 — Start TRACE Controller backend (Terminal 2)

### Step 8 — Open a second VS Code terminal

Click the **+** button in the Terminal panel. From the Laboratory project root, navigate to the Controller folder using an absolute path:

```powershell
cd "$HOME\Downloads\TRACE-Testing\Controller-for-Robotic-Arm---RPI\backend"
```

### Step 9 — Install Controller dependencies

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install --upgrade pip
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 10 — Run Controller backend on port 8001

```powershell
.\.venv312\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8001 --reload
```

Open http://127.0.0.1:8001/ in your browser.

**Expected:** `Health Check Complete`. Keep Terminal 2 open. On Windows this uses mock GPIO; **do not run this procedure on a powered Raspberry Pi arm**.

## PART 4 — Open TRACE Laboratory frontend (Terminal 3)

### Step 11 — Open a third terminal

Click **+** again in VS Code terminal. Run:

```powershell
cd "$HOME\Downloads\TRACE-Testing\Laboratory-for-Robotic-Arm\frontend"
npm install
npm run dev
```

**Expected:** Development server/Electron starts. Follow the local address shown in the terminal or the Electron window. Keep this terminal open too.

**Reminder:** Dapat running ang **Laboratory backend (8000, launched by Electron)**, **Controller backend (8001)**, at **Laboratory frontend**. Current Programming integration uses `127.0.0.1:8001`, so same-PC setup muna tayo. Huwag mag-start ng separate Laboratory backend kapag Electron na ang nag-launch nito.

## PART 5 — Create a Student test account, then test logins

> **Guys, dito natin gagamitin yung `127.0.0.1:8000/docs` na ginamit natin sa testing.** This is FastAPI's Swagger UI. It can send requests to the running backend. **Hindi ito `.env` editor.** Dapat working na ang backend bago ito buksan.
>
> **Security note:** Current `POST /auth/create` has no visible authorization check and its schema accepts `student`, `professor`, and `admin`. This is a known security issue pending a code fix. **Use only `student` in this guide; do not use this endpoint to create privileged accounts.** Use local test data only, and don't expose port 8000 publicly.

### Step 12 — Open Swagger UI (AUTH-API-01)

1. Make sure the TRACE desktop app is running and http://127.0.0.1:8000/ shows `Health Check Complete`.
2. Open **Chrome/Edge** and go to **http://127.0.0.1:8000/docs**.
3. Scroll to the **auth** section. Hanapin ang `POST /auth/create` and `POST /auth/signin`.

**Expected:** Swagger UI loads with the available endpoints. If it doesn't, check the Electron terminal first.

### Step 13 — Create a Student test account (AUTH-CREATE-01)

1. Click **`POST /auth/create` → Try it out**.
2. Swagger shows a JSON request body. **Keep all fields that Swagger requires**, based on the displayed schema. In particular, use:
   - `id`: a unique **test Student ID** (e.g., `TEST-STU-001`; actual format may be validated by the API)
   - `email`: a test email you control
   - `password` and `confirm_password`: your own matching test password
   - `user_type`: **`student` only**
3. For other required fields (such as name), follow the schema shown in Swagger. Don't delete required fields.
4. Click **Execute** **once**.
5. Look at **Response code** and **Response body**.

**Expected:** `201 Created` and a user response. If `409 Conflict`, the ID/email already exists—choose a new test ID/email rather than trying to overwrite someone else's account. For `422`, inspect which required field is missing or invalid. Don't post the password or complete request body in the group chat.

**Important:** This creates the account in *your local SQLite database*, not in a shared online database. New accounts may be **unverified**; some pages may require email verification. The email placeholders in Step 6 cannot deliver verification emails.

### Step 14 — Test Student login in Swagger (AUTH-STUDENT-API-01)

1. Expand **`POST /auth/signin` → Try it out**.
2. In the form, enter the **Student ID** from Step 13 in the `username` field (**not the email**).
3. Enter the same password in `password`.
4. Click **Execute**.

**Expected:** `200 OK` with an `access_token` and `token_type`. **Never screenshot, copy to group chat, or share the token.** This confirms credentials work; it does **not** guarantee that all verified-user features are accessible.

### Step 15 — Test Student login in the desktop app (AUTH-STUDENT-01)

1. Return to TRACE Laboratory. If logged in as someone else, click **Logout**.
2. On the Sign In screen, enter the **test Student ID** and password. The backend expects an ID, not an email; follow the actual UI labels if different and report any mismatch.
3. Click **Sign In**.
4. Check whether the Student dashboard opens. Try **Classrooms** and **Activities** if visible.
5. Record errors such as `Unauthorized`, `403 Forbidden`, or a blank page. Log out when done.

**Expected:** Login should succeed with valid credentials. Some pages may still be blocked if verification or classroom membership is required. Mark those features separately, not as a login failure.

### Step 16 — Test existing Admin account (AUTH-ADMIN-01)

1. **Do not create an Admin using `POST /auth/create`.** Ask the maintainer for an approved, separately provisioned **local Admin test account** and its setup procedure.
2. Log in using its **Admin/Employee ID** and password (not email).
3. Check that the Admin page loads and record the visible menu options. **Do not assume a user list exists**; our earlier Admin test confirmed login but not a user-list feature.
4. If the terminal shows `GET /activity/2 → 403 Forbidden`, note it as a **separate activity authorization issue**, even if the Admin page opens.
5. Log out.

**Expected:** Existing approved Admin credentials work. If no approved Admin test account exists on the groupmate's local database, mark **BLOCKED**, not FAIL.

### Step 17 — Test existing Professor account (AUTH-PROF-01)

1. Use a separately approved Professor test account; **don't create one through public registration**.
2. Log in with the **Employee ID** and password.
3. Check the dashboard, **Classrooms**, and **Activities** (if visible).
4. Record `Unauthorized` or blank screens, then log out.

**Expected:** Authorized pages work. If no approved Professor account exists, mark **BLOCKED**.

### Step 18 — Wrong-password test (AUTH-NEG-01)

1. On the Sign In screen, enter your own test Student ID.
2. Type an intentionally incorrect password and click **Sign In once**.
3. Record the result without sharing credentials.

**Expected:** Login is rejected cleanly, without exposing sensitive information. Don't repeatedly guess passwords.

## PART 6 — Programming tab: actual TRACE tests

**Important:** The current **Run** button does **not** execute what you typed in the editor. It starts a fixed Controller test script (`backend/test_execution.py`). The validation/demo features only support restricted literal `print()` statements. This is intentional for the current development test, not a full Python sandbox.

### Step 19 — Open Programming (PROG-01)

1. Sign in with an approved account that can access Programming.
2. Click **Programming** in the navigation.
3. Check if editor, file controls, validation/demo controls, **Run**, **Stop**, and output area are visible.

**Expected:** Programming page opens without a blank screen.

### Step 20 — Type sample Python code (PROG-02)

Paste this into the editor:

```python
print("Hello TRACE")
```

Try **Save/Download** and save it as `hello_trace.py`. Then inspect the saved file. **Expected:** File extension is `.py` and content matches.

### Step 21 — Upload the Python file (PROG-03)

1. Clear or change the editor text.
2. Click **Upload/Open file** (use the actual label in your UI).
3. Select `hello_trace.py`.

**Expected:** Editor shows `print("Hello TRACE")` again.

### Step 22 — Wrong file extension (PROG-04)

Try uploading a `.txt` file. **Expected:** App rejects it or shows a `.py`-only message. Record actual behavior.

### Step 23 — Validate allowed code (PROG-05)

With `print("Hello TRACE")` in the editor, click **Validate** (or equivalent). **Expected:** Accepted by Controller when backend on port 8001 is running.

### Step 24 — Validate disallowed code (PROG-06)

Replace editor content with:

```python
import os
```

Click **Validate**. **Expected:** Rejected. This test is validation only; **do not attempt to run arbitrary imported code**.

### Step 25 — Demo output (PROG-07)

Restore:

```python
print("Hello TRACE")
```

Click the demo/execute-demo control if shown. **Expected:** Demo result includes `Hello TRACE`.

### Step 26 — Test Run, output, and Stop (PROG-08 to PROG-10)

1. Keep both backends running.
2. Click **Run** once.
3. Wait about **3 seconds**.
4. Watch the output area; it should update periodically.
5. Click **Stop**.
6. Check that running stops. Note that the final output lines may be missing due to polling timing.

**Expected:** Fixed Controller test process starts and stops. **Do not claim the editor code was executed.**

### Step 27 — Connection-loss test (NET-01/NET-02)

1. In **Terminal 2**, press **Ctrl+C** to stop Controller backend.
2. Return to Programming and try **Validate** again.
3. Record the connection error shown.
4. Restart Controller using the same command from Step 10.
5. Retry validation.

**Expected:** Failure is reported when disconnected; validation works again after restart. **Do not click Run repeatedly while troubleshooting.**

## PART 7 — Activities, camera, and build checks

### Step 28 — Activities (ACT-01)

Sign in using an authorized test role, then open **Activities**. Record if it loads or shows `Unauthorized`, gray screen, or blank content. **Known issue:** This page previously failed. Mark **FAIL** if reproduced.

### Step 29 — Camera navigation (CAM-01)

If camera UI is available on your current setup, open it, navigate to another page, then return. Record whether the feed resumes. **Known issue:** Feed may stop after switching tabs. Do not connect a powered robotic arm for this test.

### Step 30 — Optional frontend build check (BUILD-01)

Open another terminal:

```powershell
cd "$HOME\Downloads\TRACE-Testing\Laboratory-for-Robotic-Arm\frontend"
npm run build
```

**Expected for testing:** Record the actual result. Previous development checks found TypeScript build errors, so a failure here is a known area for investigation—not a reason to invent a fix during groupmate testing.

## PART 8 — Optional Controller API test (PowerShell)

If Programming UI is not working but Controller backend on 8001 is running, open a new PowerShell terminal and test:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/
$body = @{ code = 'print("Hello TRACE")' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/gpio/validate_code -ContentType 'application/json' -Body $body
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/gpio/execute_demo_code -ContentType 'application/json' -Body $body
```

**Expected:** Health check, successful restricted validation, and demo output. Record any HTTP error and status; never share tokens.

## PART 9 — Paano mag-record ng results

For each test, use: **PASS** (gumagana), **FAIL** (may bug), **BLOCKED** (kulang setup/account), or **NOT TESTED** (hindi pa ginawa).

| Test ID | Test | Result | Notes / screenshot |
|---|---|---|---|
| ENV-01 | Laboratory backend 8000 | | |
| ENV-02 | Controller backend 8001 | | |
| UI-01 | Frontend opens | | |
| AUTH-API-01 | Swagger UI opens | | |
| AUTH-CREATE-01 | Create local Student test account | | |
| AUTH-STUDENT-API-01 | Student login through Swagger | | |
| AUTH-ADMIN-01 | Admin login | | |
| AUTH-PROF-01 | Professor login | | |
| AUTH-STUDENT-01 | Student login | | |
| AUTH-NEG-01 | Wrong password | | |
| ACT-01 | Activities page | | |
| PROG-01 | Programming opens | | |
| PROG-02/03 | Save and upload `.py` | | |
| PROG-04 | Reject `.txt` | | |
| PROG-05/06 | Valid/invalid code | | |
| PROG-07 | Demo output | | |
| PROG-08/09/10 | Run, output, Stop | | |
| NET-01/02 | Disconnect and reconnect | | |
| CAM-01 | Camera navigation | | |
| BUILD-01 | Frontend build | | |

### Sample bug report (copy-paste)

```text
Name / date:
Test ID:
Role used: Admin / Professor / Student / None
What I clicked (step by step):
Expected result:
Actual result:
Error message (redacted):
Screenshot (no passwords/tokens):
Windows version:
Repository commit hash:
```

## PART 10 — Common errors, quick checks

- **GitHub 404:** Hindi pa accepted ang collaborator invite, wrong account, or wrong URL.
- **`python` / `py -3.12` not found:** Install/check Python 3.12; run `py --list`.
- **`npm` not recognized:** Install Node.js and reopen terminal.
- **Backend fails to start:** Confirm dependencies installed and `backend/.env` exists with valid settings. Remember placeholders do not make email/storage work.
- **`Address already in use`:** Most likely two Laboratory backends were started (manual Uvicorn + Electron). Stop the manual one, then restart `npm run dev`.
- **Programming cannot connect:** Check Terminal 2 and http://127.0.0.1:8001/.
- **Activities says Unauthorized:** Record it; this is a known bug candidate.
- **No Admin/Professor login available:** Mark `BLOCKED` and ask for approved local provisioning. Student account can be created through Swagger for local tests. **Don't enable old default admin setup.**

## PART 11 — Pagkatapos ng testing

1. Click **Stop** sa Programming if the test process is still running.
2. In each server terminal, press **Ctrl+C** to stop the backend/frontend.
3. Save the test results and sanitized screenshots.
4. Send results to the maintainer/group lead.
5. **Don't push changes to GitHub** unless assigned; use a branch and pull request when collaboration starts.

## Notes para sa maintainer bago ipamigay sa groupmates

This is a detailed **draft**, not yet a fully verified clean-PC installation procedure. Before asking everyone to follow it, prepare: (1) a committed, reviewed `.env.example` and verified local startup; (2) approved Admin/Professor provisioning and a fix for unrestricted privileged registration; (3) confirmation that dependency installation works on a fresh PC; and (4) a screenshot or exact labels of the current Programming controls. Some UI labels and role permissions need to be checked against the running application. The known default password remains in historical Git commits; keep repositories private and never reuse that credential.
