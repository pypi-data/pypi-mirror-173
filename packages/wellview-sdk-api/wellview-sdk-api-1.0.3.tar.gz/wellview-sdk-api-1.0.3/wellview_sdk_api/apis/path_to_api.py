import typing_extensions

from wellview_sdk_api.paths import PathValues
from wellview_sdk_api.apis.paths.get_well_view_table_structure import GetWellViewTableStructure
from wellview_sdk_api.apis.paths.get_well_view_library import GetWellViewLibrary
from wellview_sdk_api.apis.paths.get_well_view_library_table import GetWellViewLibraryTable
from wellview_sdk_api.apis.paths.write_data import WriteData

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.GET_WELL_VIEW_TABLE_STRUCTURE: GetWellViewTableStructure,
        PathValues.GET_WELL_VIEW_LIBRARY: GetWellViewLibrary,
        PathValues.GET_WELL_VIEW_LIBRARY_TABLE: GetWellViewLibraryTable,
        PathValues.WRITE_DATA: WriteData,
    }
)

path_to_api = PathToApi(
    {
        PathValues.GET_WELL_VIEW_TABLE_STRUCTURE: GetWellViewTableStructure,
        PathValues.GET_WELL_VIEW_LIBRARY: GetWellViewLibrary,
        PathValues.GET_WELL_VIEW_LIBRARY_TABLE: GetWellViewLibraryTable,
        PathValues.WRITE_DATA: WriteData,
    }
)
