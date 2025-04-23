#include "tlkcore_lib.hpp"
#if TMY_FBS
#include "usrp_fbs.hpp"
#endif
#include "common_lib.h"

#include <iostream>
#include <vector>
#include <string.h>

using namespace tlkcore;

// Please assign the SN which you want to control, and they must included in device.conf
const std::vector<std::string> bf_list = {
    "D2252E058-28",
};
const std::vector<std::string> ud_list = {
    //"UD-BD22070012-24",
};

float target_freq = 28.0;

/***********************************************************************
 * Update bema configs to TLKCore for FBS
 * Or, just simple beam steering
 **********************************************************************/
int update_beam_config(tlkcore_lib::tlkcore_ptr service)
{
    for (std::string sn : bf_list) {
#if TMY_FBS
        bool fbs_mode;
        if (service->get_fast_parallel_mode(sn, fbs_mode) < 0)
        {
             printf("[Main] get_fast_parallel_mode: failed\r\n");
             return -1;
        }
        printf("[Main] get_fast_parallel_mode: %d\r\n", fbs_mode);

        if (fbs_mode == false) {
            // Set all beam configs via csv file
            if (service->apply_beam_patterns(sn, target_freq) < 0) {
                printf("[Main] apply_beam_patterns failed\r\n");
                return -1;
            }
        }

#else
        /* A sample to set beam directly */
        rf_mode_t mode = MODE_TX;
        float gain_db = 4;
        int theta = 0;
        int phi = 0;
        printf("[Main] set beam with gain/theta/phi: %.1f/%d/%d\r\n", gain_db, theta, phi);
        service->set_beam_angle(sn, target_freq, mode, gain_db, theta, phi);
#endif
    }
    return 0;
}

#if TMY_FBS
/***********************************************************************
 * Setup BBox to fast parallel mode for fast beam steering
 * Then let usrp process switching beams
 **********************************************************************/
int fpga_conftrol(tlkcore_lib::tlkcore_ptr service, std::string sn)
{
    bool fbs_mode;
    if (service->get_fast_parallel_mode(sn, fbs_mode) != 0)
    {
            printf("[Main] get_fast_parallel_mode: failed\r\n");
            return -1;
    }
    printf("[Main] get_fast_parallel_mode: %d\r\n", fbs_mode);
    if (fbs_mode == false) {
        fbs_mode = true;
        service->set_fast_parallel_mode(sn, fbs_mode, target_freq);
    }

    // Setup UHD for SPI ready, passing usrp instance or create a usrp instance or assign IP create a usrp instance
    // usrp_spi_setup(usrp);

    usrp_spi_setup();

    // std::string usrp_addr = "192.168.100.10";
    // usrp_spi_setup(usrp_addr);

    char buf[64];
#if 1
    // Case1: Manually control UHD to switch beam id by typing beam id
    int beam_id = 0;
    do {
        memset(buf, 0, sizeof(buf));
        printf("Please enter the beam id or quit(\'q\'): ");

        fgets(buf, sizeof(buf), stdin);
        if (buf[0] == 'q') { // Begin with 'q'
            printf("Break and quit loop\r\n");
            break;
        }
        printf("You entered: %s", buf);
        beam_id = atoi(buf);
        if (usrp_select_beam_id(MODE_TX, beam_id) <= 0) {
            continue;
        }
    } while (1);
#else
    // Case2: Auto switching all beams, please DO NOT print any msg after running
    printf("Please press enter to start:");
    fgets(buf, sizeof(buf), stdin);
    int beams[] = {1, 2, 3, 1, 4, 64};
    int length = sizeof(beams)/sizeof(beams[0]);
    for (int i=0; i<length; i++) {
        usrp_select_beam_id(MODE_TX, beams[i]);
    }
#endif

    // Setup BBox back from fast parallel mode
    fbs_mode = false;
    service->set_fast_parallel_mode(sn, fbs_mode, target_freq);
    service->get_fast_parallel_mode(sn, fbs_mode);
    return 0;
}
#endif

int set_ud_freq(tlkcore_lib::tlkcore_ptr service)
{
    // Here is a example we set freq for ALL UD devices
    // PLEASE MODIFY for your purpose
    for (std::string sn : ud_list) {
        if (service->set_ud_freq(sn, 24e6, target_freq*1e6, 4e6) < 0)
        {
            return -1;
        }
    }
    return 0;
}

int tmy_device_control()
{
    printf("[Main] Start controlling\r\n");
#if TMY_FBS
    printf("FBS\r\n");
#else
    printf("beam\r\n");
#endif
    // Please keep this pointer to maintain instance of tlkcore.
    tlkcore_lib::tlkcore_ptr ptr;

    // Make a new tlkcore_lib, you can assign the path to searching tlkcore libraries.
    ptr = tlkcore_lib::make();

    // Please provide the device config file for lib scanning & init
    const std::string path = "config/device.conf";
    if (ptr->scan_init_dev(path) < 0)
    {
        printf("[Main] Scan & init device got failed!\r\n");
        return -1;
    }

    // Set UD example
    if (set_ud_freq(ptr) < 0)
    {
        return -1;
    }
    // Set BBox example
    if (update_beam_config(ptr) < 0)
    {
        return -1;
    }

#if TMY_FBS
    for (std::string sn : bf_list) {
        fpga_conftrol(ptr, sn);
    }
    usrp_free();
#endif

    return 0;
}

int main(int argc, char* argv[])
{
    if (tmy_device_control() < 0)
        printf("[Main] testing failed\r\n");
    else
        printf("[Main] testing end\r\n");
}
