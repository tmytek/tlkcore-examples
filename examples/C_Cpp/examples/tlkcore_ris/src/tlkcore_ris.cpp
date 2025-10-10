#include "tlkcore_lib.hpp"
#include "common_lib.h"

#include <iostream>
#include <vector>
#include <string.h>
#include <fstream>
#include <sstream>
#include <regex>

using namespace tlkcore;
using namespace std;

std::vector<std::string> ris_list;

std::vector<std::string> load_sn_from_conf(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Cannot open file: " << filepath << std::endl;
        return {};
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string file_contents = buffer.str();

    std::vector<std::string> sn_list;
    std::regex sn_regex("\"(RIS[A-Za-z0-9-]+)\":\\s*\\{");
    auto sn_begin = std::sregex_iterator(file_contents.begin(), file_contents.end(), sn_regex);
    auto sn_end = std::sregex_iterator();

    for (std::sregex_iterator i = sn_begin; i != sn_end; ++i) {
        sn_list.push_back((*i)[1].str());
    }

    return sn_list;
}

int get_ris_module_info(tlkcore_lib::tlkcore_ptr service)
{
    for (std::string sn : ris_list) {
        if (service->get_ris_module_info(sn) < 0)
        {
            return -1;
        }
    }
    return 0;
}

int get_ris_pattern(tlkcore_lib::tlkcore_ptr service)
{
    std::string sn = ris_list[0];
    if (service->get_ris_pattern(sn) < 0)
    {
        return -1;
    }

    return 0;
}

int set_ris_angle(tlkcore_lib::tlkcore_ptr service)
{
    std::string sn = ris_list[0];
    if (service->set_ris_angle(sn) < 0)
    {
        return -1;
    }
    return 0;
}

int tmy_device_control()
{
    printf("[Main] Start controlling\r\n");

    printf("RIS\r\n");
    
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

    ris_list = load_sn_from_conf(path);
    
    if (get_ris_module_info(ptr) < 0)
    {
        return -1;
    }

    if (get_ris_pattern(ptr) < 0)
    {
        return -1;
    }

    if (set_ris_angle(ptr) < 0)
    {
        return -1;
    }

    if (get_ris_pattern(ptr) < 0)
    {
        return -1;
    }

    return 0;
}

int main(int argc, char* argv[])
{
    if (tmy_device_control() < 0)
        printf("[Main] testing failed\r\n");
    else
        printf("[Main] testing end\r\n");
}
