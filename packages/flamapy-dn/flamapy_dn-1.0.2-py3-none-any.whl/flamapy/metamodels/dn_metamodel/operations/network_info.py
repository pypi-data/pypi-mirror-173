from flamapy.core.operations import Operation
from flamapy.metamodels.dn_metamodel.models import DependencyNetwork, Version


class NetworkInfo(Operation):

    def __init__(self) -> None:
        self.result: dict[str, int] = {
            'direct_dependencies': 0,
            'indirect_dependencies': 0,
            'direct_cves': 0,
            'indirect_cves': 0,
            'constraints': 0
        }

    def get_result(self) -> dict[str, int]:
        return self.result

    def execute(self, model: DependencyNetwork) -> None:
        for requirement_file in model.requirement_files:
            for package in requirement_file.packages:
                self.result['direct_dependencies'] += 1
                for version in package.versions:
                    for _ in version.cves:
                        self.result['direct_cves'] += 1
                    self.indirect(version)
        self.result['constraints'] = self.result['direct_dependencies'] + self.result['indirect_dependencies']

    def indirect(self, version: Version) -> None:
        for package in version.packages:
            self.result['indirect_dependencies'] += 1
            for version in package.versions:
                for _ in version.cves:
                    self.result['indirect_cves'] += 1
                self.indirect(version)
