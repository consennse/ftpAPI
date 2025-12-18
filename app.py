from flask import Flask, request, jsonify
from lxml import etree
from ftplib import FTP
import requests
from io import BytesIO

app = Flask(__name__)

def process_feed(source_url, ftp_host, ftp_username, ftp_password, ftp_target_path):
    try:
        # 1️⃣ Fetch XML
        response = requests.get(
            source_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/xml,text/xml"
            }
        )
        response.raise_for_status()
        xml_bytes = response.content

        # 2️⃣ Parse & clean XML (REMOVE teaser images)
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_bytes, parser)

        removed_count = 0
        for image in root.findall(".//image"):
            tags = [t.text.strip() for t in image.findall("tag") if t.text]
            if "Teaser (Portale)" in tags:
                parent = image.getparent()
                if parent is not None:
                    parent.remove(image)
                    removed_count += 1

        cleaned_xml = etree.tostring(
            root,
            xml_declaration=True,
            encoding="utf-8",
            pretty_print=True
        )

        # 3️⃣ Upload cleaned XML to FTP
        ftp = FTP(ftp_host, timeout=30)
        ftp.login(ftp_username, ftp_password)
        ftp.storbinary(
            f"STOR {ftp_target_path}",
            BytesIO(cleaned_xml)
        )
        ftp.quit()

        return {
            "status": "success",
            "removed_images": removed_count,
            "ftp_target_path": ftp_target_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.route("/run", methods=["POST"])
def run():
    data = request.json or {}
    required = [
        "source_url",
        "ftp_host",
        "ftp_username",
        "ftp_password",
        "ftp_target_path"
    ]

    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({
            "status": "error",
            "message": f"Missing fields: {', '.join(missing)}"
        }), 400

    result = process_feed(
        data["source_url"],
        data["ftp_host"],
        data["ftp_username"],
        data["ftp_password"],
        data["ftp_target_path"]
    )

    return jsonify(result), 200 if result["status"] == "success" else 500


@app.route("/", methods=["GET"])
def health():
    return {"message": "API running – teaser images removed"}
