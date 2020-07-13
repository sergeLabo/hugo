#!python3

import matplotlib.pyplot as plt
# importing matplotlib module and respective classes
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ( MultipleLocator,
                                FormatStrFormatter,
                                AutoMinorLocator)


file_name = "./loss.txt"
with open(file_name) as f:
    data = f.read()
f.close()

lines = data.splitlines()

x = []
loss = []
average = []

for line in lines:
    d_l = line.split(" ")
    x.append(d_l[0])
    loss.append(d_l[2])
    average.append(d_l[5])

fig, ax = plt.subplots()

ax.set_xlim(0, 40)
ax.plot(x, loss, 'ys-', label="Loss")
ax.plot(x, average, 'ro-', label="Average")
ax.invert_yaxis()

ax.xaxis.set_major_locator(MultipleLocator(20))
# #ax.xaxis.set_major_formatter(FormatStrFormatter('% 1.2f'))

ax.xaxis.set_minor_locator(MultipleLocator(10))
# #ax.xaxis.set_minor_formatter(FormatStrFormatter('% 1.2f'))

ax.legend(loc="upper right", title="Efficiency", frameon=False)

ax.set(xlabel='Step', ylabel='Loss', title='LossPretty Graph')
ax.grid()

fig.savefig("loss.png")
plt.show()

"""dir(ax) =
'acorr', 'add_artist', 'add_callback', 'add_child_axes', 'add_collection',
'add_container', 'add_image', 'add_line', 'add_patch', 'add_table', 'aname',
'angle_spectrum', 'annotate', 'apply_aspect', 'arrow', 'artists', 'autoscale',
'autoscale_view', 'axes', 'axhline', 'axhspan', 'axis', 'axison', 'axvline',
'axvspan', 'bar', 'barbs', 'barh', 'bbox', 'boxplot', 'broken_barh', 'bxp',
'callbacks', 'can_pan', 'can_zoom', 'change_geometry', 'child_axes', 'cla',
'clabel', 'clear', 'clipbox', 'cohere', 'colNum', 'collections', 'containers',
'contains', 'contains_point', 'contour', 'contourf', 'convert_xunits',
'convert_yunits', 'csd', 'dataLim', 'drag_pan', 'draw', 'draw_artist', 'end_pan',
'errorbar', 'eventplot', 'eventson', 'figbox', 'figure', 'fill', 'fill_between',
'fill_betweenx', 'findobj', 'fmt_xdata', 'fmt_ydata', 'format_coord',
'format_cursor_data', 'format_xdata', 'format_ydata', 'get_adjustable',
'get_agg_filter', 'get_alpha', 'get_anchor', 'get_animated', 'get_aspect',
'get_autoscale_on', 'get_autoscalex_on', 'get_autoscaley_on', 'get_axes_locator',
'get_axisbelow', 'get_children', 'get_clip_box', 'get_clip_on', 'get_clip_path',
'get_contains', 'get_cursor_data', 'get_data_ratio', 'get_data_ratio_log',
'get_default_bbox_extra_artists', 'get_facecolor', 'get_fc', 'get_figure',
'get_frame_on', 'get_geometry', 'get_gid', 'get_gridspec', 'get_images',
'get_in_layout', 'get_label', 'get_legend', 'get_legend_handles_labels',
'get_lines', 'get_navigate', 'get_navigate_mode', 'get_path_effects',
'get_picker', 'get_position', 'get_rasterization_zorder', 'get_rasterized',
'get_renderer_cache', 'get_shared_x_axes', 'get_shared_y_axes', 'get_sketch_params',
'get_snap', 'get_subplotspec', 'get_tightbbox', 'get_title', 'get_transform',
'get_transformed_clip_path_and_affine', 'get_url', 'get_visible',
'get_window_extent', 'get_xaxis', 'get_xaxis_text1_transform',
'get_xaxis_text2_transform', 'get_xaxis_transform', 'get_xbound',
'get_xgridlines', 'get_xlabel', 'get_xlim', 'get_xmajorticklabels',
'get_xminorticklabels', 'get_xscale', 'get_xticklabels', 'get_xticklines',
'get_xticks', 'get_yaxis', 'get_yaxis_text1_transform', 'get_yaxis_text2_transform',
'get_yaxis_transform', 'get_ybound', 'get_ygridlines', 'get_ylabel', 'get_ylim',
'get_ymajorticklabels', 'get_yminorticklabels', 'get_yscale', 'get_yticklabels',
'get_yticklines', 'get_yticks', 'get_zorder', 'grid', 'has_data', 'have_units',
'hexbin', 'hist', 'hist2d', 'hitlist', 'hlines', 'ignore_existing_data_limits',
'images', 'imshow', 'in_axes', 'indicate_inset', 'indicate_inset_zoom', 'inset_axes',
'invert_xaxis', 'invert_yaxis', 'is_figure_set', 'is_first_col', 'is_first_row',
'is_last_col', 'is_last_row', 'is_transform_set', 'label_outer', 'legend',
'legend_', 'lines', 'locator_params', 'loglog', 'magnitude_spectrum', 'margins',
'matshow', 'minorticks_off', 'minorticks_on', 'mouseover', 'mouseover_set', 'name',
'numCols', 'numRows', 'patch', 'patches', 'pchanged', 'pcolor', 'pcolorfast',
'pcolormesh', 'phase_spectrum', 'pick', 'pickable', 'pie', 'plot', 'plot_date',
'properties', 'psd', 'quiver', 'quiverkey', 'redraw_in_frame', 'relim', 'remove',
'remove_callback', 'reset_position', 'rowNum', 'scatter', 'semilogx', 'semilogy',

'set', 'set_adjustable', 'set_agg_filter', 'set_alpha', 'set_anchor', 'set_animated',
 'set_aspect', 'set_autoscale_on', 'set_autoscalex_on', 'set_autoscaley_on',
 'set_axes_locator', 'set_axis_off', 'set_axis_on', 'set_axisbelow', 'set_clip_box',
 'set_clip_on', 'set_clip_path', 'set_contains', 'set_facecolor', 'set_fc',
 'set_figure', 'set_frame_on', 'set_gid', 'set_in_layout', 'set_label',
 'set_navigate', 'set_navigate_mode', 'set_path_effects', 'set_picker',
 'set_position', 'set_prop_cycle', 'set_rasterization_zorder', 'set_rasterized',
 'set_sketch_params', 'set_snap', 'set_subplotspec', 'set_title', 'set_transform',
 'set_url', 'set_visible', 'set_xbound', 'set_xlabel', 'set_xlim', 'set_xmargin',
 'set_xscale', 'set_xticklabels', 'set_xticks', 'set_ybound', 'set_ylabel',
 'set_ylim', 'set_ymargin', 'set_yscale', 'set_yticklabels', 'set_yticks',

 'set_zorder', 'specgram', 'spines', 'spy', 'stackplot', 'stale', 'stale_callback',
 'start_pan', 'stem', 'step', 'sticky_edges', 'streamplot', 'table', 'tables',
 'text', 'texts', 'tick_params', 'ticklabel_format', 'title', 'titleOffsetTrans',
 'transAxes', 'transData', 'transLimits', 'transScale', 'tricontour', 'tricontourf',
 'tripcolor', 'triplot', 'twinx', 'twiny', 'update', 'update_datalim',
 'update_datalim_bounds', 'update_from', 'update_params', 'use_sticky_edges',
 'viewLim', 'violin', 'violinplot', 'vlines', 'xaxis', 'xaxis_date',
 'xaxis_inverted', 'xcorr', 'yaxis', 'yaxis_date', 'yaxis_inverted', 'zorder']
"""
