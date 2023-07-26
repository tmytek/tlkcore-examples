import csv
import logging
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from lib.TMYPublic import RetCode, RFMode, BeamType

logger = logging.getLogger("TMYBeamConfig")

class TMYBeamConfig():
    def __init__(self, path):
        self.__config = None
        if not os.path.exists(path):
            logger.error("Not exist: %s" %path)
            return
        self.__config = self.__parse(path)

    def __parse(self, path):
        logger.info("Start to parsing...")
        try:
            file = open(path)
            reader = csv.reader(_.replace('\x00', '') for _ in file)
            custom = { 'TX': {}, 'RX': {}}
            # Parsing CSV
            for col in reader:
                if len(col) == 0 or len(col[0]) == 0 or col[0] == 'Mode':
                    continue
                # col = line.split(',')
                mode_name = col[0]
                beamID = int(col[1])
                beam_type = BeamType(int(col[2]))

                if beam_type is BeamType.BEAM:
                    # Fetch col 3~5 for db,theta,phi
                    config = [col[i] for i in range(3, 6)]
                else: #CHANNEL
                    ch = int(col[6])
                    # Fetch col 7~9 for sw,db,deg
                    config = {str(ch): [col[i] for i in range(7, 10)]}

                if custom[mode_name].get(str(beamID)) is None:
                    # Create new beam config
                    beam = {'beam_type': beam_type.value, 'config': config}
                    custom[mode_name][str(beamID)] = beam
                else:
                    # If exist, replace or add new channel config into beam config
                    custom[mode_name][str(beamID)]['config'].update(config)
                    # custom[mode_name][str(beamID)].update(beam)

            # Parsing done
            logger.info(custom)
            return custom
        except:
            logger.exception("Something wrong while parsing")
            return None

    def getConfig(self):
        if self.__config is None:
            return None
        return self.__config

    def apply_beams(self, service, sn):
        try:
            if service is None:
                logger.error("service is None")
                return False
            if self.__config is None:
                logger.error("Beam config is empty!")
                return False

            custom = self.__config
            mode = RFMode.TX
            # Get Beam then update custom beam
            for mode_name in [*custom]:
                for m in RFMode:
                    if m.name == mode_name:
                        mode = m
                # print(mode)
                for id in [*custom[mode_name]]:
                    beamID = int(id)
                    ret = service.getBeamPattern(sn, mode, beamID)
                    beam = ret.RetData
                    logger.info("Get [%s]BeamID %d info: %s" %(mode_name, beamID, beam))

                    beam_type = BeamType(custom[mode_name][str(beamID)]['beam_type'])
                    value = custom[mode_name][str(beamID)]['config']
                    if beam_type is BeamType.BEAM:
                        config = beam['beam_config']
                        if len(value[0]) > 0:
                            config['db'] = float(value[0])
                        if len(value[1]) > 0:
                            config['theta'] = int(value[1])
                        if len(value[2]) > 0:
                            config['phi'] = int(value[2])
                    else: #CHANNEL
                        config = beam['channel_config']
                        # Update each channel
                        for ch in [*value]:
                            ch_idx = int(ch) - 1
                            ch_value = value[ch]
                            if len(ch_value[0]) > 0:
                                config[ch_idx]['sw'] = int(ch_value[0])
                            if len(ch_value[1]) > 0:
                                config[ch_idx]['db'] = float(ch_value[1])
                            if len(ch_value[2]) > 0:
                                config[ch_idx]['deg'] = int(ch_value[2])
                    ret = service.setBeamPattern(sn, mode, beamID, beam_type, config)
                    if ret.RetCode is not RetCode.OK:
                        logger.error(ret.RetMsg)
                        return False
        except:
            logger.exception("Something wrong while parsing")
            return False
        logger.info("Apply beam configs to %s successfully" %sn)
        return True

if __name__ == '__main__':
    import logging.config
    if not os.path.isdir('tlk_core_log/'):
        os.mkdir('tlk_core_log/')
    logging.config.fileConfig('logging.conf')
    c = TMYBeamConfig("config/CustomBatchBeams_D2123E001-28.csv")
    # print(c.getConfig())