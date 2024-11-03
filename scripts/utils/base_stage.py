# scripts/utils/base_stage.py
class BaseStage:
    def __init__(self, config):
        self.config = config
        self.ci_yaml = {}  # Initialize ci_yaml as an empty dictionary
    # def template(self):
    #     raise NotImplementedError("Subclasses must implement the execute method.")


    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

    def to_yaml(self):
        """Convert the stage to YAML format."""
        raise NotImplementedError("Subclasses must implement the to_yaml method.")
