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
        try:
            ftp = FTP(ftp_host, timeout=30)
            ftp.login(ftp_username, ftp_password)
            ftp.storbinary(f"STOR {ftp_target_path}", BytesIO(xml_content.encode("utf-8")))
            ftp.quit()
        except Exception as ftp_error:
            return {"status": "error", "message": f"FTP upload failed: {str(ftp_error)}"}

        return {"status": "success", "message": "Uploaded successfully"}

    except requests.exceptions.RequestException as req_error:
        return {"status": "error", "message": f"Error fetching source URL: {str(req_error)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

@app.route("/run", methods=["POST"])
def run():
    data = request.json or {}
    required_keys = ["source_url", "ftp_host", "ftp_username", "ftp_password", "ftp_target_path"]

    # Validate required fields
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({"status": "error", "message": f"Missing required fields: {', '.join(missing_keys)}"}), 400

    result = process_feed(
        data["source_url"],
        data["ftp_host"],
        data["ftp_username"],
        data["ftp_password"],
        data["ftp_target_path"]
    )

    # Return JSON response
    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
