# TRACE — Complete Testing Guide for Groupmates

**Version:** Draft 1 · **Scope:** Windows development and mock-hardware testing · **Date:** 2026-11-03

## 1. Purpose and safety boundaries

This guide helps groupmates reproduce the current TRACE development setup, test the Laboratory user interface and Controller API, and document reproducible bugs. **It is not a Raspberry Pi hardware commissioning guide.** On the Raspberry Pi, importing the GPIO module may immediately set angles on 16 servo channels; do not run the hardware backend with an energized arm until movement limits, emergency stop, power supply, and supervision have been reviewed.

**Important current behavior:** The Laboratory editor can save/load `.py` files and submit restricted code for validation or demo interpretation. The **Run** button starts a fixed Controller test program (`backend/test_execution.py`), **not the code typed in the editor**. Do not present this as general Python execution or a secure sandbox. The validator currently supports restricted literal `print()` statements, not arbitrary Python.

**Repositories (private; request access from project owner):**
- Controller: https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI
- Laboratory: https://github.com/nad-lspu/Laboratory-for-Robotic-Arm

Do not post `.env` contents, credentials, database copies, JWTs, access tokens, or screenshots containing them in bug reports. The Laboratory Git history contains an old known default administrator password; never use that password for an active deployment. Do not make the repositories public without a separate security and permission review.

## 2. Test roles and prerequisites

Assign one groupmate as **tester**, one as **observer/recorder**, and one as **developer/triager** where possible. Record the Windows version, Python version, Node/npm versions, repository commit hashes, and test date before testing.

Recommended prerequisites: Windows 10/11, PowerShell, Git, VS Code, Python **3.12** (the previously tested Controller environment used 3.12.10), Node.js and npm compatible with each frontend's `package.json`, and access to the private repositories. Dependencies and clean-machine installation have **not** been comprehensively validated; report installation failures instead of silently changing dependency versions.

Use **two separate terminal windows for backend servers**, plus one for the Laboratory frontend. Keep the arm disconnected: these tests target the Windows mock GPIO environment.

## 3. Obtain code and capture versions

Clone each private repository in a working folder (or use existing checked-out copies):

```powershell
git clone https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI.git
git clone https://github.com/nad-lspu/Laboratory-for-Robotic-Arm.git
```

In each repository run `git status -sb` and `git log -1 --oneline`. Record the commit hashes. The project's development branches are currently named `master`. If the GitHub default branch differs, use the checked-out branch and record it.

## 4. Configure Laboratory backend (Windows)

From the Laboratory repository root:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Environment configuration:** `backend/api/config.py` requires values for `MODEL_STORAGE_KEY_ID`, `MODEL_STORAGE_KEY`, `MODEL_STORAGE_ENDPOINT`, `MODEL_STORAGE_NAME`, `MODEL_STORAGE_PRESIGNED_EXP_SECS`, `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXP_MINS`, `EMAIL_CODE_EXP_MINS`, `TRACE_EMAIL`, and `TRACE_APP_PASSWORD`; `EMAIL_MODE` defaults to `smtp`. Ask the project maintainer for a **safe local development configuration** through a private channel. Do not copy production credentials or commit `.env`. `INITIAL_ADMIN_PASSWORD` is optional and is only for explicitly invoked administrator initialization; automatic initialization is disabled. The exact first-time account provisioning process is **not yet verified**.

The settings file uses `env_file='.env'`, so launch the backend from the **`backend` working directory**. Once the approved `.env` is in place:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

In a browser open http://127.0.0.1:8000/ and expect a JSON response with `Health Check Complete`. If startup fails, record the error **after redacting secrets**. Do not enable `initial_super_admin_setup()` just to make login work.

## 5. Configure Controller backend (Windows mock mode)

From the Controller repository root in a separate PowerShell window:

```powershell
cd backend
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install --upgrade pip
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
.\.venv312\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8001 --reload
```

