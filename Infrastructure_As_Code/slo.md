# Agama Service – SLO Documentation

This document defines Service Level Indicators (SLIs) and Service Level Objectives (SLOs) for the **Agama web application**.  
Metrics are collected from **Nginx access logs**, **Loki**, and **Prometheus**.

---

## 🧭 User Journey 1: View Main Agama Page

### Context
A user visits the main Agama landing page (`/`) through the browser.  
They expect the page to load quickly and successfully display content.

---

### **SLI Type:** Availability

#### **SLI Specification**
- **Event:** HTTP request to `/` on Agama web servers  
- **Good event:** HTTP status code is `2xx` or `3xx`  
- **Bad event:** HTTP status code is `4xx` or `5xx`  
- **Measurement:**  
  Rate of successful (`2xx, 3xx`) responses to total valid requests  
  (excluding Grafana/Prometheus requests).  

```promql
sum without (hostname) (rate({job="haproxy"} |~ " [23][0-9][0-9] " [10m]))
/
sum without (hostname) (rate({job="haproxy"} [10m]))
```

#### **SLI Implementation**
- Data source: Loki ("job="haproxy")  
- LogQL query filters only Agama page requests.  
- Success criterion: `HTTP 2xx or 3xx`  
- Collected in Grafana dashboard: *Agama SLO – Availability*

#### **SLO**
- Target: **99 % availability** over a **30-day** rolling window.  
- Alerting threshold: < 95 % for 1 hour.

---

### **SLI Type:** Latency

#### **SLI Specification**
- **Event:** Valid HTTP request to `/`  
- **Good event:** Request completed in < 500 ms.  
- **Measurement:**  
  Ratio of requests with latency < 500 ms to total valid requests.

```promql
avg(
  avg_over_time(
    {job="haproxy"}
    | regexp " (?P<status>[0-9]{3}) (?P<tr>[0-9]+)$"
    | unwrap tr
    [10m]
  )
)
```

#### **SLI Implementation**
- Latency extracted from Nginx access logs via LogQL regexp.  
- Collected by Promtail → Loki → Grafana.  
- Valid requests exclude internal monitoring endpoints.

#### **SLO**
- Target: **95 % of requests complete < 500 ms** over a **7-day** window.

---

## 🧭 User Journey 2: Submit Data via Agama API

### Context
A user submits a form or API request (`/api/submit`).  
They expect the request to succeed and be processed promptly.

---

### **SLI Type:** Availability

#### **SLI Specification**
- **Event:** HTTP POST to `/api/submit`  
- **Good event:** Status `201 Created` or `200 OK`  
- **Bad event:** Timeout or `5xx` error  
- **Measurement:**
  ```
  (successful_requests / total_requests) * 100
  ```

#### **SLO**
- Target: **98 % successful API submissions** over a **30-day** period.

---

### **SLI Type:** Latency



---

## ⚙️ Additional Observability Metrics
| Metric | Description | Source |
|---------|--------------|--------|
| `loki_log_messages_total` | Count of log lines received by Loki | Prometheus → Loki metrics |
| `promtail_sent_entries_total` | Count of log entries sent to Loki | Prometheus → Promtail metrics |
| `node_cpu_seconds_total` | CPU utilization (Infra health) | Prometheus Node Exporter |
| `node_network_receive_bytes_total` | Network traffic health | Prometheus Node Exporter |

---

## 📈 SLO Reporting
SLO compliance is displayed in Grafana using thresholds:
- **Green:** within target  
- **Yellow:** approaching alert threshold  
- **Red:** below SLO target  

---

## ✅ Summary Table

| User Journey | SLI Type | SLO Target | Window |
|---------------|-----------|-------------|---------|
| View Main Page | Availability | 99 % success | 30 days |
| View Main Page | Latency | 95 % < 500 ms | 7 days |

---

