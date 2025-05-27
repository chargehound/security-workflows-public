import json
import traceback
from datetime import datetime

def parse_dependency_report(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        manifests = {}
        current_manifest = None

        for line in lines:
            line = line.strip()

            # Identify new manifest sections based on headers
            if line.startswith('Manifest:'):
                manifest_name = line.replace('Manifest:', '').strip()
                current_manifest = {
                    "name": manifest_name,
                    "file": {
                        "source_location": "build/dependency-graph.json"
                    },
                    "resolved": {}
                }
                manifests[manifest_name] = current_manifest

            # Parse dependency lines in format group:artifact:version
            elif current_manifest and line.startswith("- "):
                dependency = line[2:]  # Remove leading "- "
                try:
                    group, artifact, version = dependency.split(":")
                    key = f"- {group}:{artifact}:{version}"
                    package_url = f"pkg:maven/{group}/{artifact}@{version}"
                    current_manifest["resolved"][key] = {
                        "package_url": package_url,
                        "relationship": "direct",
                        "scope": "development"
                    }
                except ValueError:
                    # Handle parsing errors for dependency lines
                    print(f"Error parsing dependency line: {line}")

        # Construct the final JSON structure
        dependency_snapshot = {
            "version": 0,
            "sha": "991a3490e97761f1c6c89e9304e90a57a2f36ea2",  # Replace with actual commit SHA
            "ref": "refs/heads/main",  # Replace with actual ref
            "job": {
                "id": "fumm",
                "correlator": "example-job-id",  # Replace with actual job correlator
                "html_url": "http://example.com/job"  # Replace with actual job URL
            },
            "detector": {
                "name": "custom-detector",
                "version": "1.0.0",
                "url": "https://github.com/your-organization/gradle-dependency-extractor"
            },
            "scanned": datetime.utcnow().isoformat() + "Z",  # Current UTC timestamp
            "manifests": manifests
        }

        return dependency_snapshot

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

# Write the generated JSON output to a file
def generate_dependency_snapshot(input_file, output_file):
    snapshot = parse_dependency_report(input_file)
    if snapshot:
        with open(output_file, 'w') as file:
            json.dump(snapshot, file, indent=2)
        print(f"Dependency snapshot successfully generated in '{output_file}'")

# Example usage
input_file = 'build/dependency-report.txt'  # Input file path
output_file = 'build/dependency-graph.json'  # Output file path
generate_dependency_snapshot(input_file, output_file)
