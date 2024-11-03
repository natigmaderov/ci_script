import importlib
import sys
import os
import yaml
from pathlib import Path

# Add the root directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

class StageFactory:
    """Factory to create stage instances."""
    stage_registry = {}

    @classmethod
    def register_stage(cls, stage_name, stage_class):
        cls.stage_registry[stage_name.lower()] = stage_class

    @classmethod
    def create_stage(cls, stage_name, config):
        stage_class = cls.stage_registry.get(stage_name.lower())
        if not stage_class:
            raise ValueError(f"Stage {stage_name} is not registered.")
        return stage_class(config)

    @classmethod
    def discover_stages(cls):
        """Automatically discover and register all stages in the utils directory."""
        utils_dir = Path(__file__).resolve().parent / "utils"
        
        for filename in os.listdir(utils_dir):
            if filename.endswith(".py") and filename != "base_stage.py":
                stage_name = filename[:-3]
                try:
                    # Dynamically import the module
                    module = importlib.import_module(f"scripts.utils.{stage_name}")
                    
                    # Get the class and register it
                    stage_class = getattr(module, stage_name.capitalize(), None)
                    if stage_class:
                        cls.register_stage(stage_name, stage_class)
                except (ImportError, AttributeError) as e:
                    print(f"Error loading stage {stage_name}: {e}")

class ProjectPipeline:
    def __init__(self, project_file):
        self.project_file = project_file
        self.config = None
        self.project_stages = []
        self.stages = []
        self.load_project_config()
        self.load_stages()

    def load_project_config(self):
        try:
            self.config = importlib.import_module(f"projects.{self.project_file}")
            self.project_stages = self.config.settings["stages"]
        except ImportError as e:
            print(f"Error loading project configuration: {e}")
            self.project_stages = []

    def load_stages(self):
        for stage in self.project_stages:
            try:
                stage_instance = StageFactory.create_stage(stage, self.config)
                self.stages.append(stage_instance)
            except ValueError as e:
                print(f"Error loading stage: {e}")

    def execute(self):
        print(f"Running pipeline for {self.config.settings.get('name', 'Unknown Project')}")
        for stage in self.stages:
            stage.execute()

    def generate_yaml(self):
        """Generate YAML representation of the pipeline stages."""
        final_ci_yaml = {"stages":self.project_stages}
        for stage in self.stages:
            final_ci_yaml.update(stage.to_yaml())
        return yaml.dump(final_ci_yaml, default_flow_style=False)

if __name__ == "__main__":
    StageFactory.discover_stages()

    project_file = "icms"  # Change to the desired project file
    pipeline = ProjectPipeline(project_file)
    pipeline.execute()  # Use the correct method to execute the pipeline

    # Generate and print the YAML representation
    yaml_output = pipeline.generate_yaml()
    print("Generated Pipeline YAML:")
    print(yaml_output)


