import base64
import logging
import sys
from typing import Any

import yaml

from torque.branch.branch_context import ContextBranch
from torque.branch.branch_utils import get_and_check_folder_based_repo
from torque.commands.base import BaseCommand
from torque.exceptions import BadBlueprintRepo
from torque.models.blueprints import BlueprintsManager
from torque.parsers.command_input_validators import CommandInputValidator
import os

from torque.utils import BlueprintRepo

logger = logging.getLogger(__name__)


class BlueprintsCommand(BaseCommand):
    """
    usage:
        torque (bp | blueprint) list [--output=json | --output=json --detail]
        torque (bp | blueprint) validate <file> [--output=json | --output=json --detail]
        torque (bp | blueprint) get <name> [--source=<source_type>] [--output=json | --output=json --detail]
        torque (bp | blueprint) [--help]

    options:
       -o --output=json           Yield output in JSON format

       -s --source=<source_type>  Specify a type of blueprint source: 'torque' or 'git'. [default: git]

       -d --detail                Obtain full blueprint data in JSON format

       -h --help                  Show this message
    """

    RESOURCE_MANAGER = BlueprintsManager

    def get_actions_table(self) -> dict:
        return {
            "list": self.do_list,
            "validate": self.do_validate,
            "get": self.do_get,
        }

    def do_list(self) -> (bool, Any):
        detail = self.input_parser.blueprint_list.detail
        try:
            if detail:
                blueprint_list = self.manager.list_detailed()
            else:
                blueprint_list = self.manager.list()
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        return True, blueprint_list

    def do_get(self) -> (bool, Any):
        detail = self.input_parser.blueprint_get.detail
        blueprint_name = self.input_parser.blueprint_get.blueprint_name
        source = self.input_parser.blueprint_get.source

        try:
            if detail:
                bp = self.manager.get_detailed(blueprint_name, source)
            else:
                bp = self.manager.get(blueprint_name, source)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die(f"Unable to get details of blueprint '{blueprint_name}'")

        return True, bp

    def do_validate(self) -> (bool, Any):
        blueprint_file = self.input_parser.blueprint_validate.blueprint_file

        # if not os.path.isfile(blueprint_file):
        #     logger.warning("Unable ")
        #     try:
        #         repo = BlueprintRepo(os.getcwd())
        #     except BadBlueprintRepo as e:
        #         return self.die(f"Unable to load the blueprint '{blueprint_file}' from local blueprint repo; \n"
        #                         f"reason: {str(e)}")
        #
        #     if repo.repo_has_blueprint(blueprint_file):
        #         bp_yaml = repo.get_blueprint_yaml(blueprint_file)
        #         bp_content = yaml.dump(bp_yaml)
        #     else:
        #         return self.die(f"The blueprint '{blueprint_file}' wasn't found in a local blueprints repo")
        #
        # else:
        with open(blueprint_file, "r") as bp_file:
            bp_content = bp_file.read()

        encoded = base64.b64encode(bp_content.encode("utf-8"))

        try:
            bp = self.manager.validate(b64_blueprint_content=encoded.decode("utf-8"))
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        errors = bp.get("errors", [])

        if errors:
            logger.info("Blueprint validation failed")
            return False, errors

        else:
            return self.success("Blueprint is valid")
