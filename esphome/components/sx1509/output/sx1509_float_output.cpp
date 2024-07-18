#include "sx1509_float_output.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome {
namespace sx1509 {

static const char *const TAG = "sx1509_float_channel";

void SX1509FloatOutputChannel::write_state(float state) {
  const uint16_t max_duty = 255;
  const float duty_rounded = roundf(state * max_duty);
  auto duty = static_cast<uint16_t>(duty_rounded);
  this->parent_->set_pin_value(this->pin_, duty);
}

void SX1509FloatOutputChannel::setup_blink(uint8_t t_on, uint8_t t_off, uint8_t on_intensity, uint8_t off_intensity,
                                           uint8_t t_rise, uint8_t t_fall) {
  t_on &= 0x1F;   // t_on should be a 5-bit value
  t_off &= 0x1F;  // t_off should be a 5-bit value
  off_intensity &= 0x07;
  // Write the time on
  this->parent_->write_byte(REG_T_ON[this->pin_], t_on);
  this->parent_->write_byte(REG_OFF[this->pin_], (t_off << 3) | off_intensity);
  this->parent_->write_byte(REG_I_ON[this->pin_], on_intensity);

  t_rise &= 0x1F;
  t_fall &= 0x1F;
  if (REG_T_RISE[this->pin_] != 0xFF)
    this->parent_->write_byte(REG_T_RISE[this->pin_], t_rise);
  if (REG_T_FALL[this->pin_] != 0xFF)
    this->parent_->write_byte(REG_T_FALL[this->pin_], t_fall);
}

void SX1509FloatOutputChannel::setup() {
  ESP_LOGD(TAG, "setup pin %d", this->pin_);
  this->parent_->pin_mode(this->pin_, gpio::FLAG_OUTPUT);
  this->parent_->setup_led_driver(this->pin_);
  this->turn_off();
}

void SX1509FloatOutputChannel::dump_config() {
  ESP_LOGCONFIG(TAG, "SX1509 PWM:");
  ESP_LOGCONFIG(TAG, "  sx1509 pin: %d", this->pin_);
  LOG_FLOAT_OUTPUT(this);
}

}  // namespace sx1509
}  // namespace esphome
