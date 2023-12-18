import spacy
import os
import json

models = ["model-1.1", "model-1.2", "model-2.1", "model-3.1", "model-3.2", "model-4.1", "model-4.2", "model-4.3"]


with open("correct_results.json", "r") as f:
    expected_results = json.load(f)
with open("test_results.txt", "w") as f_result:

    for model in models:
        false_positives = 0
        false_negatives = 0
        total_entities_expected = 0
        total_entities_predicted = 0

        model_path = os.path.join(os.getcwd(), model)
        nlp = spacy.load(model_path)

        for data in expected_results:
            text = data["text"]
            expected_entities = [(entity["text"], entity["labels"][0]) for entity in data["label"]]
            f_result.write(f"Model: {model}\n")

            doc = nlp(text)
            predicted_entities = [(ent.text, ent.label_) for ent in doc.ents]
            total_entities_expected += len(expected_entities)
            total_entities_predicted += len(predicted_entities)

            for entity in predicted_entities:
                f_result.write(f"{entity}\n")
                if entity not in expected_entities:
                    false_positives += 1

            for entity in expected_entities:
                if entity not in predicted_entities:
                    false_negatives += 1

        percentage_false_positives = (false_positives / total_entities_predicted) * 100
        percentage_false_negatives = (false_negatives / total_entities_expected) * 100

        print(f"Model: {model}")
        print(f"False Positives: {percentage_false_positives:.2f}%")
        print(f"False Negatives: {percentage_false_negatives:.2f}%")
        print(f"Total Entities Expected: {total_entities_expected}")
        print(f"Total Entities Predicted: {total_entities_predicted}")
        print("-----------")