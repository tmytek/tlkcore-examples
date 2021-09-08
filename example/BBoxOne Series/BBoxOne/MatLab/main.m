%main.m function for use BBoxCtrler class

disp('Please make sure you put the correct dll path in constructor')
bbox_ctrl = BBoxCtrler('.\\BBoxAPI.dll');


bbox_type = 'BBoxOne'
sn_list = deviceInit(bbox_ctrl, bbox_type);

% assume single device
sn = string(sn_list(1))

if setOperatingFreq(bbox_ctrl, sn, 28) ~= BBoxAPI.retCode.OK
    disp('[setOperatingFreq] failed')
end

aakit_list = getAAKitList(bbox_ctrl, sn);
disp('[getAAKitList] aakit_list : ' + aakit_list)

if selectAAKit(bbox_ctrl, sn, "TMYTEK-4x4_NONE") ~= BBoxAPI.retCode.OK
    disp('[selectAAKit] failed')
    exit
end


if setOperationMode(bbox_ctrl, sn, 1) ~= BBoxAPI.retCode.OK
    disp('[setoperationMode] failed')
end

db = 10;
theta = 0;
phi = 0;


% broadside direction
if setBeamAngle(bbox_ctrl, sn, db, theta, phi) ~= BBoxAPI.retCode.OK
    disp('[setBeamAngle] failed')
end

brd = 1; %brd th
mode = 1; %Tx
ch = 1; %channel th
db = 10;
deg = 10;

% control single channel gain/phase
ret_str = setChannelGainPhase(bbox_ctrl, sn, brd, ch, db, deg);

disp('[setChannelGainPhase] ' + string(ret_str))

releaseInstance(bbox_ctrl);