import os
import time
import subprocess
import csv
from string import Template
from datetime import datetime

TEMPLATE_PATH = "./nginx/reverse_proxy.template.conf"
OUTPUT_PATH = "./nginx/reverse_proxy.conf"
NGINX_CONTAINER = "reverse_proxy"
LOG_PATH = "./nginx/migration_log.csv"
DEFAULT_TOTAL_MINUTES = 10

def render_and_reload(weight1, weight2):
    os.environ["WEIGHT_SOL1"] = str(weight1)
    os.environ["WEIGHT_SOL2"] = str(weight2)

    with open(TEMPLATE_PATH) as f:
        content = Template(f.read()).substitute(os.environ)

    with open(OUTPUT_PATH, 'w') as f:
        f.write(content)

    subprocess.run(["docker", "exec", NGINX_CONTAINER, "nginx", "-s", "reload"])

def log_step(step, total_steps, weight1, weight2):
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), step, total_steps, weight1, weight2])

def progressive_migration(total_minutes=10, steps_per_minute=4):
    total_steps = int(total_minutes * steps_per_minute)
    max_weight = 100

    # Init log file
    with open(LOG_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Step", "TotalSteps", "Solution1Weight", "Solution2Weight"])

    for step in range(total_steps + 1):
        w2 = max(1, round((max_weight / total_steps) * step)) if step != 0 else 1
        w1 = max(1, max_weight - w2) if step != total_steps else 1
        render_and_reload(w1, w2)
        log_step(step, total_steps, w1, w2)
        print(f"Step {step:03} | Solution1: {w1}% | Solution2: {w2}%")
        time.sleep(60 / steps_per_minute)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", choices=["minute", "day", "month"], default="minute")
    parser.add_argument("--span", type=int, default=10)
    parser.add_argument("--steps", type=int, default=4)
    args = parser.parse_args()

    if args.unit == "minute":
        total_minutes = args.span
    elif args.unit == "day":
        total_minutes = args.span * 24 * 60
    elif args.unit == "month":
        total_minutes = args.span * 30 * 24 * 60
    else:
        total_minutes = DEFAULT_TOTAL_MINUTES

    total_steps = args.steps * args.span
    minutes_per_step = total_minutes / total_steps
    steps_per_minute = 1 / minutes_per_step

    progressive_migration(total_minutes=total_minutes, steps_per_minute=steps_per_minute)