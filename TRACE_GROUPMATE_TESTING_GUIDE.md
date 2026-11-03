# TRACE Testing Guide para sa Groupmates (Taglish)

**Version:** Draft 2 — November 3, 2026  
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

### Step 6 — Set up local `.env` (required)

**Stop here kung wala pa kayong approved test `.env` configuration.** Laboratory needs database, authentication, storage, and email settings to start. Ask the project maintainer for **safe local development values via private channel**. Do **not** copy production credentials and do **not** commit `.env` to GitHub.

The `.env` file belongs in `Laboratory-for-Robotic-Arm\backend\.env`. The backend expects settings such as `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, token expiry, model storage configuration, and TRACE email settings. Exact safe first-time configuration is still pending maintainer verification.

**Huwag i-uncomment ang `initial_super_admin_setup()` at huwag gamitin ang historical default password.**

### Step 7 — Run Laboratory backend

Stay inside the `backend` folder:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected:** May Uvicorn running message. Keep this terminal open. Sa browser, visit:

http://127.0.0.1:8000/

**Expected:** JSON with `Health Check Complete`. If may error, record it and mark `ENV-01 = FAIL` or `BLOCKED`.

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

**Reminder:** Dapat sabay-sabay running ang **Laboratory backend (8000)**, **Controller backend (8001)**, at **Laboratory frontend**. Current Programming integration uses `127.0.0.1:8001`, so same-PC setup muna tayo.

## PART 5 — Test accounts: Admin, Professor, Student

> **Before testing:** Ask the maintainer for approved **test accounts** for each role. We have verified that the old default super-admin account was *not* present in the configured local database, but we have **not yet verified a complete first-time admin/student provisioning procedure**. Don't make up an account or reuse the historical password.

### Step 12 — Test Admin login (AUTH-ADMIN-01)

1. Sa TRACE Laboratory window, find the **Sign In** page.
2. Enter the **provided Admin test email and password**.
3. Click **Sign In**.
4. Check if successful ang login and kung may dashboard or appropriate admin pages.
5. Take a screenshot of the result **without showing credentials**.
6. Log out before testing another role.

**Expected:** Admin account can sign in and see only the functions intended for its role. **If no approved Admin test account exists, mark `BLOCKED`, not `PASS`.**

### Step 13 — Test Professor login (AUTH-PROF-01)

1. Sign in with the provided **Professor test account**.
2. Check if dashboard loads.
3. Open **Classrooms** and note whether classroom features appear.
4. Open **Activities** and record any error.
5. Log out.

**Expected:** Authorized pages load without crashes. If Activities shows `Unauthorized` or a gray/blank screen, mark **FAIL (known issue)** and record steps.

### Step 14 — Test Student login (AUTH-STUDENT-01)

1. Sign in with the provided **Student test account**.
2. Check if dashboard loads.
3. Open **Classrooms** and **Activities**, if available to this role.
4. Check if student-only/role-appropriate content is displayed; do not assume students should have admin functions.
5. Log out.

**Expected:** Student can access authorized pages only. If no Student test account is provisioned, mark **BLOCKED**.

### Step 15 — Wrong-password test (AUTH-NEG-01)

1. Use an approved test account email.
2. Type a deliberately incorrect password (not anyone's real password).
3. Click **Sign In** once.

**Expected:** Login is rejected cleanly, without exposing stack traces or sensitive data. Don't repeatedly guess passwords.

## PART 6 — Programming tab: actual TRACE tests

**Important:** The current **Run** button does **not** execute what you typed in the editor. It starts a fixed Controller test script (`backend/test_execution.py`). The validation/demo features only support restricted literal `print()` statements. This is intentional for the current development test, not a full Python sandbox.

### Step 16 — Open Programming (PROG-01)

1. Sign in with an approved account that can access Programming.
2. Click **Programming** in the navigation.
3. Check if editor, file controls, validation/demo controls, **Run**, **Stop**, and output area are visible.

**Expected:** Programming page opens without a blank screen.

### Step 17 — Type sample Python code (PROG-02)

Paste this into the editor:

```python
print("Hello TRACE")
```

Try **Save/Download** and save it as `hello_trace.py`. Then inspect the saved file. **Expected:** File extension is `.py` and content matches.

### Step 18 — Upload the Python file (PROG-03)

1. Clear or change the editor text.
2. Click **Upload/Open file** (use the actual label in your UI).
3. Select `hello_trace.py`.

**Expected:** Editor shows `print("Hello TRACE")` again.

### Step 19 — Wrong file extension (PROG-04)

Try uploading a `.txt` file. **Expected:** App rejects it or shows a `.py`-only message. Record actual behavior.

### Step 20 — Validate allowed code (PROG-05)

With `print("Hello TRACE")` in the editor, click **Validate** (or equivalent). **Expected:** Accepted by Controller when backend on port 8001 is running.

### Step 21 — Validate disallowed code (PROG-06)

Replace editor content with:

```python
import os
```

Click **Validate**. **Expected:** Rejected. This test is validation only; **do not attempt to run arbitrary imported code**.

### Step 22 — Demo output (PROG-07)

Restore:

```python
print("Hello TRACE")
```

Click the demo/execute-demo control if shown. **Expected:** Demo result includes `Hello TRACE`.

### Step 23 — Test Run, output, and Stop (PROG-08 to PROG-10)

1. Keep both backends running.
2. Click **Run** once.
3. Wait about **3 seconds**.
4. Watch the output area; it should update periodically.
5. Click **Stop**.
6. Check that running stops. Note that the final output lines may be missing due to polling timing.

**Expected:** Fixed Controller test process starts and stops. **Do not claim the editor code was executed.**

### Step 24 — Connection-loss test (NET-01/NET-02)

1. In **Terminal 2**, press **Ctrl+C** to stop Controller backend.
2. Return to Programming and try **Validate** again.
3. Record the connection error shown.
4. Restart Controller using the same command from Step 10.
5. Retry validation.

**Expected:** Failure is reported when disconnected; validation works again after restart. **Do not click Run repeatedly while troubleshooting.**

## PART 7 — Activities, camera, and build checks

### Step 25 — Activities (ACT-01)

Sign in using an authorized test role, then open **Activities**. Record if it loads or shows `Unauthorized`, gray screen, or blank content. **Known issue:** This page previously failed. Mark **FAIL** if reproduced.

### Step 26 — Camera navigation (CAM-01)

If camera UI is available on your current setup, open it, navigate to another page, then return. Record whether the feed resumes. **Known issue:** Feed may stop after switching tabs. Do not connect a powered robotic arm for this test.

### Step 27 — Optional frontend build check (BUILD-01)

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
- **Backend fails to start:** Confirm you're in the correct `backend` folder, dependencies installed, and safe `.env` supplied for Laboratory.
- **`Address already in use`:** May ibang process na gumagamit ng port 8000 or 8001. Stop the old process before retrying.
- **Programming cannot connect:** Check Terminal 2 and http://127.0.0.1:8001/.
- **Activities says Unauthorized:** Record it; this is a known bug candidate.
- **No admin/student login available:** Mark `BLOCKED` and ask for approved test accounts. **Don't enable old default admin setup.**

## PART 11 — Pagkatapos ng testing

1. Click **Stop** sa Programming if the test process is still running.
2. In each server terminal, press **Ctrl+C** to stop the backend/frontend.
3. Save the test results and sanitized screenshots.
4. Send results to the maintainer/group lead.
5. **Don't push changes to GitHub** unless assigned; use a branch and pull request when collaboration starts.

## Notes para sa maintainer bago ipamigay sa groupmates

This is a detailed **draft**, not yet a fully verified clean-PC installation procedure. Before asking everyone to follow it, prepare: (1) a sanitized local `.env.example` or private setup instructions; (2) approved test Admin, Professor, and Student accounts and a safe provisioning method; (3) confirmation that dependency installation works on a fresh PC; and (4) a screenshot or exact labels of the current Programming controls. Some UI labels and role permissions need to be checked against the running application. The known default password remains in historical Git commits; keep repositories private and never reuse that credential.
