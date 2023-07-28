#pragma once

#include <stdlib.h>

int usrp_spi_setup(std::string addr);

int usrp_select_beam_id(int mode, int id);

void usrp_free(void);
