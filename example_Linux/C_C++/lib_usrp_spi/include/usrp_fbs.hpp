#pragma once

#include <stdlib.h>

int usrp_spi_setup(std::string addr);

void usrp_set_mode(int mode);
int usrp_select_beam_id(int mode, int id);

void usrp_free(void);
