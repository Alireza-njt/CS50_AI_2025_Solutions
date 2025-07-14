# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Monday, July 14, 2025 6:02 PM +0330


import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    def month_mapping_to_int(month):
        month = month.capitalize()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i in range(len(months)):
            if months[i] == month:
                return i

    def bool_mapping_to_int(b):
        if b == 'TRUE':
            return 1
        return 0

    def visitorType_mapping_to_int(v_type):
        if v_type == 'Returning_Visitor':
            return 1
        return 0

    int_items = ['Administrative', 'Informational', 'ProductRelated',
                 'OperatingSystems', 'Browser', 'Region', 'TrafficType']
    float_items = ['Administrative_Duration', 'Informational_Duration',
                   'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
    labels = []
    evidence = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i != 0:
                labels.append(bool_mapping_to_int(row[len(row)-1]))
                evidence_for_row = []
                for j in range(len(row)-1):
                    if header[j] in int_items:
                        evidence_for_row.append(int(row[j]))
                    elif header[j] in float_items:
                        evidence_for_row.append(float(row[j]))
                    elif header[j] == 'Month':
                        evidence_for_row.append(month_mapping_to_int(row[j]))
                    elif header[j] == 'VisitorType':
                        evidence_for_row.append(visitorType_mapping_to_int(row[j]))
                    elif header[j] == 'Weekend' :
                        evidence_for_row.append(bool_mapping_to_int(row[j]))

                evidence.append(evidence_for_row)

            else:
                header = row.copy()

            i += 1

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    fknn_model = KNeighborsClassifier(n_neighbors=1)  # fitted k-nearest neighbor model (k=1)
    fknn_model.fit(evidence, labels)
    return fknn_model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity, specificity = 0, 0
    actual_positive_labels_numbers = 0
    actual_negative_labels_numbers = 0
    for i in range(len(predictions)):
        if labels[i] == predictions[i] == 1:
            sensitivity += 1
        elif labels[i] == predictions[i] == 0:
            specificity += 1
    for i in range(len(labels)):
        if labels[i] == 1:
            actual_positive_labels_numbers += 1
        elif labels[i] == 0:
            actual_negative_labels_numbers += 1
    sensitivity /= actual_positive_labels_numbers
    specificity /= actual_negative_labels_numbers
    return sensitivity, specificity


if __name__ == "__main__":
    main()
