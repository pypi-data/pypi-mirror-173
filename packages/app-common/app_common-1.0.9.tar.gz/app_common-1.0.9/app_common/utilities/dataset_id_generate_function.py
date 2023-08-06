import datetime
import logging

logger = logging.getLogger(__name__)


class IDGenerator(object):
    GLIDER = 1

    @staticmethod
    def generate_id(project_id, **kwargs):
        """
        Generate dataset ID for ERDDAP, by given platform and other arguments
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        if project_id == IDGenerator.GLIDER:
            try:
                return IDGenerator.generate_glider_id(**kwargs)
            except KeyError as e:
                msg = "missing variable {}".format(e)
                logger.error(msg)
                return None
        else:
            msg = "Invalid platform type {}".format(project_id)
            raise ValueError(msg)

    @staticmethod
    def generate_glider_id(**kwargs):
        """
        Generate dataset id for glider platform
        :param platform_type:
        :param kwargs:
        :return:
        """
        platform_name = kwargs.pop("platform_name")
        # time_format_check
        start_time = kwargs.pop("start_time")
        deployment_number = kwargs.pop("deployment_number")
        test = kwargs.pop("test")
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        return IDGenerator._generate_glider_id(platform_name, start_time, deployment_number, test, **kwargs)

    @staticmethod
    def _generate_glider_id(platform_name, start_time, deployment_number, test, **kwargs):
        """
        Generate dataset id for slocum dataset id
        :param platform_name:
        :param start_time:
        :param deployment_number:
        :param test:
        :param kwargs:
        :return:
        """
        try:
            mode = kwargs.pop("mode")
        except ValueError:
            mode = False
            msg = "mode value is not given, default is delayed"
            logger.warning(msg)
        if mode:
            mode = 'realtime'
        else:
            mode = 'delayed'
        id_format = "{0}_{1:%Y%m%d}_{2}_{3}"
        if test:
            id_format = id_format + "_test"

        dataset_id = id_format.format(platform_name, start_time, deployment_number, mode)
        return dataset_id
