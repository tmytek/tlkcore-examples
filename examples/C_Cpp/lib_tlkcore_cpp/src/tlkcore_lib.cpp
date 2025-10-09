#include "tlkcore_lib.hpp"
#include <iostream>
#include <pybind11/embed.h> // Python interpreter, everything needed for embedding
#include <pybind11/stl.h>   // Handle convertion of py:list...etc

namespace py = pybind11;

using namespace tlkcore;
using namespace std;

// Define const variable for default TLKCore path at the top
const string DEFAULT_TLKCORE_PATH = "../lib";

// Start the interpreter and keep it alive
py::scoped_interpreter guard{};

/***********************************************************************
 * TLKCore Instance Implementation
 **********************************************************************/
class tlkcore_lib_impl : public tlkcore_lib
{
private:
    py::object service;
    py::object RetCode;
    py::object RFMode;
    py::dict dev_config_dict;
    std::map<std::string, py::object> module_info;
    string tlkcore_root = ".";

    int apply_rf(std::string sn, float freq)
    {
        py::dict devs = dev_config_dict["BF_LAYERS"];
        // cout << devs << endl;
        auto config = devs.attr("get")(sn);
        if (config == Py_None) { // equals Python: if config is None:
            cout << "[TLKCore] Not found: " << sn << endl;
            return -1;
        }

        auto ret = service.attr("setOperatingFreq")(sn, freq);
        cout << "[TLKCore] Set freq: " + ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }

        // Fetch aakit list from real files
        py::list aakitList = service.attr("getAAKitList")(sn).attr("RetData");
        cout << aakitList << endl;

        // Force to chhose assigned AAKIT
        py::str aakit = config["AAKIT_NAME"];
        ret = service.attr("selectAAKit")(sn, aakit);
        cout << "[TLKCore] Select AAKit: " << aakit.cast<string>()
                << ", and return: " << ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        return 0;
    }
    /*
     * Add to sys path
     */
    void set_tlkcore_path(const std::string& root)
    {
        tlkcore_root = root;
        // Add to sys path, likes sys.path.insert(0, os.path.abspath(lib_path))
        py::module::import("sys").attr("path").attr("insert")(0, tlkcore_root);
    }
    // py::module get_pymod(const std::string& path)
    // {
    //     string tmp = tlkcore_root + '.' + path;
    //     // string to const char*
    //     return py::module::import(tmp.c_str());
    // }
