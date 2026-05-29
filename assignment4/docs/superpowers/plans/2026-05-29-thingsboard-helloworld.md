# ThingsBoard Hello World (Assignment 4) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete all 5 steps of the official ThingsBoard "Hello World" QuickStart, capture ≥5 screenshots of key moments, and produce a Word report to submit as Assignment #4.

**Architecture:** Browser-driven workflow against ThingsBoard Cloud. Telemetry is sent via ThingsBoard's built-in "Check connectivity" tool (generates platform-specific shell commands). No custom code needed — the guide is entirely UI + generated CLI commands.

**Source:** https://thingsboard.io/docs/getting-started-guides/helloworld/

---

## File Structure

```
assignment4/
├── Hands-On 7.pptx                    (source spec — don't touch)
├── screenshots/
│   ├── 01-login.png
│   ├── 02-device-provisioned.png
│   ├── 03-telemetry-active.png
│   ├── 04-dashboard.png
│   ├── 05-alarm-rule.png
│   ├── 06-alarm-triggered.png
│   ├── 07-customer-created.png
│   └── 08-customer-user-activated.png
├── report/
│   ├── build_report.py
│   └── Assignment4_Report.docx
└── docs/superpowers/plans/2026-05-29-thingsboard-helloworld.md
```

---

## Task 0: Account Setup — Sign Up & Log In

**Files:**
- Screenshot: `assignment4/screenshots/01-login.png`

- [ ] **Step 1: Sign up**

  Navigate to: https://thingsboard.cloud/signup

  Fill in your details and click **Create account**. Verify your email if prompted.

- [ ] **Step 2: Log in**

  Go to https://thingsboard.cloud and sign in (Google, GitHub, Apple, or email).

  Expected result: Redirected to the ThingsBoard Tenant interface homepage.

- [ ] **Step 3: Screenshot `01-login.png`**

  Capture the ThingsBoard home screen showing you are authenticated (your account name/email visible).

---

## Task 1: Step 1 — Provision and Connect a Device

**Files:**
- Screenshot: `assignment4/screenshots/02-device-provisioned.png`
- Screenshot: `assignment4/screenshots/03-telemetry-active.png`

### 1.1 Create the Device

- [ ] **Step 1: Navigate to Devices**

  Left sidebar → **Entities → Devices**

- [ ] **Step 2: Add a new device**

  Click **+ Add device → Add new device** (upper-right corner).

  Fill in the form:
  - Device name: `Thermometer`
  - Device profile: leave as `default` (unchanged)

  Click **Add**.

