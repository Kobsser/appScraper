
""" STEP FIVE """

import logging


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)


def parse_to_meaning_ful_text(input_phone_number, in_dict):
    """ convert the dictionary returned in STEP FOUR
    into Telegram HTML text """
    me_t = ""
    me_t += "<i>Phone Number</i>: "
    me_t += f"<u>{input_phone_number}</u>"
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>App Configuration</i>"
    me_t += "\n"
    me_t += "<b>APP ID</b>: "
    me_t += "<code>{}</code>".format(in_dict["App Configuration"]["app_id"])
    me_t += "\n"
    me_t += "<b>API HASH</b>: "
    me_t += "<code>{}</code>".format(in_dict["App Configuration"]["api_hash"])
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>Available MTProto Servers</i>"
    me_t += "\n"
    me_t += "<b>Production Configuration</b>: "
    me_t += "<code>{}</code> <u>{}</u>".format(
        in_dict["Available MTProto Servers"]["production_configuration"]["IP"],
        in_dict["Available MTProto Servers"]["production_configuration"]["DC"]
    )
    me_t += "\n"
    me_t += "<b>Test Configuration</b>: "
    me_t += "<code>{}</code> <u>{}</u>".format(
        in_dict["Available MTProto Servers"]["test_configuration"]["IP"],
        in_dict["Available MTProto Servers"]["test_configuration"]["DC"]
    )
    me_t += "\n"
    me_t += "\n"
    me_t += "<i>Disclaimer</i>: "
    me_t += "<u>{}</u>".format(
        in_dict["Disclaimer"]
    )
    return me_t
