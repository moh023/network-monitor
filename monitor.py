import subprocess
import re
import csv
import datetime
import os
import schedule
import time
import speedtest

LOG_FILE = 'network_log.csv'

def ping(host='8.8.8.8', count=4):
    result = subprocess.run(
        ['ping', '-c', str(count), host],
        capture_output=True,
        text=True
    )
    match = re.search(r'avg.*?(\d+\.\d+)', result.stdout)
    latency = float(match.group(1)) if match else None
    loss_match = re.search(r'(\d+)% packet loss', result.stdout)
    loss = int(loss_match.group(1)) if loss_match else 100
    return latency, loss

def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1000000
        upload = st.upload() / 1000000
        return round(download, 2), round(upload, 2)
    except Exception as e:
        print('Speed test failed: ' + str(e))
        return None, None

def save_to_csv(host, latency, loss, download=None, upload=None):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                'timestamp',
                'host',
                'latency_ms',
                'packet_loss_pct',
                'download_mbps',
                'upload_mbps'
            ])
        writer.writerow([
            datetime.datetime.now(),
            host,
            latency,
            loss,
            download,
            upload
        ])

def take_measurement():
    host = '8.8.8.8'
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + '] Taking measurement...')
    latency, loss = ping(host)
    print('  Ping done: ' + str(latency) + 'ms | Loss: ' + str(loss) + '%')
    print('  Running speed test (20-30 seconds)...')
    download, upload = get_speed()
    save_to_csv(host, latency, loss, download, upload)
    print('  Done! Download speed: ' + str(download) + 'Mbps | Upload speed: ' + str(upload) + 'Mbps')
    print('  Saved to ' + LOG_FILE)
    print('---')

if __name__ == '__main__':
    print('Network monitor started. Press Ctrl+C to stop.')
    print('---')
    take_measurement()
    schedule.every(45).seconds.do(take_measurement)
    while True:
        schedule.run_pending()
        time.sleep(1)
