from dataclasses import dataclass, field
from pyspark.sql import SparkSession


@dataclass
class PySpark:
    '''Sets pyspark configurartion parameters.

    Reference: http://spark-configuration.luminousmen.com/
    '''

    d_config: dict = field(default_factory=dict)
    log_level: str = 'ERROR'


    def __init__(self):

        self.d_config = {
            'spark.default.parallelism': '10',
            'spark.executor.memory': '56g',
            'spark.executor.instances': '1',
            'spark.driver.cores': '5',
            'spark.executor.cores': '5',
            'spark.driver.memory': '56g',
            'spark.driver.maxResultSize': '56g',
            'spark.driver.memoryOverhead': '5734m',
            'spark.executor.memoryOverhead': '5734m',
            'spark.dynamicAllocation.enabled': 'false',
            'spark.sql.adaptive.enabled': 'true',
        }


    def get_session(self):
        '''Gets the pre configured sapark session.'''

        spark = SparkSession.builder
        for k, v in self.d_config.items():
            spark = spark.config(k, v)
        spark = spark.getOrCreate()
        spark.sparkContext.setLogLevel(self.log_level)

        return spark