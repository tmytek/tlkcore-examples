#include "tlkcore_lib.hpp"
#include "usrp_fbs.hpp"
#include "common_lib.h"

#include <iostream>
#include <vector>
#include <string.h>

using namespace tlkcore;

int update_beam_config(tlkcore_lib::tlkcore_ptr service)
{
    const std::vector<std::string> bf = {
        "D2252E058-28",
    };

    for (std::string sn : bf) {
        bool fpga_mode;
        service->get_fast_parallel_mode(sn, fpga_mode);
        printf("[Main] get_fast_parallel_mode: %d\r\n", fpga_mode);

        /* A sample to set beam directly */
        rf_mode_t mode = MODE_TX;
        float gain_db = 4;
        int theta = 0;
        int phi = 0;
        service->set_beam_angle(sn, 28.0, mode, gain_db, theta, phi);

        /* Set all beam configs via csv file */
        service->apply_beam_patterns(sn, 28.0);
    }
    return 0;
}

int fpga_conftrol(tlkcore_lib::tlkcore_ptr service)
{
    const std::string sn = "D2252E058-28";

    // Setup BBox as fast parallel mode
    bool fpga_mode;
    service->get_fast_parallel_mode(sn, fpga_mode);
    printf("[Main] get_fast_parallel_mode: %d\r\n", fpga_mode);
    if (fpga_mode == false) {
        fpga_mode = true;
        service->set_fast_parallel_mode(sn, fpga_mode, 28.0);
    }

    // Setup UHD for SPI ready, and assign IP to reduce finding time, and assign "" will takes to scan available usrps
    std::string usrp_addr = "";//"addr=192.168.100.10";
    usrp_spi_setup(usrp_addr);

    // Control UHD to switch beam id
    char buf[64];
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

    // Setup BBox back from fast parallel mode
    fpga_mode = false;
    service->set_fast_parallel_mode(sn, fpga_mode, 28.0);
    service->get_fast_parallel_mode(sn, fpga_mode);
    return 0;
}

int set_ud_freq(tlkcore_lib::tlkcore_ptr service)
{
    const std::vector<std::string> ud = {
        "UD-BD22070012-24",
    };
    for (std::string sn : ud) {
        service->set_ud_freq(sn, 24000000, 28000000, 4000000);
    }
    return 0;
}

int tmy_device_control()
{
    printf("[Main] Start controlling\r\n");
    // Please keep this pointer to maintain instance of tlkcore.
    tlkcore_lib::tlkcore_ptr ptr;

    ptr = tlkcore_lib::make();

    // Please provide the device config file for lib scanning & init
    const std::string path = "config/device.conf";
    ptr->scan_init_dev(path);

    // set_ud_freq(ptr);
    update_beam_config(ptr);
    fpga_conftrol(ptr);
    usrp_free();

    return 0;
}

int main(int argc, char* argv[])
{
    tmy_device_control();
    printf("[Main] testing end\r\n");
}
