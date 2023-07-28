// Example for SPI testing for BBox of TMYTEK.
//
// This example shows how to work with SPI (for TMYTEK BBox procotol)
// which is based on the GPIO interface of the X410.

#include <uhd/features/spi_getter_iface.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/utils/safe_main.hpp>
#include <stdlib.h>
#include <boost/program_options.hpp>
#include <iostream>

#include "usrp_fbs.hpp"

// static const std::string SPI_DEFAULT_GPIO      = "GPIOA";
static const size_t SPI_DEFAULT_CLK_PIN        = 3;
static const size_t SPI_DEFAULT_SDI_PIN        = 7;
static const size_t SPI_DEFAULT_SDO_PIN        = 4;
static const size_t SPI_DEFAULT_CS_PIN         = 0;

static const size_t GPIO_DEFAULT_SDI_PIN       = 5;
static const size_t GPIO_DEFAULT_LDB_PIN       = 6;
static const size_t GPIO_DEFAULT_TX_EN_PIN     = 2;
static const size_t GPIO_DEFAULT_RX_EN_PIN     = 9;

static const size_t SPI_DEFAULT_PAYLOAD_LENGTH = 32;
static const std::string SPI_DEFAULT_PAYLOAD   = "0xfefe";
static const size_t SPI_DEFAULT_CLK_DIVIDER    = 4;

// TMYTEK IC mode register address for TX(Gain/Phase), and RX(Gain/Phase)
static const size_t reg_address[][2] = { {0x58, 0x78}, {0x54, 0x70} };

static const size_t num_bits = 12;

static inline uint32_t GPIO_BIT(const size_t x)
{
    return (1 << x);
}

uhd::usrp::multi_usrp::sptr usrp = NULL;

std::string gpio_bank;

// variables for SPI and follows TMYTEK's defined pin mapping:
size_t clk = SPI_DEFAULT_CLK_PIN;
size_t sdi = SPI_DEFAULT_SDI_PIN;
size_t sdo = SPI_DEFAULT_SDO_PIN;
size_t cs = SPI_DEFAULT_CS_PIN;
size_t payload_length = 13;
size_t clk_divider = SPI_DEFAULT_CLK_DIVIDER;
std::string payload_str;
uint32_t payload;

// SPI reference handler
uhd::spi_iface::sptr spi_ref;
// The spi_config_t holds items like the clock divider and the SDI and SDO edges
uhd::spi_config_t spi_config;

std::string to_bit_string(uint32_t val, const size_t num_bits)
{
    std::string out;
    for (int i = num_bits - 1; i >= 0; i--) {
        std::string bit = ((val >> i) & 1) ? "1" : "0";
        out += "  ";
        out += bit;
    }
    return out;
}

// Debug usage
void output_reg_values(const std::string& bank,
    const std::string& port,
    const uhd::usrp::multi_usrp::sptr& usrp,
    const size_t num_bits,
    const bool has_src_api)
{
    const std::vector<std::string> attrs = {
        "CTRL", "DDR", "ATR_0X", "ATR_RX", "ATR_TX", "ATR_XX", "OUT", "READBACK"};
    std::cout << (boost::format("%10s:") % "Bit");
    for (int i = num_bits - 1; i >= 0; i--)
        std::cout << (boost::format(" %2d") % i);
    std::cout << std::endl;
    for (const auto& attr : attrs) {
        const uint32_t gpio_bits = uint32_t(usrp->get_gpio_attr(bank, attr));
        std::cout << (boost::format("%10s:%s") % attr
                      % to_bit_string(gpio_bits, num_bits))
                  << std::endl;
    }

    if (!has_src_api) {
        return;
    }

    // GPIO Src - get_gpio_src() not supported for all devices
    try {
        const auto gpio_src = usrp->get_gpio_src(port);
        std::cout << boost::format("%10s:") % "SRC";
        for (auto src : gpio_src) {
            std::cout << " " << src;
        }
        std::cout << std::endl;
    } catch (const uhd::not_implemented_error& e) {
        std::cout << "Ignoring " << e.what() << std::endl;
    } catch (...) {
        throw;
    }
}

/*
 * Setup SPI & gpio config for BBox of TMYTEK
 */
