"""
Test workflows.status_reporter
"""

import os
from unittest.mock import patch

import toml
from cpg_utils import Path, to_path
from cpg_utils.config import get_config, set_config_paths, update_dict
from cpg_utils.hail_batch import dataset_path
from cpg_utils.workflows.batch import get_batch
from cpg_utils.workflows.inputs import get_cohort
from cpg_utils.workflows.targets import Cohort, Sample
from cpg_utils.workflows.utils import timestamp
from cpg_utils.workflows.workflow import (ExpectedResultT, SampleStage,
                                          StageInput, StageOutput,
                                          run_workflow, stage)
from pytest_mock import MockFixture

tmp_dir_path = to_path(__file__).parent / 'results' / timestamp()
tmp_dir_path = tmp_dir_path.absolute()
tmp_dir_path.mkdir(parents=True, exist_ok=True)

DEFAULT_CONF = f"""
[workflow]
dataset_gcp_project = 'fewgenomes'
access_level = 'test'
dataset = 'fewgenomes'
driver_image = '<stub>'
sequencing_type = 'genome'

check_inputs = false
check_intermediates = false
check_expected_outputs = false
path_scheme = 'local'

[hail]
billing_project = 'fewgenomes'
delete_scratch_on_exit = false
backend = 'local'
"""


def _set_config(dir_path: Path, extra_conf: dict | None = None):
    d = toml.loads(DEFAULT_CONF)
    d['workflow']['local_dir'] = str(dir_path)
    if extra_conf:
        update_dict(d, extra_conf)
    config_path = dir_path / 'config.toml'
    with config_path.open('w') as f:
        toml.dump(d, f)
    set_config_paths([str(config_path)])


def mock_get_dataset_bucket_url(dataset: str, bucket_type: str) -> str:
    config = get_config()
    root = config['workflow']['local_dir']
    return os.path.join(root, f'{dataset}-{bucket_type}')


@patch('cpg_utils.hail_batch.get_dataset_bucket_url', side_effect=mock_get_dataset_bucket_url)
def test_status_reporter(mock_obj, mocker: MockFixture):
    """
    Testing metamist status reporter.
    """
    _set_config(
        tmp_dir_path,
        {
            'workflow': {
                'status_reporter': 'metamist',
            },
            'hail': {
                'dry_run': True,
            },
        },
    )

    def mock_create_new_analysis(_, project, analysis_model) -> int:
        print(f'Analysis model in project {project}: {analysis_model}')
        return 1  # metamist "analysis" entry ID

    mocker.patch(
        'sample_metadata.apis.AnalysisApi.create_new_analysis', mock_create_new_analysis
    )

    def mock_create_cohort() -> Cohort:
        c = Cohort()
        ds = c.create_dataset('my_dataset')
        ds.add_sample('CPG01', external_id='SAMPLE1')
        ds.add_sample('CPG02', external_id='SAMPLE2')
        return c

    mocker.patch('cpg_utils.workflows.inputs.create_cohort', mock_create_cohort)

    @stage(analysis_type='qc')
    class MyQcStage(SampleStage):
        """
        Just a sample-level stage.
        """

        def expected_outputs(self, sample: Sample) -> ExpectedResultT:
            return dataset_path(f'{sample.id}.tsv')

        def queue_jobs(self, sample: Sample, inputs: StageInput) -> StageOutput | None:
            j = self.b.new_job('Echo', self.get_job_attrs(sample) | dict(tool='echo'))
            j.command(f'echo {sample.id}_done >> {j.output}')
            self.b.write_output(j.output, str(self.expected_outputs(sample)))
            print(f'Writing to {self.expected_outputs(sample)}')
            return self.make_outputs(sample, self.expected_outputs(sample), [j])

    run_workflow(stages=[MyQcStage])

    assert 'metamist' in get_batch().job_by_tool, get_batch().job_by_tool
    assert (
        get_batch().job_by_tool['metamist']['job_n']
        == len(get_cohort().get_samples()) * 2
    )
