# -*- coding: UTF-8 -*-
import logging
import semantic_version

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: \t%(filename)s\t%(funcName)s\t%(lineno)s\t- %(message)s",
    filename="batpy.log",
    filemode="w",
    level=logging.INFO,
)


def is_version_compatible(
    self_version: semantic_version.Version,
    version_to_check: semantic_version.Version,
    include_minor: bool = False,
) -> bool:
    """Check for version compatibility

    Check if two versions (major.minor.patch) are compatible. Thereby a version is compatible if major is equal.
    If minor should also be included a version is compatible if major is equal and minor is greater or equal.

    Parameters
    ----------
    self_version : semantic_version.Version
        Version
    version_to_check : semantic_version.Version
        Version to be checked against self_version.
    include_minor : bool, optional
        Check if minor version of version_to_check is greater or equal to self_version's minor, by default False.

    Returns
    -------
    bool
        True, if version is compatible.

    Raises
    ------
    ValueError
        If version is not compatible a ValueError will occur.
    """
    if include_minor:
        min_minor = self_version.minor
    else:
        min_minor = 0

    min_version = semantic_version.Version(
        major=self_version.major, minor=min_minor, patch=0
    )

    if min_version <= version_to_check < min_version.next_major():
        logging.info(
            f"[+] Version {version_to_check} is compatible: {min_version} <= {version_to_check} < {min_version.next_major()}"
        )
        return True
    else:
        logging.warning(
            f"[!] Version {version_to_check} should be {min_version} <= {version_to_check} < {min_version.next_major()}"
        )
        raise ValueError(
            f"[!] Version {version_to_check} should be {min_version} <= {version_to_check} < {min_version.next_major()}"
        )
