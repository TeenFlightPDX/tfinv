import csv
import tempfile
import shutil
from .models import Kit, Section, Page, Step


class csvmanager(object):

    def process_uploaded_csv(uploaded_file, auto_confirm):
        fd, filepath = tempfile.mkstemp(prefix=uploaded_file.name)
        with open(filepath, 'wb') as dest:
            shutil.copyfileobj(uploaded_file, dest)

        # Re-open the tempfile in read-only mode
        with open(filepath, 'r', encoding='latin1') as csvfile:
            reader = csv.DictReader(csvfile)

            # Re-assemble the section dictionary
            # section_dict: Key = section ; Value = page_dict
            # page_dict: Key = page ; Value = step_dict
            # step_dict: Key = step ; Value = step_text
            section_dict = {}

            for row in reader:
                page_full = row['page'].split('-')
                step = row['step']
                step_text = row['text']

                # Page = 07-01 -> [07, 01]
                section = page_full[0]
                page = page_full[1]

                # If the page_dict does not already exist, create it
                if section not in section_dict:
                    section_dict[section] = {}

                # Get the page_dict for this section
                page_dict = section_dict[section]

                # If the step_dict does not already exist, create it
                if page not in page_dict:
                    page_dict[page] = {}

                # Get the step_dict for this section
                step_dict = page_dict[page]

                # If the step_text does not already exist, create it
                if step not in step_dict:
                    page_dict[page] = {}
                    step_dict[step] = step_text
                else:
                    # The step already exists - do we want to override?
                    print("Step %s in Page %s already exists!" % (step, page))

                # Replace the old step_dict in the page
                page_dict[page] = step_dict

                # Replace the old page_dict in the section_dict
                section_dict[section] = page_dict

            # Prepare page_dict for input into db model
            for section_text, page_dict in section_dict.items():
                # Add section to db model
                section_model = None
                try:
                    # Check if the section number exists in the db model
                    section_model = Section.objects.get(
                        section_number=section_text)
                except Section.DoesNotExist:

                    # Check if the "Unassigned" kit exists, if not, create it
                    try:
                        unassigned_kit = Kit.objects.get(name='Unassigned')
                    except Kit.DoesNotExist:
                        unassigned_kit = Kit(name='Unassigned')
                        unassigned_kit.save()

                    # Section does not exist - Create new Section with a
                    # placeholder name
                    section_model = Section(
                        section_number=section_text, name="Unknown Section", confirmed=auto_confirm, kit=unassigned_kit)
                    section_model.save()
                except Section.MultipleObjectsReturned:
                    # TODO: Corrupted database? Go to the next item in the loop
                    print(
                        "Error: Multiple sections returned for Section %s. Corrupted database?" % section_text)
                    continue

                for page_text, step_dict in page_dict.items():
                    # Add page to db model
                    page_model = None
                    try:
                        # Check if the page number exists in the db model
                        Page.objects.get(section=section_model,
                                         page_number=page_text)
                    except Page.DoesNotExist:
                        # Page does not exist - Create new Page
                        page_model = Page(
                            section=section_model, page_number=page_text, confirmed=auto_confirm)
                        page_model.save()
                    except Page.MultipleObjectsReturned:
                        # TODO: Corrupted database? Go to the next item in the
                        # loop
                        print("Error: Multiple pages returned for page %s-%s. Corrupted database?" %
                              (section_text, page_text))
                        continue

                    for step_number, step_text in step_dict.items():
                        step_number_int = int(step_number)

                        # Add step to db model
                        step_model = None
                        try:
                            # Check if the step number exists in the db model
                            Step.objects.get(
                                page=page_model, step_number=step_number_int)
                            print("Error: Step %s on page %s-%s already exists!" %
                                  (step_number, page_text, section_text))
                        except Step.DoesNotExist:
                            # Step does not exist - Create new Step
                            step_model = Step(
                                page=page_model, step_number=step_number_int, step_text=step_text, confirmed=auto_confirm)
                            step_model.save()
                        except Step.MultipleObjectsReturned:
                            # TODO: Corrupted database? Go to the next item in
                            # the loop
                            print("Error: steps returned for Step %s on page %s-%s. Corrupted database?" % (
                                step_number, section_text, page_text))
                            continue
