% Setup your Python execution version for MATLAB interface engine (just
% execute it once after MATLAB started), assign the version name to Windows
% registry (Windows Only) or set the full path

terminate(pyenv)
pe = pyenv;
if pe.Status == "NotLoaded"
    disp(" ----- Calling pyenv to check Python environment, and it's NotLoaded -> Start loading(OutOfProcess) -----")

    % PLEASE MODIFY TO YOUR PYTHON VERSION (3.8/3.10/...) HERE
    pyenv(ExecutionMode="OutOfProcess")%, "Version", "3.8")
end
disp(" ----- Calling a simple Pytohn function: py.list to load Python interpreter -----")
py.list
disp(" ----- Calling pyenv to check Python environment -----")
pyenv

% Setup TLKCore lib path
pylibfolder = '.\lib';
if count(py.sys.path, pylibfolder) == 0
    insert(py.sys.path, int64(0), pylibfolder);
end
disp(" ----- Calling py.sys.path to get Python execute sequence -----")
py.sys.path

% Create instance, it finds TLKCoreService class under pylibfolder
tlkcore = py.tlkcore.TLKCoreService.TLKCoreService;
disp("TLKCore version: " + tlkcore.version)

% Scan devices via your main.py calls "scanDevices" function
scan_list = py.main.wrapper("scanDevices");
disp("Scan result:")
disp(scan_list)

% Display system information then init each device to control
for i = 1:length(scan_list)
    s = scan_list{i};
    info = s.strip().split(',');
    SN = info{1};
    addr = info{2};
    dev_type = 0;
    if length(info) == 3
        dev_type = info{3};
    end

    disp(SN)
    disp(addr)
    disp(dev_type)

    % Initial device
    ret = py.main.wrapper("initDev", SN);
    disp(ret)

    % Simple query test
    disp(py.main.wrapper("querySN", SN))
    disp(py.main.wrapper("queryFWVer", SN))
    disp(py.main.wrapper("queryHWVer", SN))

    dev_name = py.main.wrapper("getDevTypeName", SN);
    disp(dev_name)
    if contains(string(dev_name), "BBox")
        dev_name = "BBox";
    end
    try
        % Call MATLAB test function
        func_name = strcat("test", string(dev_name));
        feval(func_name, SN);
    catch
        error("Exception -> de-init device")
    end

    % Remember to de-int device to free memory
    py.main.wrapper("DeInitDev", SN)
end
disp(" ----- Terminate pyenv -----")
terminate(pyenv)

function testBBox(SN)
    disp("Test BBox")

    % Load basic enums
    tmy_public = py.importlib.import_module('tlkcore.TMYPublic');
    RFMode = tmy_public.RFMode;

    % Set TX & 28GHz here as example,
    % please modify for your purpose,
    % and make sure related tables exist.
    mode = RFMode.TX;
    py.main.wrapper("setRFMode", SN, mode)
    py.main.wrapper("setOperatingFreq", SN, 28)
    rng = py.main.wrapper("getDR", SN, mode);
    disp(rng)
    gain_max = rng{2};

    % Please assign a name/pattern to select or not select AAKit to 'PhiA' mode
    aakit_selected = false;
    aakit_pat = "4x4";
    aakitList = py.main.wrapper("getAAKitList", SN, mode);
    disp(aakitList)
    if isempty(aakitList)
        warning("PhiA mode")
    end
    % Check each aakit_name in aakitList meets the seaching pattern
    for i = 1:length(aakitList)
        disp(aakitList{i})
        if contains(string(aakitList{i}), aakit_pat)
            disp("Found")
            aakit_selected = true;
            py.main.wrapper("selectAAKit", SN, aakitList{i})
            break
        end
    end

    % Set beam with degree(theta/phi) and gain
    if aakit_selected == true
        theta = 0;
        phi = 0;
        ret = py.main.wrapper("setBeamAngle", SN, gain_max, theta, phi);
        disp(ret)
    end
end

function testUDBox(SN)
    disp("Test UDBox")

    % Load basic enums
    tmy_public = py.importlib.import_module('tlkcore.TMYPublic');
    UDState = tmy_public.UDState;

    state = py.main.wrapper("getUDState", SN, UDState.PLO_LOCK);
    disp("PLO state:")
    disp(state)
    state = py.main.wrapper("getUDState", SN);
    disp("All state:")
    disp(state)

    disp(py.main.wrapper("setUDState", SN, int32(0), UDState.CH1))
    input("Wait for ch1 off")
    disp(py.main.wrapper("setUDState", SN, int32(1), UDState.CH1))

    disp(py.main.wrapper("setUDState", SN, int32(1), UDState.OUT_10M))
    disp(py.main.wrapper("setUDState", SN, int32(1), UDState.OUT_100M))
    disp(py.main.wrapper("setUDState", SN, int32(1), UDState.PWR_5V))
    disp(py.main.wrapper("setUDState", SN, int32(1), UDState.PWR_9V))
    input("Wait")

    disp("Check harmonic")
    disp(py.main.wrapper("getHarmonic", SN, 24e6, 28e6, 4e6, 100000))

    disp(py.main.wrapper("setUDFreq", SN, 24e6, 28e6, 4e6, 100000))
end
