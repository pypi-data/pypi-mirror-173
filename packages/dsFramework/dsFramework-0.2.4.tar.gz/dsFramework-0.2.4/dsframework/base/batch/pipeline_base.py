from typing import Mapping, OrderedDict
from .stage_base import PipelineStage


class Pipeline:

    def __init__(self):
        # Override
        self.stages: Mapping[str, PipelineStage] = {}

    def run_stage(self, stage_name: str):
        if stage_name not in self.stages:
            stage_names = '\n'.join(sorted(self.stages.keys()))
            raise KeyError(f"Stage '{stage_name}' not found among stages:\n {stage_names}")

        stage = self.stages[stage_name]
        stage.go()

    def run_all_stages(self):
        log = logging.getLogger(__name__)

        assert type(self.stages) is OrderedDict, "Pipeline self.stages must be an OrderedDict to use run_all_stages()"

        if 'spark' in self.__dir__():
            try:
                # TODO -- not sure if this is needed, since all sparkConf parameters show up in the Spark Job page
                #   and it may be very long and verbose
                log.info("Spark config:", self.spark.sparkContext.getConf().getAll())
            except:
                # self.spark wasn't a SparkSession object
                pass

        start = time.time()
        for stage_name, stage in self.stages.items():
            self.run_stage(stage_name)
        elapsed = time.time() - start

        log.info('Finished all stages in %0.1f min' % (elapsed / 60.))