- [ ] **Step 3: Screenshot `02-device-provisioned.png`**

  Capture the device details screen showing `Thermometer` was created (status will show **Inactive** at this point — that's expected).

### 1.2 Send Telemetry via Check Connectivity

- [ ] **Step 4: Open the "Check connectivity" dialog**

  On the Thermometer device page, click the **Check connectivity** button (or it may open automatically after device creation).

- [ ] **Step 5: Configure the connectivity options**

  In the dialog, select your preferences:
  1. **Shell**: Windows (PowerShell or CMD)
  2. **Protocol**: HTTP
  3. **Client tool**: cURL (or PowerShell's `Invoke-WebRequest` if cURL isn't available)

  ThingsBoard will generate a ready-to-run command containing your device's access token automatically.

- [ ] **Step 6: Run the generated command**

  Copy the generated command and run it in PowerShell. It will send a temperature value of 25 to ThingsBoard.

  Example of what the generated command looks like (your token will differ):
  ```powershell
  curl -v -X POST --location "https://thingsboard.cloud/api/v1/YOUR_TOKEN/telemetry" `
    --header "Content-Type: application/json" `
    --data-raw "{"temperature": 25}"
  ```

  Expected result: The device status changes from **Inactive** → **Active** in the ThingsBoard UI.

- [ ] **Step 7: Verify telemetry in Latest Telemetry tab**

  Close the dialog. Click **Thermometer** → **Latest telemetry** tab.
  You should see `temperature` with value `25` and a recent timestamp.

- [ ] **Step 8: Screenshot `03-telemetry-active.png`**

  Capture the **Latest telemetry** tab showing `temperature = 25` and the device status **Active**.

---

## Task 2: Step 2 — Visualize Data on a Dashboard

**Files:**
- Screenshot: `assignment4/screenshots/04-dashboard.png`

- [ ] **Step 1: Create a new dashboard**

  Left sidebar → **Dashboards** → **+ Add dashboard → Create new dashboard**.
  - Title: `My Dashboard`
  - Click **Add**

- [ ] **Step 2: Open the dashboard editor**

  Click on `My Dashboard` → click the **Edit** (pencil) icon in the top-right corner.

- [ ] **Step 3: Add a Value Card widget (current temperature)**

  - Click **+ Add new widget** (center of the canvas)
  - Select **Cards → Value card**
  - Datasource: Device = `Thermometer`
  - Data key: `temperature`
  - Click **Add**
  - Resize the widget as desired

- [ ] **Step 4: Add a Time Series Chart widget**

  - Click **+ Add widget** (edit mode toolbar)
  - Select **Charts → Time series chart**
  - Datasource: Device = `Thermometer`
  - Series key: `temperature`
  - Click **Add**
  - Resize and position below or beside the value card

- [ ] **Step 5: Add an Alarms Table widget**

  - Click **+ Add widget**
  - Select **Alarm widgets → Alarms table**
  - Datasource: Device = `Thermometer`
  - Configure alarm severity and status filters as desired
  - Click **Add**

- [ ] **Step 6: Save the dashboard**

  Click the **Save** (checkmark) button in the top-right corner to exit edit mode.

- [ ] **Step 7: Screenshot `04-dashboard.png`**

  Capture the saved dashboard showing all three widgets — Value card, Time series chart, and Alarms table.

---

## Task 3: Step 3 — Configure Alarms & Notifications

**Files:**
- Screenshot: `assignment4/screenshots/05-alarm-rule.png`
- Screenshot: `assignment4/screenshots/06-alarm-triggered.png`

### 3.1 Create an Alarm Rule

- [ ] **Step 1: Navigate to Alarm Rules**

  Left sidebar → **Alarms → Alarm rules** → **+ Add alarm rule → Create new alarm rule**

- [ ] **Step 2: Fill in general settings**

  - Alarm type: `High temperature`
  - Target entity: `default`

- [ ] **Step 3: Add a telemetry argument**

  Click **Add argument**:
  - Entity type: `Current entity`
  - Argument type: `Latest telemetry`
  - Time series key: `temperature`
  - Argument name: `temperature`
  - Click **Add**

- [ ] **Step 4: Define the trigger condition**

  Click **Add trigger condition**:
  - Severity: `Critical`
  - Script condition: `return temperature > 25;`
  - Click **Save**

- [ ] **Step 5: Finalize the rule**

  Click **Add** to activate the alarm rule.

- [ ] **Step 6: Screenshot `05-alarm-rule.png`**

  Capture the alarm rule list or detail screen showing the `High temperature` rule with its condition.

### 3.2 Trigger the Alarm

- [ ] **Step 7: Send telemetry above the threshold**

  Go back to **Entities → Devices → Thermometer → Check connectivity**.

  In the generated command, change the temperature value to `26` (above the 25 threshold) and run it:

  ```powershell
  curl -v -X POST --location "https://thingsboard.cloud/api/v1/YOUR_TOKEN/telemetry" `
    --header "Content-Type: application/json" `
    --data-raw "{"temperature": 26}"
  ```

- [ ] **Step 8: Verify the alarm fired**

  Navigate to the **Alarms** page (left sidebar) or check the **Alarms tab** on the Thermometer device. You should see a `High temperature` alarm with status **Active** and severity **Critical**.

  Also check the **bell icon** (top-right) → **Notification center** for a push notification.

- [ ] **Step 9: Screenshot `06-alarm-triggered.png`**

  Capture the Alarms page or device Alarms tab showing the active `High temperature` alarm.

---

## Task 4: Step 4 — Share Data with a Customer

**Files:**
- Screenshot: `assignment4/screenshots/07-customer-created.png`

### 4.1 Create a Customer

- [ ] **Step 1: Navigate to Customers**

  Left sidebar → **Customers** → **+ Add customer**

  - Title: `My New Customer`
  - Click **Add**

  Expected result: "The Customer has been created."

### 4.2 Assign Device to Customer

- [ ] **Step 2: Assign the Thermometer device**

  In the Customers list, click **Manage customer devices** for `My New Customer`.
  Click **+ Assign new device** → select `Thermometer` → click **Assign**.

  Expected result: "The device is assigned to the Customer."

### 4.3 Assign Dashboard to Customer

- [ ] **Step 3: Assign the dashboard**

  In the Customers list, click **Manage customer dashboards** for `My New Customer`.
  Click **+ Assign new dashboard** → select `My Dashboard` → click **Assign**.

  Expected result: Customer now has read-only access to the dashboard.

- [ ] **Step 4: Screenshot `07-customer-created.png`**

  Capture the customer screen showing `My New Customer` with the assigned device and dashboard.

---

## Task 5: Step 5 — Create and Activate a Customer User

**Files:**
- Screenshot: `assignment4/screenshots/08-customer-user-activated.png`

### 5.1 Create the User

- [ ] **Step 1: Navigate to Customer Users**

  Left sidebar → **Customers** → find `My New Customer` → click **Manage customer users** → **+ Add user**

  Fill in the form:
  - Email address: (use any valid email you control, e.g. a secondary address or a temp email)
  - First name, Last name: optional
  - Activation method: **Display activation link**

  Click **Add**.

- [ ] **Step 2: Copy the activation link**

  When the activation link is displayed, copy it. Click **OK**.

### 5.2 Activate the User

- [ ] **Step 3: Activate in a new browser tab**

  Open a new incognito/private browser window. Paste the activation link.

  On the activation form:
  - Enter a password (twice)
  - Click **Create password**

  Expected result: Automatic login to ThingsBoard as the customer user. The customer user sees only `My Dashboard` and the `Thermometer` device — no admin features.

- [ ] **Step 4: Screenshot `08-customer-user-activated.png`**

  Capture the customer user's ThingsBoard view showing the limited dashboard-only interface.

---

## Task 6: Build the Submission Report

**Files:**
- Create: `assignment4/report/build_report.py`
- Output: `assignment4/report/Assignment4_Report.docx`

- [ ] **Step 1: Install python-docx**

  ```powershell
  pip install python-docx
  ```

  Expected: `Successfully installed python-docx-...` (or `already satisfied`)

- [ ] **Step 2: Create the report builder**

  Create `assignment4/report/build_report.py`:

  ```python
  from docx import Document
  from docx.shared import Inches
  import os

  doc = Document()
  doc.add_heading("Assignment #4 — ThingsBoard Hello World", 0)
  doc.add_paragraph("Student: Yakira_S")
  doc.add_paragraph("Course: IoT")
  doc.add_paragraph("Date: 2026-05-29")
  doc.add_paragraph()

  steps = [
      ("Login to ThingsBoard Cloud",
       "Signed up at thingsboard.cloud and logged in via the web interface.",
       "../screenshots/01-login.png"),
      ("Step 1: Device Provisioned",
       "Created a device named 'Thermometer' using Entities → Devices → Add new device.",
       "../screenshots/02-device-provisioned.png"),
      ("Step 1: Telemetry Active",
       "Used the built-in 'Check connectivity' tool to send temperature=25 via HTTP. "
       "Device status changed to Active and Latest Telemetry shows the data.",
       "../screenshots/03-telemetry-active.png"),
      ("Step 2: Real-Time Dashboard",
       "Created 'My Dashboard' with three widgets: Value card, Time series chart, and Alarms table — "
       "all showing live data from the Thermometer device.",
       "../screenshots/04-dashboard.png"),
      ("Step 3: Alarm Rule Defined",
       "Created a 'High temperature' alarm rule with condition: return temperature > 25; (severity: Critical) "
       "via Alarms → Alarm rules.",
       "../screenshots/05-alarm-rule.png"),
      ("Step 3: Alarm Triggered",
       "Sent temperature=26 via Check connectivity. ThingsBoard raised a Critical 'High temperature' alarm "
       "visible in the Alarms tab.",
       "../screenshots/06-alarm-triggered.png"),
      ("Step 4: Customer Created",
       "Created customer 'My New Customer' and assigned the Thermometer device and My Dashboard to them.",
       "../screenshots/07-customer-created.png"),
      ("Step 5: Customer User Activated",
       "Created a customer user account and activated it via the activation link. The customer user sees "
       "only the shared dashboard — no admin features.",
       "../screenshots/08-customer-user-activated.png"),
  ]

  for title, description, img_path in steps:
      doc.add_heading(title, level=1)
      doc.add_paragraph(description)
      abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), img_path))
      if os.path.exists(abs_path):
          doc.add_picture(abs_path, width=Inches(5.5))
      else:
          doc.add_paragraph(f"[Screenshot not found: {img_path}]")
      doc.add_paragraph()

  out_path = os.path.join(os.path.dirname(__file__), "Assignment4_Report.docx")
  doc.save(out_path)
  print(f"Report saved to: {out_path}")
  ```

- [ ] **Step 3: Run the report builder** (after all screenshots are captured)

  ```powershell
  cd "C:\Users\Gal Sar\iot-course\assignment4\report"
  python build_report.py
  ```

  Expected output:
  ```
  Report saved to: C:\Users\Gal Sar\iot-course\assignment4\report\Assignment4_Report.docx
  ```

- [ ] **Step 4: Open and verify the report**

  ```powershell
  Start-Process "C:\Users\Gal Sar\iot-course\assignment4\report\Assignment4_Report.docx"
  ```

  Check: all 8 screenshots are present, text is correct, no `[Screenshot not found]` placeholders.

- [ ] **Step 5: Final commit**

  ```powershell
  git add assignment4/
  git commit -m "feat(assignment4): complete ThingsBoard Hello World - all 5 steps + report"
  ```

---

## Spec Coverage

| Spec requirement | Covered by |
|---|---|
| Sign up at thingsboard.cloud | Task 0 |
| Complete QuickStart (all 5 steps) | Tasks 1–5 |
| Connect devices to ThingsBoard | Task 1 |
| Push data from devices to ThingsBoard | Task 1 |
| Build real-time end-user dashboards | Task 2 |
| Define thresholds and trigger | Task 3 |
| Push notifications about new alarms | Task 3 |
| Share data with Customer | Task 4 |
| Create/activate Customer User | Task 5 |
| ≥ 5 screenshots | 8 screenshots across Tasks 0–5 |
| Create doc report | Task 6 |
