# scripts/utils/deploy.py
from scripts.utils.base_stage import BaseStage

class Deploy(BaseStage):
    def __init__(self, config):
        super().__init__(config)
        self.name = self.config.settings.get("name", "Unknown Project")
        self.environment = self.config.settings.get("environment", "production")

    def get_template(self):
        return {".deploy_template":{
        "stage": "deploy",
        "image": {"name": "bitnami/git:latest", "entrypoint": [""]},   
        "script":[
            'CI_GROUP_NAME=development/chart/${PROJECT_NAME}',
            'git -c http.sslVerify=false clone "https://${CI_GITLAB_USERNAME}:${CI_GITLAB_PASSWORD}@${CI_SERVER_HOST}/${CI_GROUP_NAME}/${MODULE_NAME}.git" -b ${MODULE_BRANCH}',
            'cd ${MODULE_NAME}',
            "git config --global user.email '$GIT_USER_EMAIL:-${GITLAB_USER_EMAIL}'",
            "git config --global user.name '$GIT_USER_NAME:-${GITLAB_USER_NAME}'",
            "str=${MODULE_BRANCH}",
            'sed -i "s/tag:.*/tag:\ ${CI_PIPELINE_ID}/" ${MODULE_BRANCH}.yaml',
            'git add *${str:(-3)}*.yaml && git commit -m "Add new tag $MODULE_BRANCH-$CI_PIPELINE_ID" && git -c http.sslVerify=false push origin $MODULE_BRANCH',
        ]    
    }}

    def execute(self):
        self.ci_yaml.update(self.get_template())

    def to_yaml(self):
        return self.ci_yaml