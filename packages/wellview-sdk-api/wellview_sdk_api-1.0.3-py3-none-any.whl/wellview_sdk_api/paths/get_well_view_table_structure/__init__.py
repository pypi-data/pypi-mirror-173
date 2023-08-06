# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from wellview_sdk_api.paths.get_well_view_table_structure import Api

from wellview_sdk_api.paths import PathValues

path = PathValues.GET_WELL_VIEW_TABLE_STRUCTURE