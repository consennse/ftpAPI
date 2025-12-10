from flask import Flask, request, jsonify
import requests
from ftplib import FTP
from io import BytesIO

app = Flask(__name__)

def process_feed(source_url, ftp_host, ftp_username, ftp_password, ftp_target_path):
    try:
        # Fetch the source feed
        r = requests.get(source_url, timeout=30)
        if r.status_code != 200:
            return {"status": "error", "message": f"Failed to fetch source URL, status: {r.status_code}"}

        xml_content = r.text

        # Upload to FTP
        ftp = FTP(ftp_host, timeout=30)
        ftp.login(ftp_username, ftp_password)
        ftp.storbinary(f"STOR {ftp_target_path}", BytesIO(xml_content.encode("utf-8")))
        ftp.quit()

        return {"status": "success", "message": "Uploaded successfully"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Error fetching source URL: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"FTP error: {str(e)}"}

@app.route("/run", methods=["POST"])
def run():
    data = request.json or {}
    required_keys = ["source_url", "ftp_host", "ftp_username", "ftp_password", "ftp_target_path"]

    for key in required_keys:
        if key not in data:
            return jsonify({"status": "error", "message": f"Missing required field: {key}"}), 400

    result = process_feed(
        data["source_url"],
        data["ftp_host"],
        data["ftp_username"],
        data["ftp_password"],
        data["ftp_target_path"]
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
