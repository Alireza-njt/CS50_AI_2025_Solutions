# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Tuesday, July 8, 2025 5:40 PM +0330


import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    result = 1.000
    zero_gene = set()
    for person in people:
        if person not in one_gene and person not in two_genes:
            zero_gene.add(person)
    for person in people:
        if (people[person]['mother'] is None and people[person]['father'] is None):
            gene_number = -2025
            if person in zero_gene:
                result *= PROBS['gene'][0]
                gene_number = 0
            elif person in one_gene:
                result *= PROBS['gene'][1]
                gene_number = 1
            elif person in two_genes:
                result *= PROBS['gene'][2]
                gene_number = 2
            if person in have_trait:
                result *= PROBS['trait'][gene_number][True]
            else:
                result *= PROBS['trait'][gene_number][False]

        elif (people[person]['mother'] is not None and people[person]['father'] is not None):
            gene_number = -2025
            if person in zero_gene:
                gene_number = 0
            elif person in one_gene:
                gene_number = 1
            elif person in two_genes:
                gene_number = 2

            if person in have_trait:
                result *= PROBS['trait'][gene_number][True]
            else:
                result *= PROBS['trait'][gene_number][False]

            mother_gene_number = 0
            father_gene_number = 0

            if people[person]['mother'] in one_gene:
                mother_gene_number = 1
            elif people[person]['mother'] in two_genes:
                mother_gene_number = 2
            if people[person]['father'] in one_gene:
                father_gene_number = 1
            elif people[person]['father'] in two_genes:
                father_gene_number = 2
            mother_p = -2025  # The possibility of transmitting genes from mother to child
            father_p = -2025  # The possibility of transmitting genes from father to child
            transfer_p = -2025  # The probability of successfully transmitting genes from parents
            if mother_gene_number == 2:
                mother_p = 1 - PROBS["mutation"]
            elif mother_gene_number == 1:
                mother_p = 0.5
            else:
                mother_p = PROBS["mutation"]
            if father_gene_number == 2:
                father_p = 1 - PROBS["mutation"]
            elif father_gene_number == 1:
                father_p = 0.5
            else:
                father_p = PROBS["mutation"]

            if person in zero_gene:
                transfer_p = (1-mother_p) * (1-father_p)
            elif person in one_gene:
                transfer_p = mother_p * (1-father_p) + father_p * (1-mother_p)
            elif person in two_genes:
                transfer_p = father_p * mother_p

            result *= transfer_p

    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        gene_dict = probabilities[person]['gene']
        trait_dict = probabilities[person]['trait']
        sum_for_gene_dict = 0.000
        sum_for_trait_dict = 0.000
        sum_for_gene_dict += gene_dict[2]
        sum_for_gene_dict += gene_dict[1]
        sum_for_gene_dict += gene_dict[0]
        sum_for_trait_dict += trait_dict[True]
        sum_for_trait_dict += trait_dict[False]
        alpha_for_gene_dict = 1 / sum_for_gene_dict
        alpha_for_trait_dict = 1 / sum_for_trait_dict
        probabilities[person]['gene'][2] *= alpha_for_gene_dict
        probabilities[person]['gene'][1] *= alpha_for_gene_dict
        probabilities[person]['gene'][0] *= alpha_for_gene_dict
        probabilities[person]['trait'][True] *= alpha_for_trait_dict
        probabilities[person]['trait'][False] *= alpha_for_trait_dict


if __name__ == "__main__":
    main()