Open http://127.0.0.1:8001/ and expect `Health Check Complete`. This Windows setup uses mock GPIO/ServoKit rather than real motor control. The Raspberry Pi-specific requirements are in `backend/rpi-requirements.txt` and should **not** be installed for this Windows mock test.

**Note:** Starting both backends from the correct `backend` folders matters for configuration and local database paths. If port 8000 or 8001 is occupied, stop the conflicting process rather than changing the port without also updating frontend configuration.

## 6. Start Laboratory frontend

From the Laboratory repository root in a third PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Follow the URL printed by Vite/Electron. The Laboratory Programming tab currently calls Controller at **`http://127.0.0.1:8001`**, so both applications must run on the **same Windows computer** for these local tests. A real Pi at another IP will not work without updating networking configuration. Do not assume that Electron packaging (`npm run dist:win`) is working: the Laboratory frontend previously had unrelated TypeScript build errors.

## 7. Functional test cases

For every test record **Pass / Fail / Blocked / Not tested**, actual behavior, screenshot or sanitized console log, and issue ID.

| ID | Procedure | Expected result / interpretation |
|---|---|---|
| ENV-01 | Start Laboratory backend on 8000 and open `/` | Health-check JSON responds. |
| ENV-02 | Start Controller backend on 8001 and open `/` | Health-check JSON responds. |
| UI-01 | Launch Laboratory frontend | Main UI loads without a blank window; record startup errors. |
| AUTH-01 | Sign in using a **maintainer-provided test account** | Successful authentication and navigation; **blocked** if no test account is provisioned. |
| AUTH-02 | Enter incorrect credentials for a test account | Login is rejected without exposing internal errors. |
| CLASS-01 | Open Classrooms | Page loads and shows appropriate authorized data; report access errors. |
| ACT-01 | Open Activities | Record behavior; **known issue:** Unauthorized/gray or blank page may occur. Do not mark a broken page as passing. |
| PROG-01 | Open Programming tab | Python editor, file controls, validation/demo/Run/Stop controls and output area appear. |
| PROG-02 | Type `print("Hello TRACE")`, save `.py` | Browser/download saves a `.py` file; inspect filename and contents. |
| PROG-03 | Upload the saved `.py` | Editor restores the expected text. |
| PROG-04 | Attempt to upload `.txt` | Upload is rejected with a `.py`-only message. |
| PROG-05 | Validate `print("Hello TRACE")` | Validation succeeds while Controller is reachable. |
| PROG-06 | Validate `import os` | Validation fails; do not execute arbitrary imports. |
| PROG-07 | Run demo for `print("Hello TRACE")` | Demo output shows `Hello TRACE` if demo endpoint is operational. |
| PROG-08 | Click Run | Fixed Controller test program starts; **editor text is not executed**. |
| PROG-09 | Observe output while Run is active | Output updates periodically (current UI polls approximately every second). |
| PROG-10 | Click Stop | Fixed test process terminates and UI exits running state; last output may be incomplete. |
| PROG-11 | Stop when no process is running | Application handles `not_running` without crashing (if control is accessible). |
| NET-01 | Stop Controller backend, then attempt validation | UI reports a connection problem rather than silently succeeding. |
| NET-02 | Restart Controller backend, retry validation | Validation works again. |
| CAM-01 | Open camera view, navigate away and back | Record whether video resumes; **known issue:** camera may stop after navigation. No physical arm needed. |
| BUILD-01 | Run `npm run build` in Laboratory frontend | Record compiler output; **previously known TypeScript failures**, not a guaranteed pass. |

For authenticated pages, do not use real student records. Only use test accounts and synthetic test content approved by the maintainer.

## 8. Optional Controller API smoke checks

These commands target the Windows mock Controller on port 8001. Keep the Controller backend running. In PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/

