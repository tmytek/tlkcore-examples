import csv
import logging
import os

from tlkcore.TMYPublic import RetCode, RFMode, BeamType

logger = logging.getLogger("TMYBeamConfig")

class TMYBeamConfig():
    def __init__(self, sn, service, path="CustomBatchBeams.csv"):
        """
            Test for parsing batch beam configs then apply it,
            please edit gains to feet available gain range for your BBox
        """
        self.__sn = sn
        self.__service = service
        self.__config = None
        if not os.path.exists(path):
            logger.error("Not exist: %s" %path)
            return
        self.__config = self.__parse(path)

    def __parse(self, path):
        logger.info("Start to parsing...")
        try:
            aakit_selected = True if self.__service.getAAKitInfo(self.__sn).RetCode is RetCode.OK else False
            logger.info("[AppyBatchBeams] AAKit %sselected" %"" if aakit_selected else "NOT ")

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
                    if not aakit_selected:
                        logger.warning("PhiA mode not support whole beam config -> skip")
                        continue
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
            logger.info("[CustomCSV] " + str(custom))
            return custom
        except:
            logger.exception("Something wrong while parsing")
            return None

    def getConfig(self):
        if self.__config is None:
            return None
        return self.__config

    def applyBeams(self):
        try:
            if self.__service is None:
                logger.error("service is None")
                return False
            if self.__config is None:
                logger.error("Beam config is empty!")
                return False

            service = self.__service
            sn = self.__sn
            custom = self.__config

            channel_count = service.getChannelCount(sn).RetData
            dr = service.getDR(sn).RetData
            com_dr = service.getCOMDR(sn).RetData
            # print(com_dr)
            ele_dr_limit = service.getELEDR(sn).RetData
            # print(ele_dr_limit)

            # Get Beam then update custom beam
            for mode_name in [*custom]:
                mode = getattr(RFMode, mode_name)
                # print(mode)
                for id in [*custom[mode_name]]:
                    beamID = int(id)
                    ret = service.getBeamPattern(sn, mode, beamID)
                    beam = ret.RetData
                    logger.debug("Get [%s]BeamID %02d info: %s" %(mode_name, beamID, beam))

                    beam_type = BeamType(custom[mode_name][str(beamID)]['beam_type'])
                    value = custom[mode_name][str(beamID)]['config']
                    logger.info("Get [%s]BeamID %02d custom: %s" %(mode_name, beamID, value))

                    if beam_type is BeamType.BEAM:
                        if beam['beam_type'] != beam_type.value:
                            # Construct a new config
                            beam = {'beam_config': {'db': dr[mode.name][1], 'theta': 0, 'phi':0 }}
                        config = beam['beam_config']
                        if len(value[0]) > 0:
                            config['db'] = float(value[0])
                        if len(value[1]) > 0:
                            config['theta'] = int(value[1])
                        if len(value[2]) > 0:
                            config['phi'] = int(value[2])
                    else: #CHANNEL
                        if beam['beam_type'] != beam_type.value:
                            # Construct a new config
                            beam = {'channel_config': {}}
                            for ch in range(1, channel_count+1):
                                if ch%4 == 1: # 4 channels in one board
                                    # First channel in board: construct brd_cfg
                                    board = int(ch/4) + 1
                                    brd_cfg = {}
                                    # Use MAX COMDR - will check with assign gain to adjust
                                    brd_cfg['common_db'] = com_dr[mode.value][board-1][1]
                                ch_cfg = {
                                    'sw': 0,
                                    # Use MAX ELEDR
                                    'db': ele_dr_limit[mode.value][board-1],
                                    'deg': 0
                                }
                                brd_cfg['channel_'+str((ch-1)%4 + 1)] = ch_cfg
                                if ch%4 == 0:
                                    beam['channel_config'].update({'board_'+str(board): brd_cfg})

                        config = beam['channel_config']

                        # Update each channel
                        for ch_str, ch_value in value.items():
                            ch = int(ch_str)
                            if ch > channel_count:
                                logger.error("[%s]BeamID %02d - Invalid ch_%s exceeds %d channels! -> skip it"
                                            %(mode_name, beamID, ch, channel_count))
                                return False
                            # logger.debug("Update ch%d info: %s" %(ch, ch_value))
                            board_idx = int((ch-1)/4)
                            board_name = 'board_'+str(board_idx + 1)
                            board_ch = (ch-1)%4 + 1
                            ch_name = 'channel_'+str(board_ch)
                            if len(ch_value[0]) > 0:
                                config[board_name][ch_name]['sw'] = int(ch_value[0])
                            if len(ch_value[1]) > 0:
                                db = float(ch_value[1])
                                ele_gain = db - config[board_name]['common_db']
                                if ele_gain < 0:
                                    logger.warning("Ch_%d changed to db:%.1f < com gain:%.1f, adjust com gain later" %(ch, db, config[board_name]['common_db']))
                                config[board_name][ch_name]['db'] = ele_gain
                            if len(ch_value[2]) > 0:
                                config[board_name][ch_name]['deg'] = int(ch_value[2])
                        logger.debug("Tmp [%s]BeamID %02d custom: %s" %(mode_name, beamID, config))

                        # Simple check each com_gain, ele_gain for board/channel
                        for brd, brd_cfg in config.items():
                            brd_idx = int(brd.replace("board_", ""))-1
                            brd_db = [v['db'] for k, v in brd_cfg.items() if k.startswith("channel_")]
                            # print(brd_db)
                            if max(brd_db) - min(brd_db) > ele_dr_limit[mode.value][board_idx]:
                                logger.error("[%s]BeamID %02d - [%s] Invalid db setting: %s, the max diff of each db field exceeds the limit: %.1f"
                                            %(mode_name, beamID, brd, [d+brd_cfg['common_db'] for d in brd_db], ele_dr_limit[mode.value][board_idx]))
                                return False
                            if min(brd_db) < 0:
                                # Lower the common gain to min db
                                new_com = brd_cfg['common_db'] + min(brd_db)
                                if new_com < com_dr[mode.value][brd_idx][0]:
                                    logger.error("[%s]BeamID %02d - [%s] Invalid common gain: %.1f < min common gain: %.1f, please tune higher the minimal db field"
                                                %(mode_name, beamID, brd, new_com, com_dr[mode.value][brd_idx][0]))
                                    return False
                                logger.info("[%s]BeamID %02d - Adjust [%s]com gain: %.1f -> %.1f, and ele gain: %s -> %s"
                                            %(mode_name, beamID, brd, brd_cfg['common_db'], new_com,
                                            [v['db'] for k, v in brd_cfg.items() if k.startswith("channel_")],
                                            [v['db']-min(brd_db) for k, v in brd_cfg.items() if k.startswith("channel_")]))
                                brd_cfg['common_db'] = new_com
                                for k, v in brd_cfg.items():
                                    if k.startswith("channel_"):
                                        v['db'] -= min(brd_db)
                    logger.info("Set [%s]BeamID %02d info: %s" %(mode_name, beamID, config))
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