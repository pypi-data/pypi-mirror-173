import uuid
from switch_guides.models.guide import SwitchGuideDefinition, SwitchGuideDefinitionOptions
from switch_guides.models.step import SwitchGuideStepDependency
from switch_guides.tasks.GuideDefinitionTask import GuideDefinitionTask
import switch_api as sw


class GuideSampleClassName_Template(GuideDefinitionTask):
    @property
    def id(self) -> uuid.UUID:
        return uuid.UUID('{GuideDefinitionId_Template}')

    @property
    def author(self):
        return '{Author_Template}'

    @property
    def version(self):
        return '0.1.0'

    @property
    def description(self) -> str:
        return """Sample Guide Definition. This description is not visible to the user. 
            Please update it with one that would help future authors understand the intention of this Guide Step."""

    @property
    def mapping_entities(self):
        return ['Readings']

    @property
    def schema(self):
        pass

    def definition(self) -> SwitchGuideDefinition:
        return SwitchGuideDefinition(
            name='{GuideName_Template}',
            description='', # Description visible to the user
            instructions='', # Instructions visible to the user
            steps=[
                SwitchGuideStepDependency(
                    order=1,
                    stepId="{GuideStepDefinitionId_Template}"
                )
            ],
            options=SwitchGuideDefinitionOptions(
                enable_live_notification=False
            )
        )


task = GuideSampleClassName_Template()

if __name__ == "__main__":
    api_inputs = sw.initialize(api_project_id='96fa3fc9-1bec-4c38-b8d3-bb985e8ad238', environment='Development')

    """ ================== REGISTER TASK ==================
    """

    # response_status, response_data = task.register(api_inputs=api_inputs)

    # print(response_status)
    # print(response_data)
