%main.m function for use BBoxCtrler class

disp('Please make sure you put the correct dll path in constructor')

% BBoxOne, BBoxOne-5G-28, BBoxOne-5G-39, BBoxLite-5G-28, BBoxLite-5G-39, BBoard-5G-28, BBoard-5G-39
% user config --- start ----------------------------------------------------------------------------
lib_path = 'C:\\Program Files\\Polyspace\\R2021a\\bin\\BBoxAPI.dll'
bbox_type = 'BBoard-5G-28'
op_freq = 28
aakit_name = "TMYTEK_28LITE_4x4_A2104L999-28"
% user config --- end ------------------------------------------------------------------------------


bbox_ctrl = BBoxCtrler(lib_path);

sn_list = deviceInit(bbox_ctrl, bbox_type);

% assume single device
sn = string(sn_list(1))
disp('device sn :' + sn)

% set operation frequency
if setOperatingFreq(bbox_ctrl, sn, op_freq) ~= BBoxAPI.retCode.OK
    disp('[setOperatingFreq] failed, please make sure you have correct table with selected operating freqency')
end

% get AAkit list in "files" folder
aakit_list = getAAKitList(bbox_ctrl, sn);
disp('[getAAKitList] aakit_list : ' + aakit_list)

% select AAkit list in "files" folder
if selectAAKit(bbox_ctrl, sn, aakit_name) ~= BBoxAPI.retCode.OK
    disp('[selectAAKit] failed')
    exit
end

% set operation mode, Standby : 0, Tx : 1, Rx : 2, Sleep : 3
if setOperationMode(bbox_ctrl, sn, 1) ~= BBoxAPI.retCode.OK
    disp('[setoperationMode] failed')
end


db = 10;
theta = 0;
phi = 0;


% broadside direction
if setBeamAngle(bbox_ctrl, sn, db, theta, phi) ~= BBoxAPI.retCode.OK
    disp('[setBeamAngle] failed')
else
    disp('[setBeamAngle] successed')
end

brd = 1; %brd th
mode = 1; %Tx
ch = 1; %channel th
db = 10;
dev_dr = getDR(bbox_ctrl, sn);
tx_min = dev_dr(1,1)
tx_max = dev_dr(1,2)
rx_min = dev_dr(2,1)
rx_max = dev_dr(2,2)

% control single channel gain/phase

for db = tx_max:-1:tx_min
    for deg = 0:5:20
        for ch=1:4
            disp('Channel :' +string(ch) +', Gain : ' + string(db) + ', Phase : ' + string(deg))
            ret_str = setChannelGainPhase(bbox_ctrl, sn, brd, ch, db, deg);
            disp('[setChannelGainPhase] ' + string(ret_str))
            pause(1)
        end
    end
end

pause(5)
releaseInstance(bbox_ctrl);