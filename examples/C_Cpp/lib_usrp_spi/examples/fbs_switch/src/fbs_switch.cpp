// Standalone FBS_ADDR sender for BBox 8x8 Duo.
//
// Talks directly to the X410's SPI/GPIO (HDMI-shaped connector) path in
// libusrp_fbs.so, without going through TLKCoreService. Use this when the
// BBox is already switched into external control mode and is no longer
// reachable via TLKCoreService's Ethernet scan.

#include "usrp_fbs.hpp"
#include <uhd/utils/safe_main.hpp>
#include <boost/program_options.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>

int UHD_SAFE_MAIN(int argc, char* argv[])
{
    namespace po = boost::program_options;
    std::string addr;
    int mode;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "help message")
        ("addr", po::value<std::string>(&addr)->default_value("192.168.10.2"), "USRP X410 management IP")
        ("mode", po::value<int>(&mode)->default_value(0), "0:TX 1:RX")
    ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
        std::cout << argv[0] << " " << desc << std::endl;
        return EXIT_SUCCESS;
    }

    std::cout << "[fbs_switch] Connecting to X410 at addr=" << addr << " ..." << std::endl;
    if (usrp_spi_setup("addr=" + addr) == EXIT_FAILURE) {
        std::cout << "[fbs_switch] usrp_spi_setup failed" << std::endl;
        return EXIT_FAILURE;
    }

    char buf[64];
    int addr_a, addr_b;
    do {
        std::memset(buf, 0, sizeof(buf));
        std::cout << "Please enter FBS_ADDR (mode2, e.g. '5') or 'FBS_ADDR_A FBS_ADDR_B' "
                     "(mode1, e.g. '5 20') or quit('q'): ";
        fgets(buf, sizeof(buf), stdin);
        if (buf[0] == 'q') {
            std::cout << "Break and quit loop" << std::endl;
            break;
        }
        int parsed = sscanf(buf, "%d %d", &addr_a, &addr_b);
        if (parsed == 2) {
            usrp_select_fbs_mode1(mode, addr_a, addr_b);
        } else if (parsed == 1) {
            usrp_select_fbs_mode2(mode, addr_a);
        } else {
            std::cout << "Could not parse input, try again" << std::endl;
        }
    } while (1);

    usrp_free();
    return EXIT_SUCCESS;
}
