import os
import uuid
import click
from click_help_colors import HelpColorsGroup
import click_spinner


@click.group(
    cls=HelpColorsGroup, help_headers_color="yellow", help_options_color="green"
)
def cli_init():
    pass


@cli_init.command()
@click.option(
    "--guidename",
    prompt="Name your guide",
    help="What would you like to call this guide?",
)
@click.option(
    "--authorname", prompt="Your name", help="Who is the author of this guide?"
)
def create(guidename, authorname):
    guidename = guidename.replace(' ', '')
    
    click.echo(f"Hi, {authorname}")
    click.echo(f"Your guide will be called '{guidename}'")
    click.echo()

    directory = prompt_output_directory()

    click.echo()
    click.echo(f"Guide name: {guidename}")
    click.echo(f"Author name: {authorname}")
    click.echo(f"Directory: {directory}")
    click.echo()

    final_confirmation = click.confirm(f"Are these details correct?", default=True)
    if not final_confirmation:
        click.echo(f"Guide creation is cancelled. Please start again.")
        return

    click.echo(f"Creating your guide now...")
    with click_spinner.spinner():
        click.echo()

        # Create Guide Step Definition
        sample_guide_step_template = get_sample_guide_step()
        if not sample_guide_step_template:
            click.echo(
                f"Guide template could not be located. Please contact Switch Automation for assistance.",
                err=True,
            )
            return

        sample_guide_step_template = sample_guide_step_template.replace(
            "{GuideName_Template}", guidename
        )

        guide_step_class_name = f"{guidename}GuideStepDefinition"

        sample_guide_step_template = sample_guide_step_template.replace(
            "GuideSampleStepName_Template", guide_step_class_name
        )
        guide_step_definition_id = f"{uuid.uuid4()}"
        sample_guide_step_template = sample_guide_step_template.replace(
            "{GuideStepDefinitionId_Template}", guide_step_definition_id
        )
        sample_guide_step_template = sample_guide_step_template.replace(
            "{Author_Template}", authorname
        )

        output_guide_path = os.path.join(directory, f"{guide_step_class_name}.py")
        with open(output_guide_path, "w") as output_file:
            output_file.write(sample_guide_step_template)

        # Create Guide Definition
        sample_guide_template = get_sample_guide()
        if not sample_guide_template:
            click.echo(
                f"Guide template could not be located. Please contact Switch Automation for assistance.",
                err=True,
            )
            return

        sample_guide_template = sample_guide_template.replace(
            "{GuideName_Template}", guidename
        )

        guide_class_name = f"{guidename}GuideDefinition"

        sample_guide_template = sample_guide_template.replace(
            "GuideSampleClassName_Template", guide_class_name
        )
        sample_guide_template = sample_guide_template.replace(
            "{GuideDefinitionId_Template}", f"{uuid.uuid4()}"
        )
        sample_guide_template = sample_guide_template.replace(
            "{Author_Template}", authorname
        )
        sample_guide_template = sample_guide_template.replace(
            "{GuideStepDefinitionId_Template}", guide_step_definition_id
        )

        output_guide_path = os.path.join(directory, f"{guide_class_name}.py")
        with open(output_guide_path, "w") as output_file:
            output_file.write(sample_guide_template)

        click.echo(f"Guide definition files where created successfully")


def prompt_output_directory():
    dir_confirmation = False
    default_dir = f"{os.getcwd()}\generated_guides"

    while not dir_confirmation:
        directory = click.prompt(
            f"Which directory would you like your guide definitions created in?",
            default=default_dir,
        )

        if not os.path.isdir(directory):
            click.echo(
                "Directory will be created on completion of this as it does not exist yet."
            )

        dir_confirmation = click.confirm(
            f"Are you sure you would like to your guides at `{directory}`?",
            default=True,
        )
    return directory


def valid_step_count(number):
    try:
        number = int(number)
        if number < 1 or number > 9:
            return False
        return True
    except:
        return False


def get_sample_guide():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    templates_path = os.path.join(dir_path, "templates")
    if not os.path.isdir(templates_path):
        return None

    guide_sample_path = os.path.join(templates_path, "guide_sample_definition.py")

    with open(guide_sample_path, encoding="utf-8") as f:
        return f.read()


def get_sample_guide_step():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    templates_path = os.path.join(dir_path, "templates")
    if not os.path.isdir(templates_path):
        return None

    guide_sample_path = os.path.join(templates_path, "guide_sample_step_definition.py")

    with open(guide_sample_path, encoding="utf-8") as f:
        return f.read()


@cli_init.command()
def list():
    click.echo(f"Not implemented yet.")


if __name__ == "__main__":
    cli_init()
