#pragma once

#include <stdlib.h>
#include <uhd/usrp/multi_usrp.hpp>

int usrp_spi_setup();
int usrp_spi_setup(std::string addr);
int usrp_spi_setup(uhd::usrp::multi_usrp::sptr available_usrp);

void usrp_set_mode(int mode);
int usrp_select_beam_id(int mode, int id);

/*
 * BBox 8x8 Duo: Fast Command Mode 2 (A=B phase) write.
 * Writes a single FBS_ADDR[8:0] (0-511) that applies to both A/B channels.
 */
int usrp_select_fbs_addr(int mode, int addr);

void usrp_free(void);
