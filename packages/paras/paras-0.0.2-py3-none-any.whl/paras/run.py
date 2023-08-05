import os
from joblib import load
from typing import Tuple, List

import paras.data
from paras.domain_extraction.extract_residues import extract_stach_code
from paras.feature_extraction.get_sequence_features import get_sequence_features


CLASSIFIER_FILE = os.path.join(os.path.dirname(paras.data.__file__), 'paras.classifier')


def run_paras(sequence: str, threshold: float=0.5) -> List[Tuple[float, str]]:
    classifier = load(CLASSIFIER_FILE)
    amino_acid_classes = classifier.classes_

    stach, active_site = extract_stach_code(sequence)
    features = [get_sequence_features(active_site)]
    probabilities = classifier.predict_proba(features)[0]
    probs_and_aas = get_best_predictions(amino_acid_classes, probabilities, threshold)

    return probs_and_aas


def get_best_predictions(amino_acid_classes, probabilities, threshold):
    probs_and_aa = []
    for i, probability in enumerate(probabilities):
        if probability >= threshold:
            probs_and_aa.append((probability, amino_acid_classes[i]))

    probs_and_aa.sort(reverse=True)

    return probs_and_aa


