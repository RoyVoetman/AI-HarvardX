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
        # All people that are known to have the trait + any combination of people with trait=None
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
    probability = 1.0

    for person in people:
        personGenes = get_genes(person, one_gene, two_genes)

        # If mother and father unknown use unconditional probability
        if people[person]['mother'] is None and people[person]['father'] is None:
            probability = probability * PROBS['gene'][personGenes]
        else:
            motherGenes = get_genes(people[person]['mother'], one_gene, two_genes)
            fatherGenes = get_genes(people[person]['father'], one_gene, two_genes)

            motherPassing = get_passing_prop(motherGenes)
            fatherPassing = get_passing_prop(fatherGenes)

            # Probabilty that father and mother pass the right amount of genes
            if (personGenes == 0):
                probability = probability * And(
                    Not(motherPassing), Not(fatherPassing)
                )
            elif (personGenes == 1):
                probability = probability * Or(
                    And(motherPassing, Not(fatherPassing)), 
                    And(fatherPassing, Not(motherPassing))
                )
            elif (personGenes == 2):
                probability = probability * And(motherPassing, fatherPassing)
        
        # Probabilty having given trait
        probability = probability * (PROBS['trait'][personGenes][person in have_trait])

    return probability

def get_genes(person, one_gene, two_genes):
    if person in one_gene:
        return  1
    elif person in two_genes:
        return 2

    return 0

def get_passing_prop(genes):
    if genes == 0:
        return PROBS['mutation']
    if genes == 1:
        # Mutation does not have any effect on 
        # an even distribution (0.5 + 0.1 - 0.1 = 0.5)
        return 0.5
    if genes == 2:
        return 1 - PROBS['mutation']

    return None

def Not(statement):
    return 1 - statement

def Or(statement1, statement2):
    return statement1 + statement2

def And(statement1, statement2):
    return statement1 * statement2

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        personGenes = get_genes(person, one_gene, two_genes)

        probabilities[person]["gene"][personGenes]           = probabilities[person]["gene"][personGenes] + p
        probabilities[person]["trait"][person in have_trait] = probabilities[person]["trait"][person in have_trait] + p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for k1, v1 in probabilities.items():
        for k2, v2 in v1.items():
            total = sum(v2.values())
            
            for i in probabilities[k1][k2]:
                probabilities[k1][k2][i] = probabilities[k1][k2][i] / total


if __name__ == "__main__":
    main()
