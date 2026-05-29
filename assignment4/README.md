# IoT Assignment 4 — ThingsBoard Hello World

Cloud IoT platform assignment using ThingsBoard Cloud. Covers device provisioning, telemetry, real-time dashboards, alarm rules, and multi-tenant customer management.

---

## Project Structure

```
assignment4/
├── docs/
│   └── Assignment4_Yakira_Siboni.pdf
└── screenshots/
    ├── 01-login.png
    ├── 02-device-provisioned.png
    ├── 03-telemetry-active.png
    ├── 04-dashboard.png
    ├── 05-alarm-rule.png
    ├── 06-alarm-triggered.png
    ├── 07-customer-created.png
    └── 08-customer-user-activated.png
```

---

## Steps Completed

| Step | Description |
|------|-------------|
| 1 | Signed up and logged in to ThingsBoard Cloud |
| 2 | Provisioned a device (`Thermometer`) and pushed telemetry via HTTP |
| 3 | Built a real-time dashboard with value card, time series chart, and alarms table |
| 4 | Defined a `High temperature` alarm rule (threshold > 25°C, severity: Critical) |
| 5 | Triggered the alarm by pushing temperature = 26 |
| 6 | Created a customer and assigned the device and dashboard to them |
| 7 | Created a customer user, activated via link, and verified limited role access |

---

## Reference Links

- ThingsBoard Cloud: https://thingsboard.cloud
- Hello World Guide: https://thingsboard.io/docs/getting-started-guides/helloworld/
- Demo instance: https://demo.thingsboard.io/home
