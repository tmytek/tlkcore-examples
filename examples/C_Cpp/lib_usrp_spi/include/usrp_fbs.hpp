#pragma once

#include <stdlib.h>
#include <uhd/usrp/multi_usrp.hpp>

int usrp_spi_setup();
int usrp_spi_setup(std::string addr);
int usrp_spi_setup(uhd::usrp::multi_usrp::sptr available_usrp);

void usrp_set_mode(int mode);
int usrp_select_beam_id(int mode, int id);

void usrp_free(void);
