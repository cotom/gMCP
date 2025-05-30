from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    techniques = mitre_attack_data.get_techniques_by_tactic(
        "defense-evasion", "enterprise-attack", remove_revoked_deprecated=True
    )

    print(f"There are {len(techniques)} techniques related to the Defense Evasion tactic.")
    for technique in techniques:
        print(f"Technique ID: {technique['external_references'][0]['external_id']}")
        print(f"Name: {technique['name']}")
        print(f"Description: {technique['description']}\n")


if __name__ == "__main__":
    main()