public:
    /*
     * Constructor for implementation of tlkcore_lib
     */
    tlkcore_lib_impl(const std::string& root)
    {
        printf("[TLKCore] TLKCore lib impl initialization\r\n");

        set_tlkcore_path(root);

        RetCode = py::module::import("tlkcore.TMYPublic").attr("RetCode");
        RFMode = py::module::import("tlkcore.TMYPublic").attr("RFMode");

        // Import TLKCoreService from tlkcore.TLKCoreService then init the instance object
        service  = py::module::import("tlkcore.TLKCoreService").attr("TLKCoreService")();
        printf("[TLKCore] TLKCoreService imported\r\n");

        auto ver = service.attr("queryTLKCoreVer")();
        cout << "[TLKCore] v" + ver.attr("RetData").cast<string>() << endl;
        // printf("%x\r\n", &service);
    }

    int scan_init_dev(const std::string& conf_path) override
    {
        // printf("Config path: %s\r\n", conf_path.c_str());
        cout << "[TLKCore] Config path: " << conf_path << endl;
        py::object config = py::module::import("TMYConfig").attr("TMYConfig")(conf_path);
        dev_config_dict = config.attr("getConfig")();
        cout << "[TLKCore] TMYConfig: " << dev_config_dict << endl;

        cout << "[TLKCore] Calling scanDevices()..." << endl;
        py::object DevInterface = py::module::import("tlkcore.TMYPublic").attr("DevInterface");
        // After TLKCore v1.1.3, we provides multiple interface for scanning,
        // default is "LAN", and you can set to "ALL" for other TMY products.
        auto ret = service.attr("scanDevices")(); //(DevInterface.attr("ALL"));
        if (ret.attr("RetCode").attr("value").cast<int>() != RetCode.attr("OK").attr("value").cast<int>()) {
            cout << "[TLKCore] Init failed: " + ret.attr("RetMsg").cast<string>() << endl;
            printf("Called scanDevices() failed\r\n");
            return -1;
        }
        // printf("Called scan()\r\n");

        // Get result with str list
        py::list scanlist = ret.attr("RetData");
        cout << "[TLKCore] Scanned " << scanlist << endl;
        for (auto scan_result : scanlist) {
            py::list array = scan_result.attr("rstrip")('\x00').attr("split")(',');
            string sn = array[0].cast<string>();
            py::str ip = array[1].cast<string>();
            auto devtype_str = array[2].cast<string>();
            int devtype = std::stoi(devtype_str);
            cout << "[TLKCore] Checking " << sn << endl;

            py::dict devs;
            // cout << devtype << endl;
            if (devtype == 15) {
                devs = dev_config_dict["UD_LAYERS"];
            } else if (devtype == 28) {
                devs = dev_config_dict["RIS_LAYERS"];

                // Update scanned info into file.
                auto it = devs.begin();
                if (it != devs.end()) {
                    std::string old_key = py::str(it->first);
                    py::object old_value = py::reinterpret_borrow<py::object>(it->second);

                    devs.attr("pop")(old_key);

                    devs[sn.c_str()] = old_value;

                    py::module json = py::module_::import("json");
                    py::module builtins = py::module_::import("builtins");

                    py::object open_fn = builtins.attr("open");
                    py::object wfile = open_fn(conf_path, "w");
                    json.attr("dump")(dev_config_dict, wfile, py::arg("indent") = 4);
                    wfile.attr("close")();
                }
            } else {
                devs = dev_config_dict["BF_LAYERS"];
            }
            auto config = devs.attr("get")(sn);
            if (config == Py_None) { // equals Python: if config is None:
                cout << "[TLKCore] Not found: " << sn << "in the config file" << endl;
                continue;
            }
            // cout << config << endl;

            auto ret = service.attr("initDev")(sn);
            if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
                cout << "[TLKCore] Init failed: " + ret.attr("RetMsg").cast<string>() << endl;
                return -1;
            }
            cout << "[TLKCore] Inited " << sn << " done" << endl;

            // After init
            if (devtype == 15) {
                set_ud_state(sn);
            }
        }
        return 0;
    }

    int set_beam_angle(const std::string& sn, float freq, rf_mode_t mode, float gain_db, int theta, int phi) override
    {
        cout << "[TLKCore] Set custom beams to BBox: " << sn << endl;
        if (apply_rf(sn, freq) < 0)
            return -1;

        auto ret = service.attr("setRFMode")(sn, (int)mode);
        cout << "[TLKCore] SetRFMode: " + ret.attr("__str__")().cast<string>() << endl;

        py::list rng = service.attr("getDR")(sn, (int)mode).attr("RetData");
        // float max_gain = rng[1].cast<float>();
        cout << "[TLKCore] DR: " << rng << endl;

        ret = service.attr("setBeamAngle")(sn, gain_db, theta, phi);
        cout << "[TLKCore] Set beam: " + ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        return 0;
    }

    int apply_beam_patterns(const std::string& sn, float freq) override
    {
        cout << "[TLKCore] To apply custom beam config to BBox: " << sn << endl;
        py::dict devs = dev_config_dict["BF_LAYERS"];
        // cout << devs << endl;
        auto config = devs.attr("get")(sn);
        if (config == Py_None) { // equals Python: if config is None:
            cout << "[TLKCore] Not found: " << sn << endl;
            return -1;
        }

        if (apply_rf(sn, freq) < 0)
            return -1;

        py::str config_path = config["BEAM_CONFIG"];
        cout << "[TLKCore] Fetch custom beam config: "  << config_path << endl;

        py::object obj = py::module::import("tlkcore.TMYBeamConfig").attr("TMYBeamConfig")(sn, service, config_path);
        py::dict beam_config_dict = obj.attr("getConfig")();
        cout << "[TLKCore] TMYBeamConfig: " << beam_config_dict << endl;

        auto success = obj.attr("applyBeams")();
        if (py::str(success).is(py::str(Py_False)))
            return -1;

        cout << "[TLKCore] Apply TMYBeamConfig successfully" << endl;
        return 0;
    }

    int get_fast_parallel_mode(const std::string& sn, bool& enable) override
    {
        auto ret = service.attr("getFastParallelMode")(sn);
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        string mode = ret.attr("__str__")().cast<string>();
        cout << "[TLKCore] Get BBox fast parallel mode: " << mode  << endl;
        if (mode == "True") {
            enable = true;
        } else
            enable = false;
        return 0;
    }

    /*
     * Enable to set BBox as fast parallel mode and external SPI input with assigned center frequency
    */
    int set_fast_parallel_mode(const std::string& sn, bool& enable, float freq) override
    {
        // string TRUE = "true";
        if (enable == 1 && apply_rf(sn, freq) < 0) {
            cout << "[TLKCore] Invalid freq: " << freq << endl;
            return -1;
        }
        auto ret = service.attr("setFastParallelMode")(sn, enable);
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        cout << "[TLKCore] Set BBox fast parallel mode: " << enable << endl;
        return 0;
    }

    /**
     * Set UD state only
     */
    int set_ud_state(const std::string& sn) override
    {
        auto ret = service.attr("getUDState")(sn);
        cout << "[TLKCore] Get UD states: " << ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }

        py::dict devs = dev_config_dict["UD_LAYERS"];
        // cout << devs << endl;
        auto config = devs.attr("get")(sn);
        if (config == Py_None) { // equals Python: if config is None:
            cout << "[TLKCore] Not found: " << sn << endl;
            return -1;
        }
        py::dict states = config["STATE"];
        ret = service.attr("setUDState")(sn, states);
        cout << "[TLKCore] Apply UD states from config: " << ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        return 0;
    }

    int set_ud_freq(const std::string& sn, int freq_ud_khz, int freq_rf_khz, int freq_if_khz) override
    {
        cout << "[TLKCore] To set UD freq " << freq_ud_khz << endl;
        auto ret = service.attr("setUDFreq")(sn, freq_ud_khz, freq_rf_khz, freq_if_khz);
        string msg = "[TLKCore] Set UD freq: ";
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            cout << msg << ret.attr("__str__")().cast<string>() << endl;
            return -1;
        }
        // pass case
        string harmonic_warn = ret.attr("__str__")().cast<string>();
        if (harmonic_warn == "True") {
            msg += "OK with harmonic warning";
        } else {
            msg += "OK";
        }
        cout << msg << endl;
        return 0;
    }

    /**
     * Check for harmonic interference in the specified frequency configuration
     * @param sn Serial number of the device
     * @param freq_ud Up/Down frequency in kHz
     * @param freq_if IF frequency in kHz
     * @param freq_bw Signal bandwidth in kHz
     * @return 0: No harmonic detected, 1: Harmonic warning, -1: Error occurred
     */
    int get_harmonic(const std::string& sn, int freq_ud, int freq_if, int freq_bw) override
    {
        // Call Python service method to check harmonic
        auto ret = service.attr("getHarmonic")(sn, freq_ud, freq_if, freq_bw);
        cout << "[TLKCore] Check harmonic: " << ret.attr("__str__")().cast<string>() << endl;

        // Check if the operation was successful
        if (!ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1; // Return error code
        }

        // Extract harmonic detection result from return data
        bool has_harmonic = ret.attr("RetData").cast<bool>();
        if (has_harmonic) {
            cout << "[TLKCore] WARNING: Harmonic detected!" << endl;
            return 1; // Return warning code indicating harmonic presence
        }

        return 0; // Return success code - no harmonic detected
    }

    int get_ris_module_info(const std::string &sn) override
    {
        auto ret = service.attr("getRISModuleInfo")(sn);
        cout << "[TLKCore] Get RIS module info: " << ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }

        py::dict dict_ret = ret.attr("RetData");

        for (auto it = dict_ret.begin(); it != dict_ret.end(); ++it) {
            std::string port = py::str(it->first);
            py::object info = py::reinterpret_borrow<py::object>(it->second);

            module_info[port] = info;
        }
        // for (const auto& [port, info] : module_info) {
        //     std::cout << "port = " << port << ", info = " << py::str(info) << std::endl;
        // }
        return 0;
    }

    int get_ris_pattern(const std::string &sn) override
    {
        std::vector<std::string> ports;
        for (auto item : module_info) {
            std::string port = py::str(item.first);
            ports.push_back(port);
        }
        auto ret = service.attr("getRISPattern")(sn, ports);
        cout << "[TLKCore] Get RIS pattern: "
                    << ret.attr("__str__")().cast<string>() << endl;
        if (! ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        return 0;
    }

    int set_ris_angle(const std::string &sn) override
    {
        py::dict devs = dev_config_dict["RIS_LAYERS"];
        auto device_config = devs.attr("get")(sn);

        device_config["sn"] = sn;
        py::object ret = service.attr("setRISAngle")(**device_config);
        cout << "[TLKCore] Set RIS angle: "
                    << py::str(ret) << endl;

        if (!ret.attr("RetCode").equal(RetCode.attr("OK"))) {
            return -1;
        }
        return 0;
    }
};

tlkcore_lib::~tlkcore_lib(void)
{
    /* NOP */
}

/***********************************************************************
 * The Make Function
 **********************************************************************/
tlkcore_lib::tlkcore_ptr tlkcore_lib::make(const std::string& lib_path)
{
    printf("[TLKCore] Making TLKCore instance\r\n");
    // return std::make_shared<tlkcore_lib_impl>();
    return shared_ptr<tlkcore_lib_impl>(new tlkcore_lib_impl(lib_path));
}
tlkcore_lib::tlkcore_ptr tlkcore_lib::make()
{
    return tlkcore_lib::make(DEFAULT_TLKCORE_PATH);
}

int main()
{
    printf("[Main] testing\r\n");
    tlkcore_lib::tlkcore_ptr ptr;
    ptr = tlkcore_lib::make();
    return 0;
}
