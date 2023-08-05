from typing import List
from urllib.parse import urlparse

from .base import Resource, ResourceManager


class Sandbox(Resource):
    def __init__(self, manager: ResourceManager, sandbox_id: str, name: str, blueprint_name: str):
        super(Sandbox, self).__init__(manager)

        self.sandbox_id = sandbox_id
        self.name = name
        self.blueprint_name = blueprint_name

    @classmethod
    def json_deserialize(cls, manager: ResourceManager, json_obj: dict):
        try:
            sandbox_id = json_obj.get("id", None) or json_obj["details"]["id"]
            sb_details = json_obj["details"]["definition"]
            sb = Sandbox(
                manager,
                sandbox_id,
                sb_details["metadata"]["name"],
                sb_details["metadata"]["blueprint_name"],
            )
            sb.sandbox_status = json_obj["details"]["computed_status"]
        except KeyError as e:
            raise NotImplementedError(f"unable to create object. Missing keys in Json. Details: {e}")

        # for attr in ["description", "errors", "sandbox_status", "launching_progress"]:
        #     sb.__dict__[attr] = json_obj.get(attr, "")
        # TODO(ddovbii): set all needed attributes
        # sb.errors = json_obj.get("errors", [])
        # sb.description = json_obj.get("description", "")
        # sb.status = json_obj.get("sandbox_status", "")
        # sb.launching_progress = json_obj.get("launching_progress", {})
        # sb.__dict__ = json_obj.copy()
        return sb

    def json_serialize(self) -> dict:
        return {
            "id": self.sandbox_id,
            "name": self.name,
            "blueprint_name": self.blueprint_name,
        }

    def table_serialize(self) -> dict:
        return self.json_serialize()


class SandboxesManager(ResourceManager):
    resource_obj = Sandbox
    SANDBOXES_PATH = "environments"
    SANDBOXES_LINK = "sandboxes"

    # SPECIFIC_SANDBOX_PATH = "sandboxes"

    def get_sandbox_url(self, sandbox_id: str) -> str:
        return self._get_full_url(f"{self.SANDBOXES_PATH}/{sandbox_id}")

    def get_sandbox_ui_link(self, sandbox_id: str) -> str:
        url = urlparse(self.get_sandbox_url(sandbox_id))
        space = url.path.split("/")[3]
        return f"https://{url.hostname}/{space}/{self.SANDBOXES_LINK}/{sandbox_id}"

    def get(self, sandbox_id: str) -> Sandbox:
        url = f"{self.SANDBOXES_PATH}/{sandbox_id}"
        sb_json = self._get(url)

        return self.resource_obj.json_deserialize(self, sb_json)

    def get_detailed(self, sandbox_id: str) -> dict:
        url = f"{self.SANDBOXES_PATH}/{sandbox_id}"
        sb_json = self._get(url)

        return sb_json

    def list(self, count: int = 25, filter_opt: str = "my") -> List[Sandbox]:

        filter_params = {"count": count, "filter": filter_opt}
        list_json = self._list(path=self.SANDBOXES_PATH, filter_params=filter_params)

        return [self.resource_obj.json_deserialize(self, obj) for obj in list_json]

    def start(
        self,
        sandbox_name: str,
        blueprint_name: str,
        duration: int = 120,
        branch: str = None,
        commit: str = None,
        inputs: dict = None,
        source: str = None,
    ) -> str:
        url = "sandbox"

        source_type_map = {
            "git": "git_repository",
            "torque": "qtorque",
        }

        if commit and not branch:
            raise ValueError("Commit is passed without branch")

        iso_duration = f"PT{duration}M"

        params = {
            "sandbox_name": sandbox_name,
            "duration": iso_duration,
            "inputs": inputs,
            "source": {
                "blueprint_source_type": source_type_map.get(source, None),
                "blueprint_name": blueprint_name,
            },
        }

        if branch:
            params["source"]["branch"] = branch
            params["source"]["commit"] = commit or ""

        result_json = self._post(url, params)
        sandbox_id = result_json["id"]
        return sandbox_id

    def end(self, sandbox_id: str):
        url = f"{self.SANDBOXES_PATH}/{sandbox_id}"

        try:
            self.get(sandbox_id)

        except Exception as e:
            raise NotImplementedError(f"Unable to end sandbox with ID: {sandbox_id}. Details: {e}")

        self._delete(url)
