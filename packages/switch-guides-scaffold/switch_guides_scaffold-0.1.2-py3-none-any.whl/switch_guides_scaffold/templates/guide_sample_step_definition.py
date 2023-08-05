import uuid
from switch_guides.models.api import SwitchGuideStepApiResponse, SwitchGuideStepProcessInput
from switch_guides.models.step import SwitchGuideStepComponent, SwitchGuideStepDefinition, SwitchGuideStepDefinitionUiAssets, SwitchGuideStepStatus, SwitchGuideStepStatusProgress
from switch_guides.tasks.GuideStepDefinitionTask import GuideStepDefinitionTask
from switch_guides.utils.utils import ApiInputs
from switch_guides.models.enums import StepResultType

import switch_api as sw


class GuideSampleStepName_Template(GuideStepDefinitionTask):
    @property
    def id(self) -> uuid.UUID:
        return uuid.UUID('{GuideStepDefinitionId_Template}')

    @property
    def author(self):
        return '{Author_Template}'

    @property
    def version(self):
        return '0.1.0'

    @property
    def description(self) -> str:
        return """Sample Guide Step Definition. This description is not visible to the user. 
            Please update it with one that would help future authors understand the intention of this Guide Step."""

    @property
    def mapping_entities(self):
        return ['Readings']

    @property
    def schema(self):
        pass

    def definition(self) -> SwitchGuideStepDefinition:
        return SwitchGuideStepDefinition(
            name='Sample Guide Step',
            description='', # Description of the step visible to the user
            icon='map-marker',
            isEnabled=True,
            isHidden=False,
            status=SwitchGuideStepStatus(
                type='Percentage',
                messages={
                    'default': 'This step is under construction.'
                }
            ),
            # Update this component to one that represents the step use case.
            component=SwitchGuideStepComponent(
                type='Vue',
                id='JourneyStepResult',
                attributes={
                    'resultType': StepResultType.StepProgress,
                    'message': 'This step is under construction.'
                }
            ),
            callToAction=None
        )

    def check_status(self, api_inputs: ApiInputs, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepStatus:
        """This method will be called by the Guides Backend under two conditions.

            1. When user completes the requirements of a component associated with this step.
            2. Periodically to check the status of the step over time.

        Please take note of these two items:

            1. Only logic to check the current status of the step should exist here
            2. This efficient and quick as possible as the Guides backend would be calling this method regularly until completion.
        """
        status = SwitchGuideStepStatus(
            progress=SwitchGuideStepStatusProgress(
                completionPercentage=0
            )
        )

        return status

    def check_ui_assets(self, step_status: SwitchGuideStepStatus) -> SwitchGuideStepDefinitionUiAssets:
        """This method can be used to dynamically configure certain elements of the Platform Guides UI.
        Avoid external calls in this method. Use the provided step_status parameter to run you conditional logic.
        """
        return None

    def check_ui_component(self, api_inputs: ApiInputs, step_status: SwitchGuideStepStatus, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepComponent:
        """This method can be used to dynamically configure return components to be displayed on the step.
        Just like check_status, ensure this method is quick and efficient as possible.
        """
        return None

    def process(self, api_inputs: ApiInputs, journey_input: SwitchGuideStepProcessInput) -> SwitchGuideStepApiResponse:        
        """This method will be called by the Guides Backend under two conditions.
            1. When user completes the requires of a component associated with this step.
        Run your logic here to extract, process, and export data how ever you see fit.
        User may be waiting on a response so how long this method should run depends on how long a user is willing to wait.
        """
        
        return SwitchGuideStepApiResponse()

task = GuideSampleStepName_Template()

if __name__ == "__main__":
    api_inputs = sw.initialize(api_project_id='96fa3fc9-1bec-4c38-b8d3-bb985e8ad238', environment='Development')

    """ ================== REGISTER TASK ==================
    """

    # response_status, response_data = task.register(api_inputs=api_inputs)

    # print(response_status)
    # print(response_data)

    """ ================== CONFIGURE GUIDE INPUT ======================
    Valid journey_id is only required when your methods depend on it.
    Guides backend will provide the correct journey_id in production.
    """
    guide_input = SwitchGuideStepProcessInput(journey_id='')


    """ ================== RUN PROCESS LOCALLY ======================
    """

    # result = task.process(api_inputs=api_inputs,
    #                       journey_input=guide_input)
    # print(result)

    """ ================== RUN STATUS CHECK LOCALLY ======================
    """

    # status = task.check_status(api_inputs=api_inputs, journey_input=guide_input)
    # print(status)

    """ ================== RUN STATUS CHECK_UI_ASSETS LOCALLY ======================
    """

    # ui_assets = task.check_ui_assets(journey_input=guide_input, step_status=status)
    # print(ui_assets)


    """ ================== RUN STATUS CHECK_UI_COMPONENT LOCALLY ======================
    """

    # component = task.check_ui_component(api_inputs=api_inputs, journey_input=guide_input, step_status=status)
    # print(component)
