#!/usr/bin/env python3

import requests
import sys
from semantic_version import Version, SimpleSpec

def find_min_parent_dep_version(parent_name, child_name, child_version_str):
    url = f"https://registry.npmjs.org/{parent_name}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"No se pudo obtener información de '{parent_name}' desde npm. "
              f"Código de estado: {resp.status_code}")
        return None

    data = resp.json()

    versions_data = data.get("versions", {})

    def try_parse_version(v):
        try:
            return Version(v)
        except ValueError:
            return None

    valid_versions = []
    for v_str in versions_data.keys():
        v_parsed = try_parse_version(v_str)
        if v_parsed is not None:
            valid_versions.append(v_parsed)

    valid_versions.sort()

    child_version = Version(child_version_str)

    for parent_ver in valid_versions:
        parent_ver_str = str(parent_ver)
        pkg_data = versions_data[parent_ver_str]

        deps = pkg_data.get("dependencies", {})

        if child_name in deps:
            range_str = deps[child_name]

            try:
                spec = SimpleSpec(range_str)
            except ValueError:
                continue

            if spec.match(child_version):
                return parent_ver_str

    return None

def main():
    if len(sys.argv) != 4:
        print("Uso: python find_min_dep_version.py <parent_name> <child_name> <child_version>")
        print("Ejemplo: python find_min_dep_version.py eslint cross-spawn 7.0.5")
        sys.exit(1)

    parent_name = sys.argv[1]
    child_name = sys.argv[2]
    child_version_str = sys.argv[3]

    result = find_min_parent_dep_version(parent_name, child_name, child_version_str)
    if result:
        print(f"La versión mínima de '{parent_name}' que declara "
              f"'{child_name}' compatible con '{child_version_str}' "
              f"es: {result}")
    else:
        print(f"No se encontró ninguna versión de '{parent_name}' que "
              f"declare '{child_name}' con un rango compatible con {child_version_str}.")

if __name__ == "__main__":
    main()
