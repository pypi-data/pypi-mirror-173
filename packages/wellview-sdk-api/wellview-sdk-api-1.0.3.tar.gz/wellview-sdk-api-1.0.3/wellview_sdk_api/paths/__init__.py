# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from wellview_sdk_api.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    GET_WELL_VIEW_TABLE_STRUCTURE = "/GetWellViewTableStructure"
    GET_WELL_VIEW_LIBRARY = "/GetWellViewLibrary"
    GET_WELL_VIEW_LIBRARY_TABLE = "/GetWellViewLibraryTable"
    WRITE_DATA = "/WriteData"
