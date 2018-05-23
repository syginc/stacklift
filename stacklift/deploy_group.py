#!/usr/bin/env python3

import asyncio
import yaml
from stacklift.deploy_template import DeployTemplate
from stacklift.cfn_deploy import DeployStatus
import os
import logging


logging.basicConfig(format="[%(name)s] %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

class DeployGroup:
    def __init__(self, config_file, group_file, function_root):
        self.config_file = config_file
        self.function_root = function_root

        with open(group_file) as f:
            self.group_config = yaml.load(f)
        self.group_file_dir = os.path.dirname(group_file)

        self.template_dict = {template["Name"]: template for template in self.group_config["Templates"]}
        self.deploy_futures = {}

    def get_template(self, name):
        template = self.template_dict.get(name)
        if template is None:
            raise RuntimeError("Template {} is not found.".format(name))
        return template

    async def deploy(self, name, start_ready_event):
        await start_ready_event.wait()

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        template = self.get_template(name)
        depends = template.get("Depends") or []
        if depends:
            depend_results = await asyncio.gather(*[self.deploy_futures[x] for x in depends])
            if not all(depend_results):
                logger.info("Not start")
                return None

            if not all([x.deploy_status in [DeployStatus.UNCHANGED,
                                            DeployStatus.CHANGESET_COMPLETED] for x in depend_results]):
                raise RuntimeError("Dependent stack(s) did not complete changing")

        try:
            filename = template.get("Filename")
            template_file = os.path.join(self.group_file_dir, filename) if filename else None
            deploy_template = DeployTemplate(template_file=template_file,
                                             config_file=self.config_file,
                                             section_name=name,
                                             stack_desired_state=template.get("StackDesiredState"))
            deploy_result = await deploy_template.deploy(function_root=self.function_root)

            return deploy_result
        except:
            logger.exception("Failed to deploy")
            return None

    async def deploy_all(self):
        start_ready_event = asyncio.Event()
        for name in self.template_dict.keys():
            self.deploy_futures[name] = asyncio.ensure_future(self.deploy(name, start_ready_event))
        start_ready_event.set()

        results = await asyncio.gather(*self.deploy_futures.values())
        if not all(results):
            raise RuntimeError("Deploy failed")

        lines = ["", "# Changes", ""]
        for result in results:
            if result.deploy_status is not DeployStatus.UNCHANGED:
                lines.append(str(result))
                lines.append("")

        logger.info("\n".join(lines))

def deploy_group(config_file, group_file, function_root):
    instance = DeployGroup(config_file=config_file, group_file=group_file, function_root=function_root)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(instance.deploy_all())
