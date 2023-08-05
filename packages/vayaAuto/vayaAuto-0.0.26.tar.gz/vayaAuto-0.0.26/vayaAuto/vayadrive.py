from vayaAuto import __BASE__
import xml.etree.ElementTree as ET
import string
import configparser
import time
import copy
import yaml
import threading
from yaml.loader import SafeLoader
import logging
from subprocess import Popen, PIPE, STDOUT
from vayaAuto.section import Section
import os
import queue
logger = logging.getLogger()


def osPath(func):
    def wrapper(*args, **kwargs):

        if os.name == 'nt':
            osArgs = []
            for i, arg in enumerate(args):
                if isinstance(arg, str):
                    osArg = os.sep.join(arg.split('/'))
                    osArgs.append(osArg)
                else:
                    osArgs.append(arg)
            func(*tuple(osArgs), **kwargs)
        else:
            func(*tuple(args), **kwargs)
    return wrapper


class VayaDrive(object):
    VD, VDCONSOLE = 0, 1
    _CONFIGURATION_TREE = {}
    __INSTANCE = None

    @osPath
    def __init__(self, vaya_dir_path, console=False):
        VayaDrive.__INSTANCE = self
        self.process_output = []
        self.temp_ini_file_path = os.path.join(__BASE__, 'temp.ini')
        self.local_ini_path = os.path.join(os.path.dirname(vaya_dir_path), 'local.ini')
        self.vaya_dir_path = vaya_dir_path
        self.log_catcher_thread = None
        self.timeout_thread = None
        self.exceptions_bucket = None
        self.version = None
        self.is_paused = False
        self.can_bus_selected_units = None
        self.playback_done = False
        self.ignore_list = []
        self.compiled = False
        self.configuration = {}
        if self.vaya_dir_path in VayaDrive._CONFIGURATION_TREE.keys():
            self.configuration = copy.deepcopy(VayaDrive._CONFIGURATION_TREE[self.vaya_dir_path])
        self.b_configuration = {}
        self.exe_path = None
        self.default_config_folder = os.path.join(vaya_dir_path, 'DefaultConfigs')
        self.default_config_paths = {}
        self.parent_dir = os.path.abspath(os.path.join(vaya_dir_path, os.pardir))
        self._seq_output_folder = ''
        self._consoleMode = 0
        self.vayadrive_process = None
        if os.path.isdir(self.default_config_folder):
            self.gather_default_configs(self.default_config_folder)
        else:
            logger.info(f'not found default config folder in {self.default_config_folder}')
        self.consoleMode = str(console).lower()
        self.engine_logs = []
        self._set_vaya_config()
        self.generate_properties()

    @staticmethod
    def get_instance():
        return VayaDrive.__INSTANCE
    def generate_properties(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with open(f'{here}/configurations/vayadrive_params.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for sec, options in data.items():
                for attr_name, option in options.items():
                    # setattr(VayaDrive, attr_name, None)
                    try:
                        if not hasattr(self, attr_name):
                            setattr(VayaDrive, attr_name, property(self.get_func(sec, option),
                                                                   self.set_func(sec, option)))
                    except KeyError as e:
                        logger.info(f'Unable to set attribute {attr_name}')

    # """
    # create GLOBAL TAB get and set functions
    # """
    def get_func(self, section, option):
        def getf(self):

            if 'SensorEnable' in option and self.configuration['Pipe-0']['SENSORS_BY_INDEX_Bool'].value == 'false':
                if not os.path.isdir(self.configuration['Global']['InputLocation'].value):
                    raise AttributeError(f'input location is invalid')
                input_location = self.configuration['Global']['InputLocation'].value
                parent_dir = os.path.join(input_location, os.parendir)
                calib_folder = os.path.join(parent_dir, 'Calibration')
                sensors_xml_file = os.path.join(input_location, 'recorded_sensors.xml')
                if not os.path.isfile(sensors_xml_file):
                    sensors_xml_file = os.path.join(calib_folder, 'sensors.xml')
                    if not os.path.isfile(sensors_xml_file):
                        raise FileNotFoundError('recorded_sensors.xml file not found ')
                loadDataSensors, loadIndexSensors = self.loadConf(sensors_xml_file)
                if option.split('_')[-2].isdigit():
                    sensor,  index = option.split('_')[-3:-1]
                else:
                    sensor, index = option.split('_')[-2], ""
                    return self.configuration['Pipe-0'][f'SENSORS__Table_{sensor}'].value

                sensors_data = loadDataSensors[f'{sensor.lower()}']
                try:
                    sensor_index = loadIndexSensors[f'{sensor.lower()}'].index(index)
                except ValueError as e:
                    return '-1'
                sensor_name = f"{sensors_data[sensor_index]['name']}_{sensors_data[sensor_index]['position']}"
                try:
                    return self.configuration['Pipe-0'][f'SENSORS__Table_{sensor_name}'].value
                except KeyError as e:
                    return '-1'
            else:
                try:
                    return self.configuration[section][option].value
                except KeyError as e:
                    return ''

        return getf

    def set_func(self, section, option):
        def setf(self, value):
            if 'SensorEnable' in option and self.configuration['Pipe-0']['SENSORS_BY_INDEX_Bool'].value == 'false':
                if not os.path.isdir(self.configuration['Global']['InputLocation'].value):
                    raise AttributeError(f'input location is invalid')
                input_location = self.configuration['Global']['InputLocation'].value
                parent_dir = os.path.join(input_location, os.pardir)
                calib_folder = os.path.join(parent_dir, 'Calibration')
                sensors_xml_file = os.path.join(input_location, 'recorded_sensors.xml')
                if not os.path.isfile(sensors_xml_file):
                    sensors_xml_file = os.path.join(calib_folder, 'sensors.xml')
                    if not os.path.isfile(sensors_xml_file):
                        raise FileNotFoundError('recorded_sensors.xml file not found ')
                loadDataSensors, loadIndexSensors = self.loadConf(sensors_xml_file)

                if option.split('_')[-2].isdigit():
                    sensor,  index = option.split('_')[-3:-1]
                else:
                    sensor, index = option.split('_')[-2], ""
                    sensors_names = {'CANBUS': 'Canbus','IMU': 'IMU','GPS': 'GPS'}
                    option_ = f'SENSORS__Table_{sensors_names[sensor]}'
                    self.set_explicit_param(section=section, option=option_, value=value)
                    return
                # sensor,  index = option.split('_')[-3:-1]
                sensors_data = loadDataSensors[f'{sensor.lower()}']
                try:
                    sensor_index = loadIndexSensors[f'{sensor.lower()}'].index(index)
                except ValueError as e:
                    return
                sensor_name = f"{sensors_data[sensor_index]['name']}_{sensors_data[sensor_index]['position']}"
                option_ = f'SENSORS__Table_{sensor_name}'
                self.set_explicit_param(section=section, option=option_, value=value)
            else:
                self.set_explicit_param(section=section, option=option, value=value)
        return setf

    @property
    def seq_output_folder(self):
        return self._seq_output_folder

    @seq_output_folder.setter
    def seq_output_folder(self, value):
        self._seq_output_folder = value

    @property
    def consoleMode(self):
        return self._consoleMode

    @consoleMode.setter
    def consoleMode(self, value):
        if str(value).lower() == 'true':
            self._consoleMode = self.VDCONSOLE
        else:
            self._consoleMode = self.VD
        logger.info(f'vayadrive console mode = {self._consoleMode}')
        self.set_exe_path(self.vaya_dir_path)

    # @osPath
    def record_mode(self, calib_folder, output_folder):
        self.runningMode = '7'
        self.createFrames = 'false'
        self.recordToDisk = 'true'
        self.defaultCalibFolderString = calib_folder
        self.recordLocationString = output_folder

    # @osPath
    def live_mode(self, calib_folder, output_folder):
        self.runningMode = '7'
        self.createFrames = 'true'
        self.recordToDisk = 'false'
        self.defaultCalibFolderString = calib_folder
        self.recordLocationString = output_folder

    def playback_mode(self):
        self.runningMode = '5'

    def gather_default_configs(self, default_config):

        for file in os.listdir(default_config):
            file_path = os.path.join(default_config, file)
            if os.path.isdir(file_path):
                self.gather_default_configs(file_path)
            elif file.endswith(r'.ini'):
                self.default_config_paths[os.path.splitext(file)[0]] = file_path

    def set_explicit_param(self, **kwargs):
        sec = kwargs.pop('section')
        option = kwargs.pop('option')
        value = kwargs.pop('value')
        if sec not in self.configuration.keys():
            section = Section(sec)
            self.configuration[sec] = section
        if option not in self.configuration[sec].keys():
            self.configuration[sec].add_option(option)
        if type(value) is bool:
            value = str(value).lower()
        self.configuration[sec][option].value = str(value)

    # @osPath
    def find_vd_exe_path(self, path, exe):
        for (root, dirs, files) in os.walk(path, topdown=True):
            if exe in files:
                return os.path.join(root, exe)
        else:
            raise FileNotFoundError(f"couldn't find VayaDrive exe file")

    # @osPath
    def set_exe_path(self, root_path):
        if os.name == 'nt':
            posix = '.exe'
            build_folder = 'build_vs2019' if not self.consoleMode else 'build_console_vs2019'
        else:
            posix = ''
            build_folder = 'build_Release' if not self.consoleMode else 'build_console_Release'

        if self.consoleMode:
            exe = f'VayaDriveConsole{posix}'
        else:
            exe = f"VayaDrive{posix}"
        exe_path = os.path.join(root_path, build_folder, 'Release', exe)
        if os.path.isfile(exe_path):
            self.exe_path = exe_path
            return
        else:
            self.exe_path = self.find_vd_exe_path(root_path, exe)

    def _set_vaya_config(self):
        logger.info(f'Set default configuration')
        if self.configuration:
            # self.configuration = {}
            logger.info(f'Default configuration exist')
            return
        self.run_vayadrive(nogui=True, export_full_ini=True, autostart=True)
        config = configparser.ConfigParser()
        config.optionxform = str
        with open(self.temp_ini_file_path, "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                raise VayaException('Unable to dump configuration')
        with open(self.temp_ini_file_path, "w") as f:
            for line in lines:
                if any([word in line for word in ['DefaultValue','Units', ' ', '%']]):
                    continue
                else:
                    f.write(line)

        config.read(self.temp_ini_file_path)
        for sec in config.sections():

            section = Section(sec)
            for option in config[sec]:
                section.add_option(option)
                try:
                    section[option].value = config.get(sec, option)
                except Exception as e:
                    raise VayaException(f'Get an exception \n{e}')
                self.configuration[sec] = section
        if not 'SENSORS_BY_INDEX_Bool' in self.configuration['Pipe-0'].keys():
            self.set_explicit_param(section='Pipe-0', option='SENSORS_BY_INDEX_Bool', value='true')
        # self.b_configuration = copy.deepcopy(self.configuration)
        VayaDrive._CONFIGURATION_TREE[self.vaya_dir_path] = copy.deepcopy(self.configuration)
        self.process_output = []
        self.seq_output_folder = ''

    @osPath
    def set_configuration_with_ini(self, ini_path, reset=False):
        if reset:
            self.reset()
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(ini_path)
        for sec in config.sections():
            for option in config[sec]:
                if sec not in self.configuration.keys():
                    section = Section(sec)
                    self.configuration[sec] = section
                if option not in self.configuration[sec].keys():
                    self.configuration[sec].add_option(option)
                self.configuration[sec][option].value = config.get(sec, option)

    def export_ini_file(self):

        config = configparser.ConfigParser()
        config.optionxform = str
        for name, sec in self.configuration.items():
            config[name] = sec
        with open(self.temp_ini_file_path, 'w') as configfile:
            config.write(configfile)
        # self.update_local_ini()

    def create_local_ini(self):

        config = configparser.ConfigParser()
        config.optionxform = str
        output_location = self.outputLocation
        record_location = self.recordLocationString
        default_calib_folder = self.defaultCalibFolderString
        config['Global'] = {'OutputLocation': output_location}
        config['Reader-Sensors'] = {'RECORD_LOCATION_String': record_location,
                                    'DEFAULT_CALIB_FOLDER_String': default_calib_folder}
        with open(self.local_ini_path, 'w') as local_ini:
            config.write(local_ini)

    def update_local_ini(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        try:
            output_location = self.outputLocation
            record_location = self.recordLocationString
            default_calib_folder = self.defaultCalibFolderString
        except AttributeError:
            output_location = './output'
            record_location = ''
            default_calib_folder = ''
        config['Global'] = {'OutputLocation': output_location}
        config['Reader-Sensors'] = {'RECORD_LOCATION_String': record_location,
                                    'DEFAULT_CALIB_FOLDER_String': default_calib_folder}
        with open(self.local_ini_path, 'w') as local_ini:
            config.write(local_ini)

    def run_vayadrive(self, nogui=False, autostart=False, get_process=False, export_full_ini=False, force_run=False,
                      qt=False, preset=False, o_params=None, non_blocking_mode=False, timeout=0, update_local=True):
        if o_params is None:
            o_params = []
        self.playback_done = False
        self.seq_output_folder = ''
        self.export_ini_file()
        if update_local:
            self.update_local_ini()
        call_list = [self.exe_path]
        if nogui:
            call_list.append('-nogui')
        if autostart:
            call_list.append('-autostart')
        if preset:
            call_list.append(f'-p{self.temp_ini_file_path}')
        else:
            call_list.append(f'-c{self.temp_ini_file_path}')
        if o_params:
            call_list += o_params
        if export_full_ini:
            call_list.append(f'-d')

        env = dict(os.environ)
        if not self.compiled:
            if os.name == 'posix':  # LINUX
                dependencies = self.extract_dependencies_linux()
                dependencies = dependencies
                try:
                    ld_library_path = env['LD_LIBRARY_PATH']
                    env['LD_LIBRARY_PATH'] = dependencies + ld_library_path
                except:
                    env['LD_LIBRARY_PATH'] = dependencies
            elif os.name == 'nt':  # WINDOWS
                dependencies = self.extract_dependencies_windows()
                win_path = env['PATH']
                env['PATH'] = dependencies + win_path
        if qt:
            return {'call_list': call_list, 'env': env, 'cwd': self.vaya_dir_path}
        self.vayadrive_process = Popen(call_list, cwd=self.vaya_dir_path, env=env,  stdout=PIPE, stderr=STDOUT)
        if get_process and not non_blocking_mode:
            return self.vayadrive_process
        if non_blocking_mode:
            self.log_catcher_thread = threading.Thread(target=self.catch_log, args=(export_full_ini, force_run))
            self.log_catcher_thread.start()
            if get_process:
                return self.vayadrive_process
        else:
            if timeout:
                self.timeout_thread = threading.Thread(target=self.timeout_handler, args=(timeout, ))
                self.timeout_thread.start()
            self.catch_log(export_full_ini, force_run)

    def catch_log(self, export_full_ini, force_run):
        self.process_output = []
        self.exceptions_bucket = queue.Queue()
        while self.vayadrive_process.poll() is None:
            output = self.vayadrive_process.stdout.readline().decode('utf-8')
            self.process_output.append(output)
            # sys.stdout.write(output)
            if 'ERROR' in output and not force_run:
                if self.check_ignore_list(output):
                    continue
                self.vayadrive_process.kill()
                if not export_full_ini:
                    self.exceptions_bucket.put('Exception')  # handle exceptions while catch log is running by thread
                    raise VayaException(f'Found error in VD log\n{output}')
            if 'Shutting down system' in output:
                self.playback_done = True
            if 'Loading engine' in output:
                self.engine_logs.append(output)
            if 'Output folder created:' in output:
                self.seq_output_folder = output.split()[-1]
            if 'getUnits: CanBus units used' in output:
                self.can_bus_selected_units = output.split()[-1]
            if 'Pause: 1' in output:
                self.is_paused = True
            elif 'Pause: 0' in output:
                self.is_paused = False
            if not self.version and 'Version' in output:
                output = output.replace('\r', '')
                output = output.replace('\n', '')
                self.version = output.split('Version: ')[-1]

    def check_ignore_list(self, log_error) -> bool:
        for ignored_error in self.ignore_list:
            if ignored_error in log_error:
                return True
        return False

    def timeout_handler(self, timeout):
        target_timeout = time.time() + timeout
        while time.time() <= target_timeout:
            pass
        self.vayadrive_process.kill()

    def loadConf(self, fileName):
        root = ET.parse(fileName).getroot()
        loadDataSensors = {}
        loadIndexSensors = {}
        for child in root:
            sensor = child.tag.rstrip(string.digits)
            loadDataSensors[sensor] = []
            loadIndexSensors[sensor] = []
        for child in root:
            sensorindex = ""
            lastChar = child.tag[len(child.tag) - 1]
            if lastChar.isdigit():
                sensorindex = lastChar
            sensor = child.tag.rstrip(string.digits)
            loadDataSensors[sensor].append(child.attrib)
            loadIndexSensors[sensor].append(sensorindex)
        return [loadDataSensors, loadIndexSensors]
    def enabled_cameras(self):
        if self.configuration['Pipe-0']['SENSORS_BY_INDEX_Bool'].value == 'true':
            for name, option in self.configuration['Pipe-0'].items():
                if 'sensorenable_camera' in name.lower() and option.value == 'true':
                    yield option.name.split('_')[2]
        else:
            if not os.path.isdir(self.inputLocation):
                raise AttributeError(f'input location is invalid')
            parent_dir = os.path.join(self.inputLocation, os.pardir)
            calib_folder = os.path.join(parent_dir, 'Calibration')
            sensors_xml_file = os.path.join(self.inputLocation, 'recorded_sensors.xml')
            if not os.path.isfile(sensors_xml_file):
                sensors_xml_file = os.path.join(calib_folder, 'sensors.xml')
                if not os.path.isfile(sensors_xml_file):
                    raise FileNotFoundError('recorded_sensors.xml file not found ')
            loadDataSensors, loadIndexSensors = self.loadConf(sensors_xml_file)
            camera_date = loadDataSensors['camera']
            camera_index = loadIndexSensors['camera']
            for i, sensor in enumerate(camera_date):
                sensor_name = f'{sensor["name"]}_{sensor["position"]}'
                try:
                    if self.configuration['Pipe-0'][f'SENSORS__Table_{sensor_name}'].value == 'true':
                        yield camera_index[i]
                except KeyError as e:
                    pass
    def enabled_radars(self):
        if self.configuration['Pipe-0']['SENSORS_BY_INDEX_Bool'].value == 'true':
            for name, option in self.configuration['Pipe-0'].items():
                if 'sensorenable_radar' in name.lower() and option.value == 'true':
                    yield option.name.split('_')[2]
        else:
            if not os.path.isdir(self.inputLocation):
                raise AttributeError(f'input location is invalid')
            parent_dir = os.path.join(self.inputLocation, os.pardir)
            calib_folder = os.path.join(parent_dir, 'Calibration')
            sensors_xml_file = os.path.join(self.inputLocation, 'recorded_sensors.xml')
            if not os.path.isfile(sensors_xml_file):
                sensors_xml_file = os.path.join(calib_folder, 'sensors.xml')
                if not os.path.isfile(sensors_xml_file):
                    raise FileNotFoundError('recorded_sensors.xml file not found ')
            loadDataSensors, loadIndexSensors = self.loadConf(sensors_xml_file)
            radars_date = loadDataSensors['radar']
            radars_index = loadIndexSensors['radar']
            for i, sensor in enumerate(radars_date):
                sensor_name = f'{sensor["name"]}_{sensor["position"]}'
                try:
                    if self.configuration['Pipe-0'][f'SENSORS__Table_{sensor_name}'].value == 'true':
                        yield radars_index[i]
                except KeyError as e:
                    pass

    def enabled_lidars(self):
        if self.configuration['Pipe-0']['SENSORS_BY_INDEX_Bool'].value == 'true':
            for name, option in self.configuration['Pipe-0'].items():
                if 'sensorenable_lidar' in name.lower() and option.value == 'true':
                    yield option.name.split('_')[2]
        else:
            if not os.path.isdir(self.inputLocation):
                raise AttributeError(f'input location is invalid')
            parent_dir = os.path.join(self.inputLocation, os.pardir)
            calib_folder = os.path.join(parent_dir, 'Calibration')
            sensors_xml_file = os.path.join(self.inputLocation, 'recorded_sensors.xml')
            if not os.path.isfile(sensors_xml_file):
                sensors_xml_file = os.path.join(calib_folder, 'sensors.xml')
                if not os.path.isfile(sensors_xml_file):
                    raise FileNotFoundError('recorded_sensors.xml file not found ')
            loadDataSensors, loadIndexSensors = self.loadConf(sensors_xml_file)
            lidars_date = loadDataSensors['lidar']
            lidars_index = loadIndexSensors['lidar']
            for i, sensor in enumerate(lidars_date):
                sensor_name = f'{sensor["name"]}_{sensor["position"]}'
                try:
                    if self.configuration['Pipe-0'][f'SENSORS__Table_{sensor_name}'].value:
                        yield lidars_index[i]
                except KeyError as e:
                    pass

    def delete_temp_ini(self):
        if os.path.isfile(self.temp_ini_file_path):
            os.remove(self.temp_ini_file_path)

    def extract_dependencies_linux(self):
        run_rel_sh = os.path.join(self.vaya_dir_path, 'cmake_vv_scripts', 'cmake_run_release.sh')
        if os.path.isfile(run_rel_sh):
            run_sh = run_rel_sh
        elif self.consoleMode:
            run_sh = os.path.join(self.vaya_dir_path, 'cmake_vv_scripts', 'cmake_run_console_unix.sh')
        else:
            run_sh = os.path.join(self.vaya_dir_path, 'cmake_vv_scripts', 'cmake_run_unix.sh')
        depends = ''
        with open(run_sh, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\\', '')
                line = line.replace(':', '')
                if 'EXPORT' in line and line.index('EXPORT') == 0:
                    depends += line.split('=')[1][:-1] + ':'
                elif '..' in line and line.index('..') == 0:

                    depends += line + ':'
        depends += f'../Libs/PCL/PCL-1.8.1/lib/ubuntu1804:'
        return depends

    def extract_dependencies_windows(self):
        run_bat = os.path.join(self.vaya_dir_path, 'cmake_run_vs2019.bat')
        with open(run_bat, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'PATH' in line:
                    return line[9:-7]
        return False

    def turn_off_all_algos(self, pipe: int):
        for key, val in self.configuration[f'Pipe-{pipe}'].items():
            if key.endswith('Bool') and not any(map(key.__contains__, ['Settings', 'SensorEnable', 'SENSORS__Table', 'SENSORS_BY_INDEX_Bool'])):
                val.value = 'false'

    def reset(self):
        self.configuration = copy.deepcopy(VayaDrive._CONFIGURATION_TREE[self.vaya_dir_path])
        self.process_output = []
        self.log_catcher_thread = None
        self.timeout_thread = None
        self.exceptions_bucket = None
        self.version = None
        self.is_paused = False
        self.can_bus_selected_units = None
        self.playback_done = False
        self.ignore_list = []
        self.seq_output_folder = ''
        self.vayadrive_process = None
        self.engine_logs = []
        self.consoleMode = VayaDrive.VD

    def find_version(self, timeout: int = 3):
        """
        :param timeout: how much time to wait for vd version to be extracted from log (seconds)
        :return: version string if found, unknown otherwise
        """
        self.reset()
        self.run_vayadrive(autostart=True, force_run=True)
        timeout_target = time.time() + timeout  # 3 seconds
        while True:
            if time.time() > timeout_target or self.version:
                break

        self.vayadrive_process.kill()
        if not self.version:
            print('SW version details were not found!')
            return 'Unknown'
        return self.version


class VayaException(Exception):
    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__('VayaException has been raised')