int usrp_spi_setup(std::string addr)
{
    // const uhd::device_addr_t& dev_addr
    // It will be the format likes: addr=192.168.100.10
    if(usrp == NULL) {
        // Create a usrp device
        std::cout << "[USRP] Creating the usrp device with: " << addr << "..." << std::endl;
        usrp = uhd::usrp::multi_usrp::make(addr);
    }

    // Get the SPI getter interface from where we'll get the SPI interface itself
    if (!usrp->get_radio_control().has_feature<uhd::features::spi_getter_iface>()) {
        std::cout << "[USRP] Error: Could not find SPI_Getter_Iface. Please check if your FPGA "
                     "image is up to date.\n";
        return EXIT_FAILURE;
    }
    auto& spi_getter_iface =
        usrp->get_radio_control().get_feature<uhd::features::spi_getter_iface>();

    //Only for GPIO0 here
    std::string port = usrp->get_gpio_src_banks(0).front();
    std::cout << "[USRP] Using GPIO connector: " << port << std::endl;
    gpio_bank = usrp->get_gpio_banks(0).front();
    std::cout << "[USRP] Using GPIO bank: " << gpio_bank << std::endl;

    // Set some available pins to SPI for GPIO0
    // TODO: GPIO1
    std::vector<std::string> sources(num_bits, "DB0_RF0");
    // Set SPI gpios
    sources[clk] = "DB0_SPI";
    sources[sdi] = "DB0_SPI";
    sources[sdo] = "DB0_SPI";
    sources[cs] = "DB0_SPI";
    usrp->set_gpio_src(port, sources);
    // usrp->set_gpio_src("GPIO1", sources);

    // Create peripheral configuration per peripheral
    // The terms 'MISO' and 'MOSI' in the spi_config_t struct map to 'SDI' and 'SDO' respectively.
    uhd::features::spi_periph_config_t periph_cfg;
    periph_cfg.periph_clk = clk;
    periph_cfg.periph_sdi = sdi; //MISO, controld by IC
    periph_cfg.periph_sdo = sdo; //MOSI, IC_PDI
    periph_cfg.periph_cs  = cs;

    // The vector holds the peripheral configs with index=peripheral number
    std::vector<uhd::features::spi_periph_config_t> periph_cfgs;
    periph_cfgs.push_back(periph_cfg);

    // Set the data direction register
    uint32_t outputs = 0x0;
    outputs |= 1 << periph_cfg.periph_clk;
    outputs |= 1 << periph_cfg.periph_sdo;
    outputs |= 1 << periph_cfg.periph_cs;
    outputs |= 1 << GPIO_DEFAULT_SDI_PIN; //IC_SDI, always low
    outputs |= 1 << GPIO_DEFAULT_LDB_PIN; //LDB, low pulse after transmission
    outputs |= 1 << GPIO_DEFAULT_TX_EN_PIN;
    outputs |= 1 << GPIO_DEFAULT_RX_EN_PIN;
    std::cout << "[USRP] direction pin config: " << outputs << std::endl;
    usrp->set_gpio_attr(gpio_bank, "DDR", outputs & 0xFFFFFF);
    spi_ref = spi_getter_iface.get_spi_ref(periph_cfgs);

    std::cout << "[USRP] Using pins: " << std::endl
              << "  CS    = " << (int)(periph_cfg.periph_cs) << std::endl
              << "  Clock = " << (int)(periph_cfg.periph_clk) << std::endl
              << "  SDO   = " << (int)(periph_cfg.periph_sdo) << std::endl
              << "  SDI   = " << (int)(periph_cfg.periph_sdi) << std::endl
              << std::endl;

    // Disable ATR mode(automatic controlled by FPGA) for all pins
    usrp->set_gpio_attr(gpio_bank, "CTRL", 0x0, outputs & 0xFFFFFF);
    // Set default output pins
    usrp->set_gpio_attr(gpio_bank, "OUT", 0x0, outputs & 0xFFFFFF);
    usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(SPI_DEFAULT_SDI_PIN), GPIO_BIT(SPI_DEFAULT_SDI_PIN));
    usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(GPIO_DEFAULT_LDB_PIN), GPIO_BIT(GPIO_DEFAULT_LDB_PIN));

    std::cout << "[USRP] Configured GPIO values:" << std::endl;
    bool has_src_api = true;
    output_reg_values(gpio_bank, port, usrp, num_bits, has_src_api);

    spi_config.divider            = clk_divider;
    spi_config.use_custom_divider = true;
    spi_config.mosi_edge          = spi_config.EDGE_RISE;
    spi_config.miso_edge          = spi_config.EDGE_FALL;

    return EXIT_SUCCESS;
}

/*
 * Higher function to generating SPI & gpio operation for BBox of TMYTEK
 */
