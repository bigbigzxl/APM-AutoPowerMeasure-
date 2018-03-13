# -*- coding: utf-8 -*-
"""
    AW_PM.constants
    ~~~~~~~~~~~~~~~~

    Makes all "completion and error codes", "attribute values", "event type
    values", and "values and ranges" defined in the VISA specification VPP-4.3.2,
    section 3, available as variable values.

    The module exports the values under the original, all-uppercase names.

    This file is part of PyVISA.

    :copyright: 2014 by AW_PMpl Authors, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""


device_type = {
    "power":{},
    "multimeter":{},
    "scope":{}
}
VI_ATTR_RSRC_CLASS           = 0xBFFF0001
VI_ATTR_RSRC_NAME            = 0xBFFF0002
VI_ATTR_RSRC_IMPL_VERSION    = 0x3FFF0003
VI_ATTR_RSRC_LOCK_STATE      = 0x3FFF0004
VI_ATTR_MAX_QUEUE_LENGTH     = 0x3FFF0005
VI_ATTR_USER_DATA            = 0x3FFF0007
VI_ATTR_FDC_CHNL             = 0x3FFF000D
VI_ATTR_FDC_MODE             = 0x3FFF000F
VI_ATTR_FDC_GEN_SIGNAL_EN    = 0x3FFF0011
VI_ATTR_FDC_USE_PAIR         = 0x3FFF0013
VI_ATTR_SEND_END_EN          = 0x3FFF0016
VI_ATTR_TERMCHAR             = 0x3FFF0018
VI_ATTR_TMO_VALUE            = 0x3FFF001A
VI_ATTR_GPIB_READDR_EN       = 0x3FFF001B
VI_ATTR_IO_PROT              = 0x3FFF001C
VI_ATTR_DMA_ALLOW_EN         = 0x3FFF001E
