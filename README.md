# 🌀 Progressive Load Migration with Docker + NGINX

This project demonstrates a **progressive migration strategy** for routing traffic between two backend services using **Docker** and **NGINX** as a reverse proxy.

📌 The system simulates a real-world scenario where one backend (Solution 1) is being gradually replaced by another (Solution 2) over a custom time span, using controlled traffic redirection.

---

## 🔧 Key Features

- **Two services** (`solution1`, `solution2`) behind a reverse proxy
- **NGINX-based load balancing** using dynamic weights
- **Automated traffic shift** via a Python controller (`adaptive_migrate.py`)
- **Fully Dockerized setup** with one-line startup
- **CSV logging** of the migration process
- Supports custom spans:
  - `--unit minute/day/month`
  - `--span <int>` for total units
  - `--steps <int>` per unit

---

## 🛠 Tech Stack

- 🐳 Docker & Docker Compose
- 🔁 NGINX (Reverse Proxy)
- 🐍 Python 3 (Controller)
- 📄 CSV logging
- 🧪 Optional: Matplotlib for plotting migration log (future)

---

## 🚀 Usage

```bash
./launch.sh
```

Starts the full environment and launches a 10-minute migration from `solution1` to `solution2`, with 4 steps per minute.

---

## 🧪 Example

Initial state:
```
solution1: 100%
solution2:   0%
```

Final state (after N steps):
```
solution1:   0%
solution2: 100%
```

---

## 📊 Log Example (`migration_log.csv`)

| Timestamp           | Step | TotalSteps | Solution1Weight | Solution2Weight |
|---------------------|------|-------------|------------------|------------------|
| 2025-06-24 13:00:00 | 0    | 40          | 100              | 0                |
| 2025-06-24 13:02:00 | 1    | 40          | 97               | 3                |
| ...                 | ...  | ...         | ...              | ...              |

---

## 📂 Project Structure

```
.
├── nginx/
│   ├── solution1.conf
│   ├── solution2.conf
│   ├── reverse_proxy.template.conf
│   ├── reverse_proxy.conf
│   └── migration_log.csv
├── adaptive_migrate.py
├── docker-compose.yml
└── launch.sh
```

---

## 🧠 Future Work

- [ ] Replace NGINX with HAProxy or Envoy for smarter control
- [ ] Real-time plotting during migration
- [ ] A/B testing and canary deployment patterns