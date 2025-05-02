import json


def parse_dependency_report(filepath):
    """Parses the dependency report file and returns a list of dependencies."""
    dependencies = []
    current_configuration = None
    try:
      with open(filepath, 'r') as f:
          for line in f:
              line = line.strip()
              if line.startswith("Configuration:"):
                  current_configuration = line.split(": ")[1]
              elif line.startswith("-"):
                  parts = line.split(":")
                  group = parts[0].split(" ")[-1].strip()
                  name = parts[1].strip()
                  version = parts[2].strip()
                  dependencies.append({
                      "configuration": current_configuration,
                      "group": group,
                      "name": name,
                      "version": version
                  })
    except FileNotFoundError:
      print(f"File Not Found at: {filepath}")
      return None
    return dependencies


def create_dependency_graph_json(dependencies):
    """Formats the dependencies into the JSON structure for GitHub dependency graph."""
    if dependencies is None:
        return None
    graph_dependencies = []
    for dep in dependencies:
        graph_dependencies.append({
            "packageName": f"{dep['group']}:{dep['name']}",
            "version": dep['version'],
            "relationship": "direct",  # For now, assume all are direct
            "scope": dep['configuration']
        })
    return json.dumps({
        "version": 0,
        "metadata": {},
        "dependencies": graph_dependencies
    }, indent=2)


def main():
    """Main function to parse the report and generate the JSON."""
    report_filepath = "build/dependency-report.txt"
    dependencies = parse_dependency_report(report_filepath)
    json_output = create_dependency_graph_json(dependencies)
    if json_output is not None:
      print(json_output)
      output_filepath = "build/dependency-graph.json"
      with open(output_filepath, 'w') as outfile:
          outfile.write(json_output)
      print(f"Dependency graph JSON generated: {output_filepath}")


if __name__ == "__main__":
    main()