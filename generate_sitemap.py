import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

BASE_URL = "https://chuyentin-tailieu.a3sachhonaba.com/"
JSON_FILE = "assets/documents/documents.json"
OUTPUT_FILE = "sitemap.xml"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []

def create_sitemap():
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = BASE_URL + "index.html"
    ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(url, "changefreq").text = "weekly"
    ET.SubElement(url, "priority").text = "1.0"
    
    documents = load_json_data(JSON_FILE)
    
    for doc in documents:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{BASE_URL}assets/documents/files/{doc['fileName']}.html"
        ET.SubElement(url, "lastmod").text = doc.get('uploadDate', datetime.now().strftime("%Y-%m-%d"))
        ET.SubElement(url, "changefreq").text = "monthly"
        ET.SubElement(url, "priority").text = "0.8"
    
    rough_string = ET.tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    create_sitemap()
    print(f"Sitemap generated successfully: {OUTPUT_FILE}")