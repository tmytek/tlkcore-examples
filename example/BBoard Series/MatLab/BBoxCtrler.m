classdef BBoxCtrler
    properties
        bbox_library % .net lib
        instance %class instance
        % Value {mustBeNumeric}
    end

    methods
        function obj = BBoxCtrler(api_path)
            try
                %please use the full path name instead of relevant path%
                disp('API path : ' + string(api_path));
                obj.bbox_library = NET.addAssembly(api_path);
                obj.instance = BBoxAPI.BBoxOneAPI();
            catch ex
                disp(ex)
               % ex.ExceptionObject.LoaderExceptions.Get(0).Message
            end

        end

        function releaseInstance(obj)
            delete(obj.instance)
            delete(obj.bbox_library)
        end

        % return device sn list
        function dev_sn = deviceInit(obj, bbox_type_str)
            % a string contains device information
            dev_info = string(obj.instance.ScanningDevice(BBoxAPI.DEV_SCAN_MODE.NORMAL));

            try
                % in order to get, sn, ip, device type
                sn_ip_type = split(dev_info,",");
            catch ex
                disp("[deviceInit] scanning failed")
                disp(ex)
            end

            if strcmp(bbox_type_str, 'BBoxOne') % previous version of BBox
                div = 2
            else % BBox 5G series(One,Lite, Board...)
                div = 3

            end

            % init dev_sn list
            dev_sn = {}
            dev_type = []

            % indicate to device number - 1, if you have multiple devices.
            for idx = 0 : length(sn_ip_type)/div - 1

                dev_sn(end + 1) = {sn_ip_type(idx*div + 1)}; % get sn;

                if div == 2
                    dev_type(end + 1) = 0;
                elseif div == 3 
                    dev_type(end + 1) =  str2double(sn_ip_type((idx + 1)*div));
                end

                if obj.instance.Init(string(dev_sn(end)), dev_type(end), idx) == BBoxAPI.retCode.OK
                   disp("[Init] Device "+ idx + " init done");

                    mode = 0; % [STANDBY:0, Tx:1, Rx:2, SLEEP:3]
                    ret = obj.instance.SwitchTxRxMode(mode, string(dev_sn(end)));
                    if ret ~= BBoxAPI.retCode.OK
                        disp("[Init] Device " + idx + " switch to standby mode failed");
                    end
                else
                   disp("[Init] Device " + idx + " init failed");
                end
            end
        end

        function freq_list = getFrequencyList(obj, dev_sn)
            freq_list = string(obj.instance.getFrequencyList(dev_sn));
        end

        % select one frequency from frequency list
        function ret = setOperatingFreq(obj, dev_sn, freq)
            freq_list = string(obj.instance.getFrequencyList(dev_sn));

            if isempty(find(double(freq_list) == freq)) == 1
                disp('[Error] unsupport frequency')
                pause
            end

            ret = obj.instance.setOperatingFreq(freq, dev_sn);
        end

        function ret = getAAKitList(obj, dev_sn)
            ret = string(obj.instance.getAAKitList(dev_sn));
        end

        function ret = selectAAKit(obj, dev_sn, aakit_name)
            aakit_list = string(obj.instance.getAAKitList(dev_sn));
            if isempty(find((aakit_list) == aakit_name)) == 1
                disp('[Error] unsupport aakit')
                pause
            end
            ret = obj.instance.selectAAKit(aakit_name, dev_sn);
        end

        function ret = setOperationMode(obj, dev_sn, mode)
            ret = obj.instance.SwitchTxRxMode(mode, dev_sn);
        end

        function ret = setChannelGainPhase(obj, dev_sn, board, ch, db, deg)
            ret = obj.instance.setChannelGainPhase(board, ch, db, deg, dev_sn);
        end

        function ret = setBeamAngle(obj, dev_sn, db, theta, phi)
            ret = obj.instance.setBeamAngle(db, theta, phi, dev_sn);
        end
        
        function ret = getDR(obj, dev_sn)
            ret = double(obj.instance.getDR(dev_sn));
        end
    end % end of methods
end % end of class
