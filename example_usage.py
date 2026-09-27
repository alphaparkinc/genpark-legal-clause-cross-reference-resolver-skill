import sys, json
from client import LegalClauseCrossReferenceResolver

def main():
    print("Testing LegalClauseCrossReferenceResolver...")
    resolver = LegalClauseCrossReferenceResolver()
    res = resolver.run_benchmark_legal_resolution()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["defined_terms_count"] >= 1
    assert res["has_circular_reference"] is True, "Should detect circular reference between Section 2.0 and 3.0"
    print("All Legal Clause Cross Reference Resolver tests passed successfully!")

if __name__ == "__main__":
    main()
