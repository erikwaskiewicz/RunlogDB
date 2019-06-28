"""
----------------------------------------------------------------------------------------------------
main.py
-- parse data from runInfo.xml and add to runinfo dictionary
-- parse data from samplesheet.csv and add to samplesheet dictionary
-- parse data from interops files and add to interop dictionary
-- add data from dictionaries above to runlog table in RunlogDB
-- determine if run was from hiseq or miseq
-- add data from RunParameters.xml file to either hiseq or miseq table in RunlogDB
----------------------------------------------------------------------------------------------------
"""
import sys
import json
from django.core.management.base import BaseCommand, CommandError
from db.models import *
# Import scripts
from db.utils.parsers import add_to_db, parse_interop, parse_runinfo, parse_runparameters, parse_samplesheet
#from . import add_to_db_new


#from .models import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('run_folder')


    def handle(self, *args, **options):
        # Load run folder
        run_folder = options['run_folder']
        #run_folder = r"/Users/erik/Documents/RunLog"

# ----------------------------------------------------------------------------------------------------
# PARSE RUNINFO

        runinfo_full_dict = parse_runinfo.get_runinfo_dict(run_folder)
        run_sorted_dict = parse_runinfo.extract_data(runinfo_full_dict)


# ----------------------------------------------------------------------------------------------------
# PARSE RUNPARAMETERS

        runparameters_full_dict = parse_runparameters.get_runparameters_dict(run_folder)
        run_sorted_dict['raw_runparameters_json'] = json.dumps(runparameters_full_dict, indent=2, separators=(',', ':'))

        # TODO any specific data needed - chemistry version??


# ----------------------------------------------------------------------------------------------------
# PARSE INTEROPS

        # create empty dictionary
        #interop_dict = {}

        # parse (parameters set in function)
        run_sorted_dict.update(parse_interop.parse(run_folder))


# ----------------------------------------------------------------------------------------------------
# PARSE SAMPLESHEET


        samplesheet_full_dict = parse_samplesheet.get_samplesheet_dict(run_folder)

        # extract run level fields from samplesheet dict and add to run level dictionary
        run_sorted_dict.update(parse_samplesheet.extract_data(samplesheet_full_dict))
        run_sorted_dict['raw_samplesheet_json'] = json.dumps(samplesheet_full_dict, indent=2, separators=(',', ':'))

        #print(run_sorted_dict['raw_samplesheet_json'])
        #print(run_sorted_dict.keys())
        #print(samplesheet_full_dict)


# ----------------------------------------------------------------------------------------------------
# ADD TO DATABASE


        # TODO: Format pipeline???
        worksheets = samplesheet_full_dict['Data'].keys()
        worksheet_obj_list = []
        for ws in worksheets:
            # within in worsheet, loops through samples
            ws_data = samplesheet_full_dict['Data'][ws]
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
                samplerun_uid = f"{s}_{ws}_{run_sorted_dict['run_id']}"
                try:
                    sample_run_obj = SampleRun.objects.get(unique_id=samplerun_uid)
                except SampleRun.DoesNotExist:
                    sample_run_obj = SampleRun(
                        unique_id=samplerun_uid,
                        sample_obj=sample_obj,
                        description=sample_data['Description'],
                        sex=sample_data['sex'],
                        i5_name='',
                        i5_seq='',
                        i7_name=sample_data['I7_Index_ID'],
                        i7_seq=sample_data['index'],
                        sample_well=sample_data['Sample_Well'],
                        sample_project=sample_data['Sample_Project']
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
            instrument_obj = Instrument.objects.get(instrument_id=run_sorted_dict['instrument'])
        except Instrument.DoesNotExist:
            instrument_id = run_sorted_dict['instrument']
            if instrument_id.startswith('M'):
                instrument_type = 'MiSeq'
            elif instrument_id.startswith('D'):
                instrument_type = 'HiSeq'
            elif instrument_id.startswith('NB'):
                instrument_type = 'NextSeq'
            else:
                instrument_type = ''
            instrument_obj = Instrument(
                instrument_id=instrument_id,
                instrument_type=instrument_type
            )
            instrument_obj.save()

        # add run
        try:
            run_obj = Run.objects.get(run_id=run_sorted_dict['run_id'])
        except Run.DoesNotExist:
            run_obj = Run(
                run_id=run_sorted_dict['run_id'],
                instrument=instrument_obj,
                instrument_date='2000-01-01', #run_sorted_dict['instrument_date'], TODO - reformat dict date
                samplesheet_date=run_sorted_dict['samplesheet_date'],
                investigator=run_sorted_dict['investigator'],
                experiment=run_sorted_dict['experiment'],
                workflow=run_sorted_dict['workflow'],
                application=run_sorted_dict['application'],
                assay=run_sorted_dict['assay'],
                chemistry=run_sorted_dict['chemistry'],
                description=run_sorted_dict['description'],
                num_reads=run_sorted_dict['num_reads'],
                length_read1=run_sorted_dict['length_read1'],
                num_indexes=run_sorted_dict['num_indexes'],
                length_index1=run_sorted_dict['length_index1'],
                percent_q30=run_sorted_dict['percent_q30'],
                cluster_density=run_sorted_dict['cluster_density'],
                percent_pf=run_sorted_dict['percent_pf'],
                phasing=run_sorted_dict['phasing'],
                prephasing=run_sorted_dict['prephasing'],
                error_rate=run_sorted_dict['error_rate'],
                percent_aligned=run_sorted_dict['aligned'],
                diagnostic_run=True,
                raw_runinfo_json=run_sorted_dict['raw_runinfo_json'],
                raw_runparameters_json=run_sorted_dict['raw_runparameters_json'],
                raw_samplesheet_json=run_sorted_dict['raw_samplesheet_json']
            )
            run_obj.save()

            try: 
                run_obj.length_read2 = run_sorted_dict['length_read2']
            except KeyError:
                pass
            try:
                run_obj.length_index2 = run_sorted_dict['length_index2']
            except KeyError:
                pass

            run_obj.worksheets.add(*worksheet_obj_list)
            run_obj.save()
