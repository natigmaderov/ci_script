# scripts/utils/build.py
from scripts.utils.base_stage import BaseStage

class Build(BaseStage):
    def __init__(self, config):
        super().__init__(config)
        self.name = self.config.settings.get("name", "Unknown Project")

    def get_template(self):
        return {".build_template":{
        "image": {"name": "gcr.io/kaniko-project/executor:debug", "entrypoint": [""]},
        "stage": "build",
        "before_script": ["echo $CI_PROJECT_DIR"],
        "script": [
            "mkdir -p /kaniko/.docker",
            "AUTH=$(echo -n ${CI_GITLAB_USERNAME}:${CI_GITLAB_PASSWORD} | base64)",
            "echo \"{\\\"auths\\\":{\\\"${CI_REGISTRY}\\\":{\\\"auth\\\":\\\"$AUTH\\\"}}}\" > /kaniko/.docker/config.json",
            "cat /kaniko/.docker/config.json",
            "/kaniko/executor --context $CI_PROJECT_DIR --dockerfile ./docker_repo/${MODULE_NAME}/Dockerfile $BUILD_ARG --insecure --skip-tls-verify --destination ${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}/${PROJECT_NAME}-${MODULE_NAME}:$CI_PIPELINE_ID"
        ],
        "timeout": "2h",
        "allow_failure": True,
        "tags": ["RUNNER"],
        "only": {"refs": []}
    }}

    def execute(self):
        self.ci_yaml.update(self.get_template())

    def to_yaml(self):
        return self.ci_yaml