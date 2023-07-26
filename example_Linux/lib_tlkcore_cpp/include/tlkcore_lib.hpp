#pragma once

// #include <iostream>
#include <memory>
// using namespace std;

namespace tlkcore {

typedef enum {
    MODE_TX = 0,
    MODE_RX
} rf_mode_t;

class tlkcore_lib
{
public:
    typedef std::shared_ptr<tlkcore_lib> tlkcore_ptr;

    virtual ~tlkcore_lib(void) = 0;

    /*!
     * Make a new multi usrp from the device address.
     * \param dev_addr the device address
     * \return a new single usrp object
     * \throws uhd::key_error no device found
     * \throws uhd::index_error fewer devices found than expected
     */
    static tlkcore_ptr make(void);

    /*! Scan TMY devices then makes sure these devices are in TMY config.
     * \param conf_path the config path.
     * \return the error code.
     */
    virtual int scan_init_dev(const std::string& conf_path) = 0;

    virtual int set_beam_angle(const std::string& sn, float freq, rf_mode_t mode, float gain_db, int theta, int phi) = 0;

    virtual int apply_beam_patterns(const std::string& sn, float freq) = 0;

    virtual int get_fast_parallel_mode(const std::string& sn, bool& enable) = 0;

    virtual int set_fast_parallel_mode(const std::string& sn, bool& enable, float freq) = 0;

    virtual int set_ud_state(const std::string& sn) = 0;

    virtual int set_ud_freq(const std::string& sn, int freq_ud, int freq_rf, int freq_if) = 0;

};

} // namespace tlkcore