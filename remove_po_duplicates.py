import polib

po_files = [
    r'locale/uk/LC_MESSAGES/django.po',
    r'locale/en/LC_MESSAGES/django.po'
]

for po_file_path in po_files:
    po = polib.pofile(po_file_path)

    seen_msgids = set()
    entries_to_remove = []

    for entry in po:
        if entry.msgid in seen_msgids:
            entries_to_remove.append(entry)
        else:
            seen_msgids.add(entry.msgid)

    for entry in entries_to_remove:
        po.remove(entry)

    po.save()
    print(f"{po_file_path}: deleted {len(entries_to_remove)} duplicates.")

