import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_PIN, CONF_ID
from .. import SX1509Component, sx1509_ns, CONF_SX1509_ID

CONF_BLINK = "blink"
CONF_ON_TIME = "on_time"
CONF_OFF_TIME = "off_time"
CONF_RISE_TIME = "rise_time"
CONF_FALL_TIME = "fall_time"
CONF_ON_INTENSITY = "on_intensity"
CONF_OFF_INTENSITY = "off_intensity"

DEPENDENCIES = ["sx1509"]

SX1509FloatOutputChannel = sx1509_ns.class_(
    "SX1509FloatOutputChannel", output.FloatOutput, cg.Component
)

BLINK_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ON_TIME): cv.positive_time_period_milliseconds,
        cv.Required(CONF_OFF_TIME): cv.positive_time_period_milliseconds,
        cv.Required(CONF_RISE_TIME): cv.positive_time_period_milliseconds,
        cv.Required(CONF_FALL_TIME): cv.positive_time_period_milliseconds,
        cv.Required(CONF_ON_INTENSITY): cv.int_range(min=0, max=255),
        cv.Required(CONF_OFF_INTENSITY): cv.int_range(min=0, max=255),
    }
)

CONFIG_SCHEMA = output.FLOAT_OUTPUT_SCHEMA.extend(
    {
        cv.Required(CONF_ID): cv.declare_id(SX1509FloatOutputChannel),
        cv.GenerateID(CONF_SX1509_ID): cv.use_id(SX1509Component),
        cv.Required(CONF_PIN): cv.int_range(min=0, max=15),
        cv.Optional(CONF_BLINK): cv.Schema(BLINK_SCHEMA),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_SX1509_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    if CONF_BLINK in config:
        blink = config[CONF_BLINK]
        cg.add(
            var.setup_blink(
                blink[CONF_ON_TIME],
                blink[CONF_OFF_TIME],
                blink[CONF_RISE_TIME],
                blink[CONF_FALL_TIME],
                blink[CONF_ON_INTENSITY],
                blink[CONF_OFF_INTENSITY],
            )
        )

    await output.register_output(var, config)
    cg.add(var.set_pin(config[CONF_PIN]))
    cg.add(var.set_parent(parent))
