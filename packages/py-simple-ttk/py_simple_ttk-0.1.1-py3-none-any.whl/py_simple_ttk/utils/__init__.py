from .color import (
    limit_255,
    rgb_to_hex,
    rgba_to_hex,
    hex_to_rgb,
    hex_to_rgba,
    get_gradient,
    rgb_to_scalar,
    scalar_to_rgb,
    linear_gradient,
    get_rainbow,
    COLOR_FUNCTIONS,
)

from .HTML_Generator import HTML_Generator
from .TXT_Generator import TXT_Generator
from .MD_Generator import MD_Generator
from .utils import (
    check_if_module_installed,
    check_string_contains,
    dummy_function,
    format_SI,
    get_friendly_modified_time,
    get_friendly_time,
    get_installed_packages,
    get_unix_timestamp,
    get_unix_timestring,
    get_user_home_folder,
    modify_filename,
    open_folder_in_explorer,
    sort_dict_by_keys,
    timer_decorator,
)
from .History import HistoryMixin
from .scaling import enable_dpi_awareness
from .ProfilesSystem import (
    ProfilesSystem,
    UserProfile,
    get_profiles_folder,
    get_profiles_list,
    PROFILES_OBJECTS,
    PROFILES_FUNCTIONS,
)
