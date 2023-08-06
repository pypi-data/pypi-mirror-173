# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import traceback
from pathlib import Path
from typing import List, Optional, Dict

from lean.components.api.api_client import APIClient
from lean.components.config.project_config_manager import ProjectConfigManager
from lean.components.util.logger import Logger
from lean.components.util.project_manager import ProjectManager
from lean.models.api import QCLanguage, QCProject
from lean.models.utils import LeanLibraryReference


class PushManager:
    """The PushManager class is responsible for synchronizing local projects to the cloud."""

    def __init__(self,
                 logger: Logger,
                 api_client: APIClient,
                 project_manager: ProjectManager,
                 project_config_manager: ProjectConfigManager) -> None:
        """Creates a new PushManager instance.

        :param logger: the logger to use when printing messages
        :param api_client: the APIClient instance to use when communicating with the cloud
        :param project_manager: the ProjectManager to use when looking for certain projects
        :param project_config_manager: the ProjectConfigManager instance to use
        """
        self._logger = logger
        self._api_client = api_client
        self._project_manager = project_manager
        self._project_config_manager = project_config_manager
        self._last_file = None
        self._cloud_projects = []

    def push_projects(self, projects_to_push: List[Path], organization_id: Optional[str] = None) -> None:
        """Pushes the given projects from the local drive to the cloud.

        It will also push every library referenced by each project and add or remove references.

        :param projects_to_push: a list of directories containing the local projects that need to be pushed
        :param organization_id: the id of the organization where the project will be pushed to
        """
        if len(projects_to_push) == 0:
            return

        projects_paths = projects_to_push + [library
                                             for project in projects_to_push
                                             for library in self._project_manager.get_project_libraries(project)]
        projects_paths = sorted(projects_paths)

        pushed_projects = {}
        for index, path in enumerate(projects_paths, start=1):
            relative_path = path.relative_to(Path.cwd())
            try:
                self._logger.info(f"[{index}/{len(projects_paths)}] Pushing '{relative_path}'")
                pushed_projects[path] = self._push_project(path, organization_id)
            except Exception as ex:
                self._logger.debug(traceback.format_exc().strip())
                if self._last_file is not None:
                    self._logger.warn(f"Cannot push '{relative_path}' (failed on {self._last_file}): {ex}")
                else:
                    self._logger.warn(f"Cannot push '{relative_path}': {ex}")

        self._update_cloud_library_references(pushed_projects)

    def _update_cloud_library_references(self, projects: Dict[Path, QCProject]) -> None:
        for path, project in projects.items():
            local_libraries_cloud_ids = self._get_local_libraries_cloud_ids(path)
            self._add_new_libraries(project, local_libraries_cloud_ids)
            self._remove_outdated_libraries(project, local_libraries_cloud_ids)

    def _get_local_libraries_cloud_ids(self, project_dir: Path) -> List[int]:
        project_config = self._project_config_manager.get_project_config(project_dir)

        libraries_in_config = project_config.get("libraries", [])
        library_paths = [LeanLibraryReference(**library).path.expanduser().resolve() for library in libraries_in_config]

        local_libraries_cloud_ids = [int(self._project_config_manager.get_project_config(path).get("cloud-id", None))
                                     for path in library_paths]

        return local_libraries_cloud_ids

    def _get_library_name(self, library_cloud_id: int) -> str:
        return self._get_cloud_project(library_cloud_id).name

    def _add_new_libraries(self, project: QCProject, local_libraries_cloud_ids: List[int]) -> None:
        libraries_to_add = [library_id for library_id in local_libraries_cloud_ids if
                            library_id not in project.libraries]

        if len(libraries_to_add) > 0:
            self._logger.info(f"Adding libraries to project {project.name} in the cloud")

        for i, library_cloud_id in enumerate(libraries_to_add, start=1):
            library_name = self._get_library_name(library_cloud_id)
            self._logger.info(f"[{i}/{len(libraries_to_add)}] "
                              f"Adding library {library_name} to project {project.name} in the cloud")
            self._api_client.projects.add_library(project.projectId, library_cloud_id)

    def _remove_outdated_libraries(self, project: QCProject, local_libraries_cloud_ids: List[int]) -> None:
        libraries_to_remove = [library_id for library_id in project.libraries
                               if library_id not in local_libraries_cloud_ids]

        if len(libraries_to_remove) > 0:
            self._logger.info(f"Removing libraries from project {project.name} in the cloud")

        for i, library_cloud_id in enumerate(libraries_to_remove, start=1):
            library_name = self._get_library_name(library_cloud_id)
            self._logger.info(f"[{i}/{len(libraries_to_remove)}] "
                              f"Removing library {library_name} from project {project.name} in the cloud")
            self._api_client.projects.delete_library(project.projectId, library_cloud_id)

    def _push_project(self, project: Path, organization_id: Optional[str]) -> QCProject:
        """Pushes a single local project to the cloud.

        Raises an error with a descriptive message if the project cannot be pushed.

        :param project: the local project to push
        :param organization_id: the id of the organization to push the project to
        """
        project_name = project.relative_to(Path.cwd()).as_posix()

        project_config = self._project_config_manager.get_project_config(project)
        cloud_id = project_config.get("cloud-id")

        # Find the cloud project to push the files to
        if cloud_id is not None:
            # Project has cloud id which matches cloud project, update cloud project
            cloud_project = self._get_cloud_project(cloud_id)
        else:
            # Project has invalid cloud id or no cloud id at all, create new cloud project
            cloud_project = self._api_client.projects.create(project_name,
                                                             QCLanguage[project_config.get("algorithm-language")],
                                                             organization_id)
            self._cloud_projects.append(cloud_project)
            project_config.set("cloud-id", cloud_project.projectId)
            project_config.set("organization-id", cloud_project.organizationId)

            organization_message_part = f" in organization '{organization_id}'" if organization_id is not None else ""
            self._logger.info(f"Successfully created cloud project '{project_name}'{organization_message_part}")

        # Push local files to cloud
        self._push_files(project, cloud_project)

        # Finalize pushing by updating locally modified metadata
        self._push_metadata(project, cloud_project)

        return cloud_project

    def _push_files(self, project: Path, cloud_project: QCProject) -> None:
        """Pushes the files of a local project to the cloud.

        :param project: the local project to push the files of
        :param cloud_project: the cloud project to push the files to
        """
        cloud_files = self._api_client.files.get_all(cloud_project.projectId)
        local_files = self._project_manager.get_source_files(project)
        local_file_names = [local_file.relative_to(project).as_posix() for local_file in local_files]

        for local_file, file_name in zip(local_files, local_file_names):
            self._last_file = local_file

            if "bin/" in file_name or "obj/" in file_name or ".ipynb_checkpoints/" in file_name:
                continue

            file_content = local_file.read_text(encoding="utf-8")
            cloud_file = next(iter([f for f in cloud_files if f.name == file_name]), None)

            if cloud_file is None:
                new_file = self._api_client.files.create(cloud_project.projectId, file_name, file_content)
                self._project_manager.update_last_modified_time(local_file, new_file.modified)
                self._logger.info(f"Successfully created cloud file '{cloud_project.name}/{file_name}'")
            elif cloud_file.content.strip() != file_content.strip():
                new_file = self._api_client.files.update(cloud_project.projectId, file_name, file_content)
                self._project_manager.update_last_modified_time(local_file, new_file.modified)
                self._logger.info(f"Successfully updated cloud file '{cloud_project.name}/{file_name}'")

        # Delete locally removed files in cloud
        files_to_remove = [cloud_file for cloud_file in cloud_files
                           if (not cloud_file.isLibrary and
                               not any(local_file_name == cloud_file.name for local_file_name in local_file_names))]
        for file in files_to_remove:
            self._last_file = Path(file.name)
            self._api_client.files.delete(cloud_project.projectId, file.name)
            self._logger.info(f"Successfully removed cloud file '{cloud_project.name}/{file.name}'")

        self._last_file = None

    def _push_metadata(self, project: Path, cloud_project: QCProject) -> None:
        """Pushes local project description and parameters to the cloud.

        Does nothing if the cloud is already up-to-date.

        :param project: the local project to push the parameters of
        :param cloud_project: the cloud project to push the parameters to
        """
        project_config = self._project_config_manager.get_project_config(project)

        local_description = project_config.get("description", "")
        cloud_description = cloud_project.description

        local_parameters = project_config.get("parameters", {})
        cloud_parameters = {parameter.key: parameter.value for parameter in cloud_project.parameters}

        # Use latest (-1) by default
        local_lean_version = int(project_config.get("lean-engine", "-1"))
        cloud_lean_version = cloud_project.leanVersionId

        local_lean_venv = project_config.get("python-venv", None)
        cloud_lean_venv = cloud_project.leanEnvironment

        update_args = {}

        if local_description != cloud_description:
            update_args["description"] = local_description

        if local_parameters != cloud_parameters:
            update_args["parameters"] = local_parameters

        if (local_lean_version != cloud_lean_version and
           (local_lean_version != -1 or not cloud_project.leanPinnedToMaster)):
            update_args["lean_engine"] = local_lean_version

        # Initially, python-venv is not defined in the config and the default one will be used.
        # After it is changed, in order to use the default one again, it must not be removed from the config,
        # but it should be set to the default env id explicitly instead.
        if local_lean_venv is not None and local_lean_venv != cloud_lean_venv:
            update_args["python_venv"] = local_lean_venv

        if update_args != {}:
            self._api_client.projects.update(cloud_project.projectId, **update_args)
            self._logger.info(f"Successfully updated {' and '.join(update_args.keys())} for '{cloud_project.name}'")

    def _get_cloud_project(self, project_id: int) -> QCProject:
        project = next(iter(p for p in self._cloud_projects if p.projectId == project_id), None)
        if project is None:
            project = self._api_client.projects.get(project_id)
            self._cloud_projects.append(project)

        return project
