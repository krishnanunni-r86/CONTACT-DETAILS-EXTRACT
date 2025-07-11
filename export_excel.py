import os
import glob
import json
from datetime import datetime
import pandas as pd

def write_entities_to_excel(output_dir, details_by_file):
    rows = []
    for file_name, details in details_by_file.items():
        names = [n['value'] for n in details.get('NAME', [])]
        addresses = [a['value'] for a in details.get('ADDRESS', [])]
        emails = [e['value'] for e in details.get('EMAIL', [])]
        phones = [p['value'] for p in details.get('PHONE', [])]
        max_len = max(len(names), len(addresses), len(emails), len(phones), 1)
        for i in range(max_len):
            row = {
                'file_name': file_name,
                'name': names[i] if i < len(names) else '',
                'address': addresses[i] if i < len(addresses) else '',
                'email': emails[i] if i < len(emails) else '',
                'phone': phones[i] if i < len(phones) else ''
            }
            rows.append(row)
    print(f"Preparing to write {len(rows)} rows to Excel...")
    if rows:
        df = pd.DataFrame(rows)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        excel_path = os.path.join(output_dir, f'entity_extraction_{timestamp}.xlsx')
        df.to_excel(excel_path, index=False)
        print(f"Excel file created: {excel_path}")

        # Move JSON files to 'JSON files' subfolder
        json_folder = os.path.join(output_dir, 'JSON files')
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
        json_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.json')]
        for json_file in json_files:
            src = os.path.join(output_dir, json_file)
            dst = os.path.join(json_folder, json_file)
            try:
                os.replace(src, dst)
                print(f"Moved {json_file} to {json_folder}")
            except Exception as e:
                print(f"Error moving {json_file}: {e}")
    else:
        print("No data to write to Excel.")

def export_excel():
    config_path = 'audio_scheduler_config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    output_dir = config.get('output_dir', 'output')
    print(f"Looking for JSON files in: {output_dir}")
    json_files = glob.glob(os.path.join(output_dir, '*.json'))
    print(f"Found JSON files: {json_files}")
    details_by_file = {}
    for json_file in json_files:
        print(f"Reading: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            details = data.get('details', {})
            if any(details.get(field) for field in ['NAME','ADDRESS','EMAIL','PHONE']):
                details_by_file[os.path.basename(json_file)] = details
    print(f"details_by_file: {details_by_file}")
    if details_by_file:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        write_entities_to_excel(output_dir, details_by_file)
        return True
    else:
        print("No details found to export to Excel.")
        return False
