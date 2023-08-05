from famapy.core.transformations import Transformation

from famapy.metamodels.dn_metamodel.models import (DependencyNetwork, Package,
                                 RequirementFile, Version)


class SerializeNetwork(Transformation):

    '''
    SerializeNetwork(
        source_model: dict
    )
    '''

    source_model: dict
    destination_model: DependencyNetwork | None = None

    def __init__(self, **kwargs) -> None:
        valid_keys = [
            'source_model',
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

    def transform(self) -> None:
        requirement_files = [self.transform_requirement_file(requirement_file) for requirement_file in self.source_model['requirement_files']]
        self.source_model['requirement_files'] = requirement_files
        self.destination_model = DependencyNetwork(**self.source_model)

    def transform_requirement_file(self, requirement_file) ->RequirementFile:
        packages = [self.transform_package(package) for package in requirement_file['packages']]
        requirement_file['packages'] = packages
        return RequirementFile(**requirement_file)

    def transform_package(self, package) -> Package:
        versions = [self.transform_version(version) for version in package['versions']]
        package['versions'] = versions
        return Package(**package)

    def transform_version(self, version) -> Version:
        packages = [self.transform_package(package) for package in version['packages']]
        version['packages'] = packages
        return Version(**version)