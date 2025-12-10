from flask import Flask, request, jsonify
import requests
from ftplib import FTP

app = Flask(__name__)

def process_feed(source_url, ftp_host, ftp_username, ftp_password, ftp_target_path):
    r = requests.get(source_url)
    if r.status_code != 200:
        return {"status": "error", "message": "Failed to fetch source URL"}

    xml_content = r.text

    ftp = FTP(ftp_host)
    ftp.login(ftp_username, ftp_password)

    ftp.storbinary(f"STOR {ftp_target_path}", bytes(xml_content, "utf-8"))
    ftp.quit()

    return {"status": "success", "message": "Uploaded successfully"}

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    return jsonify(process_feed(
        data["source_url"],
        data["ftp_host"],
        data["ftp_username"],
        data["ftp_password"],
        data["ftp_target_path"]
    ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
