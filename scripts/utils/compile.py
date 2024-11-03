# scripts/utils/compile.py
from scripts.utils.base_stage import BaseStage

class Compile(BaseStage):
    def __init__(self, config):
        super().__init__(config)
        self.name = self.config.settings.get("name", "Unknown Project")
    def get_template(self):
        return {".compile_template":{
        "stage": "compile",
        "image": {
            "name": "gitlab.infra.bestcomp.net:4567/development/code/edms/api-backend/bcg-esd:nsdk7"
        },
        "allow_failure": False,
        "script": [
            "dotnet restore $CI_PROJECT_DIR/src/APIs/$SERVICE_NAME/$SERVICE_NAME.csproj --configfile $CI_PROJECT_DIR/NuGet.Config",
            "dotnet build $CI_PROJECT_DIR/src/APIs/$SERVICE_NAME/$SERVICE_NAME.csproj --configuration $BUILD_CONFIGURATION",
            "dotnet publish $CI_PROJECT_DIR/src/APIs/$SERVICE_NAME/$SERVICE_NAME.csproj --configuration $BUILD_CONFIGURATION --output ./apis/$MODULE_NAME/ /p:UseAppHost=false /p:SelfContained=false"
        ],
        "timeout": "2h",
        "artifacts": {
            "paths": ["./apis/$MODULE_NAME"],
            "expire_in": "1 hour"
        },
        "tags": ["RUNNER"],
        "needs": ["download_repo"],
    }}

    def execute(self):
        self.ci_yaml.update(self.get_template())

    def to_yaml(self):
        return self.ci_yaml
