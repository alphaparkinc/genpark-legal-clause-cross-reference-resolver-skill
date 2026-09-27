import sys, json
from client import LegalClauseCrossReferenceResolver

def main():
    resolver = LegalClauseCrossReferenceResolver()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(resolver.run_benchmark_legal_resolution(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "extract_defined_terms", "description": "Extract defined terms and statutory definitions."},
                        {"name": "map_clause_dependencies", "description": "Map internal section cross references."},
                        {"name": "detect_circular_references", "description": "Detect drafting circularities."},
                        {"name": "run_benchmark_legal_resolution", "description": "Run contract legal dependency benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "extract_defined_terms":
                    out = resolver.extract_defined_terms(args.get("contract_text", ""))
                elif tname == "map_clause_dependencies":
                    out = resolver.map_clause_dependencies(args.get("clauses_dict", {}))
                elif tname == "detect_circular_references":
                    out = resolver.detect_circular_references(args.get("dependency_graph", {}))
                elif tname == "run_benchmark_legal_resolution":
                    out = resolver.run_benchmark_legal_resolution()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
