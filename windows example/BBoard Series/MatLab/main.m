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


% set operation mode, Standby : 0, Tx : 1, Rx : 2, Sleep : 3
if setOperationMode(bbox_ctrl, sn, 1) ~= BBoxAPI.retCode.OK
    disp('[setoperationMode] failed')
end

brdth = 1
chth = 1
sw = 1 % 1 indicates to power-off, 0 indicates to power-on
if switchChannelPower(bbox_ctrl, sn, brdth, chth, sw) ~= 'OK'
    disp('[switchChannelPower] failed')
end


pause(5)
releaseInstance(bbox_ctrl);