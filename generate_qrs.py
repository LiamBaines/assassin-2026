import csv
import qrcode
from pathlib import Path

INPUT_CSV = "target/player_card_data.csv"
OUTPUT_DIR = "target/qr_codes"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

with open(INPUT_CSV, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        player = row["player"].strip()
        url = "https://liambaines.github.io/assassin-2026/?data=" + row["card_data"].strip()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        output_path = Path(OUTPUT_DIR) / f"{player}.png"
        img.save(output_path)

        print(f"Generated QR for {player}: {output_path}")
