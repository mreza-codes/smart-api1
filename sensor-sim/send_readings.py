import csv
import time
import urllib.error
import urllib.request
import json

API_URL = "http://localhost:30080/readings"
CSV_PATH = "TourPerret10col.csv"
DELAY_SECONDS = 2  # فاصله زمانی بین ارسال هر ردیف (شبیه‌سازی جریان بلادرنگ)


def send_reading(sensor_id: str, temperature: float) -> tuple[bool, str]:
    payload = json.dumps({
        "sensor_id": sensor_id,
        "temperature": temperature,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        return False, str(e)


def main():
    with open(CSV_PATH, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        for idx, row in enumerate(reader, start=1):
            if len(row) <= 4:
                continue

            try:
                temp_val = float(row[4])
                col0_val = row[0].strip()
            except ValueError:
                print(f"[{idx}] رد شد — مقدار نامعتبر: {row[4]}")
                continue

            sensor_id = f"perret-{col0_val}"
            ok, info = send_reading(sensor_id, temp_val)
            status = "OK" if ok else "ERR"
            print(f"[{idx}] {status} | sensor_id={sensor_id} | temp={temp_val} | {info}")

            time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    main()