$body = @{ code = 'print("Hello TRACE")' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/gpio/validate_code -ContentType 'application/json' -Body $body
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/gpio/execute_demo_code -ContentType 'application/json' -Body $body
```

To test the fixed Run/Stop lifecycle (not editor-code execution):

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8001/gpio/run_code
Start-Sleep -Seconds 3
Invoke-RestMethod http://127.0.0.1:8001/gpio/program_output
Invoke-RestMethod -Method Post http://127.0.0.1:8001/gpio/terminate_code
```

If a request fails, record HTTP status, sanitized response, and whether the server was running. **Always send Stop** after a successful Run. Do not test user-submitted unrestricted Python execution: it is not an implemented safe feature.

## 9. Known issues and how to classify them

| Issue | Current understanding | Test disposition |
|---|---|---|
| Run ignores editor text | Run launches `backend/test_execution.py` | Known limitation, not a regression unless behavior changes unexpectedly |
| Restricted validation | Literal `print()` statements only; not a secure sandbox | Expected restriction |
| Camera stops after tab navigation | Previously observed | Reproduce and record |
| Activities unauthorized/blank | Previously observed | Reproduce with authorized test account |
| Laboratory production build | Previously reported TypeScript errors | Record exact errors and commit |
| Pi Controller connection | Frontend URL hardcoded to localhost | Out of scope for same-PC test; requires integration work |
| Hardware motion | GPIO module may move servos at initialization | **Do not test on powered arm** |
| Default administrator setup | Disabled; historical known password remains in Git history | Do not enable or reuse historical credentials |

## 10. Bug report template

Copy this for each failure:

```text
Issue ID:
Tester / date:
Component: Laboratory / Controller / Integration
Commit hash(es):
Windows / Python / Node versions:
Test case ID:
Preconditions:
Steps to reproduce:
Expected behavior:
Actual behavior:
Frequency: Always / Sometimes / Once
Severity: Blocker / High / Medium / Low
Screenshot or sanitized log:
Workaround (if any):
```

Severity guidance: **Blocker** = prevents launching or testing core workflow; **High** = major function unusable; **Medium** = intermittent or partial function; **Low** = cosmetic/minor inconvenience. Never include credentials, database content, or personal student information in reports.

## 11. Test session checklist and sign-off

- [ ] Recorded date, tester, OS and both Git commit hashes
- [ ] Confirmed **no powered robotic arm** connected
- [ ] Laboratory backend health check passed (or documented failure)
- [ ] Controller backend health check passed (or documented failure)
- [ ] Laboratory frontend launched (or documented failure)
- [ ] Authentication tested with approved test account or marked blocked
- [ ] Classrooms and Activities tested or marked blocked
- [ ] Programming save/upload/validate/demo tested
- [ ] Fixed Run/Stop/output tested and Stop confirmed
- [ ] Connection-loss recovery tested
- [ ] Camera navigation issue checked
- [ ] Build attempt and errors documented
- [ ] Bugs filed with reproducible steps and sanitized evidence
- [ ] Backend processes stopped at end of session

**Exit criterion for Windows mock testing:** Both backends respond; the frontend opens; programming demo and fixed Run/Stop behavior can be reproduced; every failure has an issue report. This does **not** imply production readiness, safe arbitrary-code execution, Raspberry Pi compatibility, or safe motor operation.

## 12. Work still needed before a fully reproducible groupmate release

1. Publish a sanitized `.env.example` with documented local-development values (no actual credentials).
2. Document a safe first-run test-account provisioning procedure; never reactivate the historical default administrator password.
3. Verify dependency installation on a clean Windows machine and pin supported Node/Python versions.
4. Fix or document Laboratory frontend TypeScript build errors.
5. Make Controller address configurable before remote Pi integration.
6. Perform a separate hardware safety review and create a supervised Raspberry Pi commissioning checklist.

**Maintainer note:** This guide describes observed project behavior and known limitations; some steps are proposed acceptance tests rather than previously verified results. Groupmates should record actual results instead of assuming expected outcomes have been proven.
