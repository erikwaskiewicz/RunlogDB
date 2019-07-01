import sys
import json

from django.core.management.base import BaseCommand, CommandError
from db.utils.parsers import parse_interop, parse_runinfo, parse_runparameters, parse_samplesheet
from db.models import Sample, Instrument, Run, Worksheet, SampleRun


def add_to_db(full_samplesheet_dict, run_level_dict):
    worksheets = full_samplesheet_dict['Data'].keys()
    worksheet_obj_list = []
    for ws in worksheets:
        # within in worsheet, loops through samples
        ws_data = full_samplesheet_dict['Data'][ws]
        samples = ws_data['samples'].keys()

        sample_obj_list = []
        sample_run_obj_list = []

        for s in samples:
            sample_data = ws_data['samples'][s]

            # add sample object 
            try:
                sample_obj = Sample.objects.get(sample_id=s)
            except Sample.DoesNotExist:
                sample_obj = Sample(sample_id=s)
                sample_obj.save()
            sample_obj_list += [sample_obj]

            # add samplerun object
            samplerun_uid = f"{s}_{ws}_{run_level_dict['run_id']}"
            try:
                sample_run_obj = SampleRun.objects.get(unique_id=samplerun_uid)
            except SampleRun.DoesNotExist:
                sample_run_obj = SampleRun(
                    unique_id=samplerun_uid,
                    sample_obj=sample_obj,
                    description=sample_data['Description'],
                    sex=sample_data['sex'],
                    i7_name=sample_data['I7_Index_ID'],
                    i7_seq=sample_data['index'],
                    sample_well=sample_data['Sample_Well'],
                    )
                sample_run_obj.save()

                try: 
                    sample_run_obj.I5_name = sample_data['I5_Index_ID']
                except KeyError:
                    pass
                try: 
                    sample_run_obj.I5_seq = sample_data['index2']
                except KeyError:
                    pass
                sample_run_obj.save()
            sample_run_obj_list += [sample_run_obj]

        # add worksheet
        try:
            ws_obj = Worksheet.objects.get(ws_id=ws)
        except Worksheet.DoesNotExist:
            ws_obj = Worksheet(
                ws_id=ws,
                pipeline_name=ws_data['pipelineName'],
                pipeline_version=ws_data['pipelineVersion'],
                panel=ws_data['panel']
            )
            ws_obj.save()
            ws_obj.samples.add(*sample_run_obj_list) # add all sampleruns at once
            ws_obj.save()

        worksheet_obj_list += [ws_obj]
            
    # add instrument
    try:
        instrument_obj = Instrument.objects.get(instrument_id=run_level_dict['instrument'])
    except Instrument.DoesNotExist:
        # get instrument info
        instrument_id = run_level_dict['instrument']
        instrument_type = parse_runparameters.get_instrument_type(instrument_id)
        # make new instrument object
        instrument_obj = Instrument(
            instrument_id=instrument_id,
            instrument_type=instrument_type
        )
        instrument_obj.save()

    # add run
    try:
        run_obj = Run.objects.get(run_id=run_level_dict['run_id'])
        # TODO add warning if run already exists?
    except Run.DoesNotExist:
        run_obj = Run(
            run_id=run_level_dict['run_id'],
            instrument=instrument_obj,
            instrument_date=run_level_dict['instrument_date'],
            samplesheet_date=run_level_dict['samplesheet_date'],
            investigator=run_level_dict['investigator'],
            experiment=run_level_dict['experiment'],
            workflow=run_level_dict['workflow'],
            application=run_level_dict['application'],
            assay=run_level_dict['assay'],
            chemistry=run_level_dict['chemistry'],
            description=run_level_dict['description'],
            num_reads=run_level_dict['num_reads'],
            length_read1=run_level_dict['length_read1'],
            num_indexes=run_level_dict['num_indexes'],
            length_index1=run_level_dict['length_index1'],
            percent_q30=run_level_dict['percent_q30'],
            cluster_density=run_level_dict['cluster_density'],
            percent_pf=run_level_dict['percent_pf'],
            phasing=run_level_dict['phasing'],
            prephasing=run_level_dict['prephasing'],
            error_rate=run_level_dict['error_rate'],
            percent_aligned=run_level_dict['aligned'],
            diagnostic_run=True,
            raw_runinfo_json=run_level_dict['raw_runinfo_json'],
            raw_runparameters_json=run_level_dict['raw_runparameters_json'],
            raw_samplesheet_json=run_level_dict['raw_samplesheet_json']
        )
        run_obj.save()

        # try to add optional fields if they are in the dict
        try: 
            run_obj.length_read2 = run_level_dict['length_read2']
        except KeyError:
            pass
        try:
            run_obj.length_index2 = run_level_dict['length_index2']
        except KeyError:
            pass

        # add worksheet relations
        run_obj.worksheets.add(*worksheet_obj_list)
        run_obj.save()
    print('done')



"""
----------------------------------------------------------------------------------------------------
upload_run
-- parse data from runInfo.xml and add to run level dictionary
-- parse data from RunParameters.xml and add to run level dictionary
-- parse data from interops files and add to run level dictionary
-- parse data from samplesheet.csv and add to samplesheet dictionary
-- determine if run was from miseq/hiseq/nextseq
-- upload data
----------------------------------------------------------------------------------------------------
"""
class Command(BaseCommand):
    help = 'Upload a run to the RunlogDB'

    def add_arguments(self, parser):
        parser.add_argument('run_folder')
        parser.add_argument('--nipt', action='store_true', help="NIPT run")


    def handle(self, *args, **options):
        # Load run folder
        run_folder = options['run_folder']

        # PARSE RUNINFO
        full_runinfo_dict = parse_runinfo.get_runinfo_dict(run_folder)
        run_level_dict = parse_runinfo.extract_data(full_runinfo_dict)

        # PARSE RUNPARAMETERS
        full_runparameters_dict = parse_runparameters.get_runparameters_dict(run_folder)
        run_level_dict['raw_runparameters_json'] = json.dumps(full_runparameters_dict, indent=2, separators=(',', ':'))

        # TODO any specific data needed - chemistry version??

        # PARSE INTEROPS
        run_level_dict.update(parse_interop.parse(run_folder))

        # PARSE SAMPLESHEET
        # TODO finish off
        if options['nipt']:
            full_samplesheet_dict = parse_samplesheet.get_samplesheet_dict(run_folder, run_type='nipt')
        else:
            full_samplesheet_dict = parse_samplesheet.get_samplesheet_dict(run_folder)


        # extract run level fields from samplesheet dict and add to run level dictionary
        run_level_dict.update(parse_samplesheet.extract_data(full_samplesheet_dict))
        run_level_dict['raw_samplesheet_json'] = json.dumps(full_samplesheet_dict, indent=2, separators=(',', ':'))

        #print(run_level_dict['raw_samplesheet_json'])
        #print(run_level_dict.keys())
        #print(full_samplesheet_dict)

        # ADD TO DATABASE
        add_to_db(full_samplesheet_dict, run_level_dict)