int usrp_select_beam_id(int mode, int id)
{
    // Check id is in range
    if (id < 1 || id > 64) {
        std::cout << "[USRP] Invalid Beam ID: " << id << std::endl;
        return EXIT_FAILURE;
    }

    // Switch Tx/Rx mode
    if (mode == 0) {
        std::cout << "[USRP] Tx mode" << std::endl;
        usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(GPIO_DEFAULT_TX_EN_PIN), GPIO_BIT(GPIO_DEFAULT_TX_EN_PIN));
        usrp->set_gpio_attr(gpio_bank, "OUT", 0, GPIO_BIT(GPIO_DEFAULT_RX_EN_PIN));
    } else {
        std::cout << "[USRP] Rx mode" << std::endl;
        usrp->set_gpio_attr(gpio_bank, "OUT", 0, GPIO_BIT(GPIO_DEFAULT_TX_EN_PIN));
        usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(GPIO_DEFAULT_RX_EN_PIN), GPIO_BIT(GPIO_DEFAULT_RX_EN_PIN));
    }

    /* Transform payload to the format of BF IC, and index starts from 0
     * [Example]:
     *      1. TX beam_id=1  => Gain:0x1600 & Phase:0x1e00
     *      2. RX beam_id=20 => Gain:0x1513 & Phase:0x1c13
     */
    for (int i=0; i<2; i++) {
        payload = (reg_address[mode][i] << 6) | ((id-1) & 0x3F);
        std::cout << "[USRP] Writing payload: 0x" << std::hex << payload << " with length "
              << std::dec << payload_length << " bits" << std::endl;

        // Do the SPI transaction. There are write() and read() methods available, too.
        std::cout << "[USRP] Performing SPI transaction..." << std::endl;
        // uint32_t read_data = spi_ref->transact_spi(0, spi_config, payload, payload_length, true);
        // std::cout << "Data read: 0x" << std::hex << read_data << std::endl;
        spi_ref->write_spi(0, spi_config, payload, payload_length);

        // TMY LDB: low pulse
        usrp->set_gpio_attr(gpio_bank, "OUT", 0, GPIO_BIT(GPIO_DEFAULT_LDB_PIN));
        usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(GPIO_DEFAULT_LDB_PIN), GPIO_BIT(GPIO_DEFAULT_LDB_PIN));
    }

    std::cout << "[USRP] BeamID:" << id << " selected" << std::endl;
    return EXIT_SUCCESS;
}

/*
 * Free usrp instance to avoid 'Segmentation fault'
 */
void usrp_free(void)
{
    usrp = NULL;
}

int UHD_SAFE_MAIN(int argc, char* argv[])
{
    namespace po = boost::program_options;

    // variables to be set by po
    std::string args;

    // setup the program options
    po::options_description desc("Allowed options");
    // clang-format off
    desc.add_options()
        ("help", "help message")
        ("args", po::value<std::string>(&args)->default_value(""), "multi uhd device address args")
        ("list-banks", "print list of banks before running tests")
        ("clk", po::value<size_t>(&clk)->default_value(SPI_DEFAULT_CLK_PIN), "number of pin for SPI clock")
        ("sdo", po::value<size_t>(&sdo)->default_value(SPI_DEFAULT_SDO_PIN), "number of pin for serial data out")
        ("sdi", po::value<size_t>(&sdi)->default_value(SPI_DEFAULT_SDI_PIN), "number of pin for serial data in")
        ("cs", po::value<size_t>(&cs)->default_value(SPI_DEFAULT_CS_PIN), "number of pin for chip select")
        ("payload", po::value<std::string>(&payload_str)->default_value(SPI_DEFAULT_PAYLOAD), "payload as integer value")
        ("length", po::value<size_t>(&payload_length)->default_value(SPI_DEFAULT_PAYLOAD_LENGTH), "payload length in bits")
        ("clk-div", po::value<size_t>(&clk_divider)->default_value(SPI_DEFAULT_CLK_DIVIDER), "clock divider for SPI")
    ;
    // clang-format on
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    // print the help message
    if (vm.count("help")) {
        std::cout << argv[0] << " " << desc << std::endl;
        return ~0;
    }

    // create a usrp device
    std::cout << std::endl;
    std::cout << "Creating the usrp device with: " << args << "..." << std::endl;
    usrp = uhd::usrp::multi_usrp::make(args);

    if (vm.count("list-banks")) {
        std::cout << "Available GPIO banks: " << std::endl;
        auto banks = usrp->get_gpio_banks(0);
        for (auto& bank : banks) {
            std::cout << "* " << bank << std::endl;
        }
    }

    int ret = usrp_spi_setup(args);
    if (ret == EXIT_FAILURE)
        return ret;

    payload = strtoul(payload_str.c_str(), NULL, 0);
    std::cout << "Writing payload: 0x" << std::hex << payload << " with length "
              << std::dec << payload_length << " bits" << std::endl;

    spi_config.divider            = clk_divider;
    spi_config.use_custom_divider = true;
    spi_config.mosi_edge          = spi_config.EDGE_RISE;
    spi_config.miso_edge          = spi_config.EDGE_FALL;

    // Do the SPI transaction. There are write() and read() methods available, too.
    std::cout << "Performing SPI transaction..." << std::endl;
    // uint32_t read_data = spi_ref->transact_spi(0, spi_config, payload, payload_length, true);
    // std::cout << "Data read: 0x" << std::hex << read_data << std::endl;
    spi_ref->write_spi(0, spi_config, payload, payload_length);

    // TMY LDB: low pulse
    usrp->set_gpio_attr(gpio_bank, "OUT", 0, GPIO_BIT(GPIO_DEFAULT_LDB_PIN));
    usrp->set_gpio_attr(gpio_bank, "OUT", GPIO_BIT(GPIO_DEFAULT_LDB_PIN), GPIO_BIT(GPIO_DEFAULT_LDB_PIN));

    std::cout << "End" << std::endl;

    usrp_free();
    return EXIT_SUCCESS;
}
