settings = {}
# FIXME: make setting for pre-processing for frame detection
# settings['glob_pattern'] = "/home/martijn/Documents/work/2023-08_synthesis/vu_high_res/iiif_cache/northkorea/*309.json"
# settings['glob_pattern'] = "/home/martijn/Documents/work/2023-08_synthesis/north_korea/infos/*069.json"
# settings['glob_pattern'] = "/home/martijn/Documents/work/2023-08_synthesis/north_korea/infos/*130.json"
# settings['glob_pattern'] = "/home/martijn/Documents/work/2023-08_synthesis/north_korea/infos/*009.json"
settings["glob_pattern"] = (
    "/home/martijn/Documents/work/2023-08_synthesis/north_korea/infos/*.json"
)
settings["output_folder"] = "/scratch/iiif_inspect/north_korea"

settings["overview_width"] = 1024  # overview size
settings["pipeline_overview"] = (
    "bgr2rgb|gray|equalize_clahe|otsu_threshold|make_fat(2,4)|canny|invert"
)
# # settings["pipeline_overview"] = "bgr2rgb|gray|equalize_clahe|otsu_threshold"

# settings["glob_start"] = 3  # 0
# settings["erode_dilate_kernel"] = 3
settings["part_size"] = 150
settings["expected_layouts"] = [
    # [[left, right], [bottom, top]] # left/right along positive x; bottom / top along negative y
    # [[130, 860], [133, 780]],  # at size width=1024
    # [[135, 900], [133, 780]],  # at size width=1024
    # [[250, 1805], [265, 1560]],
    # [[325, 1800], [250, 1560]],
    # [[325, 1800], [250, 1560]],
    [[174, 907], [133, 780]],  # at size width=1024, override for sheet = 290 / 309
]
settings["overview_width"] = 1024
# settings["samples_along_rim"] = 5  # how many samples to take along rim
# settings["samples_outskirt"] = (
#     0.05  # percentage of space to go away from the corner for samples
# )
# settings["rim_threshold"] = 170  # threshold to generate high res black white image
# settings["rim_size_pixels"] = (
#     25  # how many black pixels does the thick frame occupy on the high resolution version
# )
# settings["rim_offset"] = (
#     192  # on the high resolution version, number of pixels from the thick black line to the rim of the sheet
# )
settings["rim_fraction_filled"] = (
    0.7  # percentage as number between [0.0-1.0] of how many pixels will need to be black
    # (where will peaks be thresholded)
)
settings["interactive_plots"] = False
settings["produce_output"] = True
settings["output_file_name"] = "/tmp/north_korea_rim_points.ndjson"
settings["enable_caching"] = False

settings["rim_to_find"] = "outer-inner"
# settings["rim_width_outer"] = 26
settings["rim_width_outer_fuzzy"] = [26 - 8, 26 - 2, 26 + 5, 26 + 7]
# settings["rim_width_inner"] = 1
settings["rim_width_inner_fuzzy"] = [0, 2, 4, 8]
# settings["rim_outer_inner_distance"] = 200
outer_target = 200
settings["rim_outer_inner_distance_fuzzy"] = [
    outer_target - 30,
    outer_target - 10,
    outer_target + 10,
    outer_target + 30,
]


d = {"rim_to_find": "outer-inner"}
d["rim_width_outer_fuzzy"] = [26 - 8, 26 - 2, 26 + 5, 26 + 7]
d["rim_width_inner_fuzzy"] = [0, 2, 4, 8]
distance = 60
d["rim_outer_inner_distance_fuzzy"] = [
    outer_target - 30,
    outer_target - 10,
    outer_target + 10,
    outer_target + 30,
]
d["pipeline_detail_split_horizontal_vertical"] = False
d["rim_fraction_filled"] = (
    0.5  # percentage of how many pixels will need to be black in cut-out rectangle
)


# # # FIXME:
# # # to find the outer rim, a threshold that is more towards 0 (lower) works better
# # # while a threshold more towards 255 (higher) is better for the 'double rim find'
# d["pipeline_detail"] = "bgr2rgb|gray|threshold(190)"

settings["find_rims"] = [d]

d = {"rim_to_find": "outer"}
d["rim_width_fuzzy"] = [26 - 8, 26 - 2, 26 + 5, 26 + 7]
d["pipeline_detail"] = "bgr2rgb|gray|threshold(150)"
d["pipeline_detail_split_horizontal_vertical"] = False
d["rim_fraction_filled"] = (
    0.5  # percentage of how many pixels will need to be black in cut-out rectangle
)

settings["find_rims"].append(d)
# FIXME: for particular sheets, we may want to overwrite the settings
# we could store this in a dict, indexed by sheet id (numeric / uuid?)
# settings["overwrite"] = {25: {"find_rims": [{"a": "b"}]}}

import json

print(json.dumps(settings, indent=2))
