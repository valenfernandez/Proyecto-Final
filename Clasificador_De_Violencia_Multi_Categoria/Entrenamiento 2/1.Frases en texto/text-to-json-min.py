import json

def process_phrases(file_path, output_path, sentiment):
    processed_phrases = []
    with open(file_path, 'r', encoding = 'utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):
            phrase = line.strip()

            processed_phrase = {
                "text": phrase,
                "id": i + 1,
                "sentiment": sentiment,
                "annotator": 1,
                "annotation_id": i + 1,
                "created_at": "2023-07-13T00:00:00.000000Z",
                "updated_at": "2023-07-13T00:00:00.000000Z",
                "lead_time": 8.342
            }

            processed_phrases.append(processed_phrase)

        with open(output_path, 'w', encoding = 'utf-8') as file:
            json.dump(processed_phrases, file, indent=4, ensure_ascii=False)

processed_data = process_phrases('simbolica.txt', 'frases_simbolica.json', 'Simbólica')
processed_data = process_phrases('economica.txt', 'frases_economica.json', 'Económica')
processed_data = process_phrases('psicologica.txt', 'frases_psicologica.json', 'Psicológica')
processed_data = process_phrases('sexual.txt', 'frases_sexual.json', 'Sexual')
processed_data = process_phrases('fisica.txt', 'frases_fisica.json', 'Física')



