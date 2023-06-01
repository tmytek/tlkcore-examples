#include "tlkcore_lib.hpp"
#include <iostream>
#include <pybind11/embed.h> // Python interpreter, everything needed for embedding
#include <pybind11/stl.h>   // Handle convertion of py:list...etc

namespace py = pybind11;

using namespace tlkcore;
using namespace std;

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
public:
    tlkcore_lib_impl()
    {
        printf("[TLKCore] TLKCore lib impl initialization\r\n");

        RetCode = py::module::import("lib.TMYPublic").attr("RetCode");
        RFMode = py::module::import("lib.TMYPublic").attr("RFMode");

        // from lib.TLKCoreService import TLKCoreService then init the instance object
        service  = py::module::import("lib.TLKCoreService").attr("TLKCoreService")();
        printf("[TLKCore] TLKCoreService imported\r\n");

        auto ver = service.attr("queryTLKCoreVer")();
        cout << "[TLKCore] v" + ver.attr("RetData").cast<string>() << endl;
        // printf("%x\r\n", &service);
    }

    int scan_init_dev(const std::string& conf_path) override
    {
        // printf("Config path: %s\r\n", conf_path.c_str());
        cout << "[TLKCore] Config path: " << conf_path << endl;
        py::object config = py::module::import("lib.TMYConfig").attr("TMYConfig")(conf_path);
        dev_config_dict = config.attr("getConfig")();
        cout << "[TLKCore] TMYConfig: " << dev_config_dict << endl;

        cout << "[TLKCore] Calling scanDevices()..." << endl;
        auto ret = service.attr("scanDevices")();
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
            if (devtype == 15) {
                devs = dev_config_dict["UD_LAYERS"];
            } else {
                devs = dev_config_dict["BF_LAYERS"];
            }
            auto config = devs.attr("get")(sn);
            if (config == Py_None) { // equals Python: if config is None:
                cout << "[TLKCore] Not found: " << sn << endl;
                return -1;
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

        py::object obj = py::module::import("lib.TMYBeamConfig").attr("TMYBeamConfig")(config_path);
        py::dict beam_config_dict = obj.attr("getConfig")();
        cout << "[TLKCore] TMYBeamConfig: " << beam_config_dict << endl;

        auto success = obj.attr("apply_beams")(service, sn);
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
};

tlkcore_lib::~tlkcore_lib(void)
{
    /* NOP */
}

/***********************************************************************
 * The Make Function
 **********************************************************************/
tlkcore_lib::tlkcore_ptr tlkcore_lib::make()
{
    printf("[TLKCore] Making TLKCore instance\r\n");
    // return std::make_shared<tlkcore_lib_impl>();
    return shared_ptr<tlkcore_lib_impl>(new tlkcore_lib_impl());
}

int main()
{
    printf("[Main] testing\r\n");
    tlkcore_lib::tlkcore_ptr ptr;
    ptr = tlkcore_lib::make();
    return 0;
}
