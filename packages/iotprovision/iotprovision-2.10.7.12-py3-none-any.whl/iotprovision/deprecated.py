"""
Deprecated stuff. This is expected to be removed partially or
completely at some point, so don't pollute main logic with it.
"""
from logging import getLogger

def deprecated(args):
    """
    Deal with deprecation oddities

    :param args: Invocation arguments
    :return: Possibly modifed arguments or None if failure
    """
    logger = getLogger(__name__)

    # Early versions of iotprovision used "custom" for AWS JITR but after MAR was introduced the user must be explicit
    if args.cloud_provider == "aws":
        if args.provision_method == "custom":
            logger.warning("")
            logger.warning('AWS provisioning method name "custom" is deprecated - use "jitr" instead')
            logger.warning("")
            args.provision_method = "jitr"

    if args.cloud_provider == "azure" and "wincupgrade" not in args.actions:
        # Always do winc upgrade for Azure (Until all kits have new winc FW from factory?)
        args.actions.append("wincupgrade")

    return args
