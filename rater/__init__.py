# import dbsettings
#
#
# class RaterSettings(dbsettings.Group):
#     rating_scale = dbsettings.StringValue(description="rating representation",
#                                           choices=["continuous_scale", "single_choice"],
#                                           default="continuous_scale")
#
#     rating_question = dbsettings.StringValue(description="question for human raters",
#                                              default="How much of the meaning of the human translation is also expressed in the machine	translation?")
#
#     single_choice_options = dbsettings.MultiSeparatorValue(description="options for single choice selection",
#                                                    default="None;Little;Much;Most;All")
#
#     continuous_scale_min = dbsettings.PositiveIntegerValue(description="Minimum value in the continuous scale", default=0)
#
#     continuous_scale_min_label = dbsettings.StringValue(description="Minimum value label in the continuous scale", default="Strongly Disagree")
#
#     continuous_scale_max = dbsettings.PositiveIntegerValue(description="Maximum value in the continuous scale", default=100)
#
#     continuous_scale_max_label = dbsettings.StringValue(description="Maximum value label in the continuous scale", default="Strongly Agree")
#
#     number_of_batches = dbsettings.PositiveIntegerValue(description="Number of batches rated segments are divided into", default=1)
#
# rater_settings = RaterSettings()