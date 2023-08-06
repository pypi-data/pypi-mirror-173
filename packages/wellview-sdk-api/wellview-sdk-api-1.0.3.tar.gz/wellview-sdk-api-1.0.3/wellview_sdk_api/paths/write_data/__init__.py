# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from wellview_sdk_api.paths.write_data import Api

from wellview_sdk_api.paths import PathValues

path = PathValues.WRITE_DATA