"""TEMPLATE PLOTLY BASED ON THEME"""
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template
from pyconfig import appConfig
from plotly import colors
import plotly.graph_objects as go

load_figure_template(appConfig.TEMPLATE.THEME.lower())
fktemplate = pio.templates[pio.templates.default]

# VARS
_FONT_FAMILY = fktemplate.layout.font.family
_FONT_COLOR_TUPLE = colors.hex_to_rgb(fktemplate.layout.font.color)
_FONT_COLOR_RGB_ALPHA = "rgba({},{},{},0.2)".format(*_FONT_COLOR_TUPLE)

# LAYOUT
fktemplate.layout.images = [
    dict(
        source=appConfig.TEMPLATE.WATERMARK_SOURCE,
        xref="x domain",
        yref="y domain",
        x=0.5,
        y=0.5,
        sizex=0.5,
        sizey=0.5,
        xanchor="center",
        yanchor="middle",
        name="watermark-fiako",
        layer="below",
        opacity=0.2,
    )
]

# GENERAL

fktemplate.layout.hovermode = "x"
fktemplate.layout.margin.t = 80
fktemplate.layout.margin.b = 35
fktemplate.layout.margin.l = 55  # noqa
fktemplate.layout.margin.r = 55
fktemplate.layout.margin.pad = 0
# fktemplate.layout.paper_bgcolor = "rgba(0,0,0,0)"
fktemplate.layout.paper_bgcolor = fktemplate.layout.plot_bgcolor

# LEGEND
_LEGEND_FONT_SIZE = 15
fktemplate.layout.showlegend = True
fktemplate.layout.legend.font.size = _LEGEND_FONT_SIZE
fktemplate.layout.legend.groupclick = "toggleitem"


def apply_legend_inside():
    fktemplate.layout.legend.xanchor = "left"
    fktemplate.layout.legend.yanchor = "top"
    fktemplate.layout.legend.x = 0.005
    fktemplate.layout.legend.y = 0.98
    fktemplate.layout.legend.orientation = "h"
    fktemplate.layout.legend.bordercolor = "black"
    fktemplate.layout.legend.borderwidth = 1
    fktemplate.layout.legend.bgcolor = "rgba(255,255,255,0.6)"


if appConfig.TEMPLATE.SHOW_LEGEND_INSIDE:
    apply_legend_inside()

# MODEBAR
fktemplate.layout.modebar.activecolor = "blue"
fktemplate.layout.modebar.add = (
    "hoverclosest hovercompare v1hovermode togglehover drawrect eraseshape".split()
)
# fktemplate.layout.modebar.remove = "toImage"
fktemplate.layout.modebar.bgcolor = "rgba(0,0,0,0)"
fktemplate.layout.modebar.color = "rgba(0,0,0,0.6)"

# NEWSHAPE
fktemplate.layout.newshape.line.color = "red"
fktemplate.layout.newshape.line.width = 3

# HOVERLABEL
fktemplate.layout.hoverlabel.font.family = _FONT_FAMILY

# TITLE
fktemplate.layout.title.pad = dict(b=10, l=0, r=0, t=0)
fktemplate.layout.title.x = 0
fktemplate.layout.title.xref = "paper"
fktemplate.layout.title.y = 1
fktemplate.layout.title.yref = "paper"
fktemplate.layout.title.yanchor = "bottom"
fktemplate.layout.title.font.size = 35

# XAXIS
_XAXIS_GRIDCOLOR = "black"  # fktemplate.layout.xaxis.gridcolor
_XAXIS_LINEWIDTH = 2
_XAXIS_TITLE_FONT_SIZE = 20
_XAXIS_TITLE_STANDOFF = 20
fktemplate.layout.xaxis.mirror = True
fktemplate.layout.xaxis.showline = True
fktemplate.layout.xaxis.linewidth = _XAXIS_LINEWIDTH
fktemplate.layout.xaxis.linecolor = _XAXIS_GRIDCOLOR
fktemplate.layout.xaxis.spikecolor = _XAXIS_GRIDCOLOR
fktemplate.layout.xaxis.gridcolor = _FONT_COLOR_RGB_ALPHA
fktemplate.layout.xaxis.gridwidth = _XAXIS_LINEWIDTH
# fktemplate.layout.xaxis.title.text = "<b>PLACEHOLDER XAXIS</b>"
fktemplate.layout.xaxis.title.font.size = _XAXIS_TITLE_FONT_SIZE
fktemplate.layout.xaxis.title.standoff = _XAXIS_TITLE_STANDOFF
fktemplate.layout.xaxis.spikethickness = 1
fktemplate.layout.xaxis.spikemode = "across"
fktemplate.layout.xaxis.spikedash = "solid"


# YAXIS
_YAXIS_GRIDCOLOR = "black"  # fktemplate.layout.yaxis.gridcolor
_YAXIS_LINEWIDTH = 2
_YAXIS_TITLE_FONT_SIZE = 20
_YAXIS_TITLE_STANDOFF = 15
fktemplate.layout.yaxis.mirror = True
fktemplate.layout.yaxis.showline = True
fktemplate.layout.yaxis.linewidth = _YAXIS_LINEWIDTH
fktemplate.layout.yaxis.linecolor = _YAXIS_GRIDCOLOR
fktemplate.layout.yaxis.spikecolor = _YAXIS_GRIDCOLOR
fktemplate.layout.yaxis.rangemode = "tozero"
fktemplate.layout.yaxis.gridcolor = _FONT_COLOR_RGB_ALPHA
fktemplate.layout.yaxis.gridwidth = _YAXIS_LINEWIDTH
# fktemplate.layout.yaxis.title.text = "<b>PLACEHOLDER XAXIS</b>"
fktemplate.layout.yaxis.title.font.size = _YAXIS_TITLE_FONT_SIZE
fktemplate.layout.yaxis.title.standoff = _YAXIS_TITLE_STANDOFF

# MAPBOX
fktemplate.layout.mapbox = dict(
    bearing=0,
    style="carto-positron",
    zoom=3.8,
    pitch=0,
    accesstoken=appConfig.APP.MAPBOX_TOKEN,
)

# SUBPLOTS
# ANNOTATION
fktemplate.layout.annotationdefaults.font.color = fktemplate.layout.font.color

# LAYOUT BAR
fktemplate.layout.barmode = "stack"
fktemplate.layout.bargap = 0

# =============
# PLOT SPECIFIC
# =============

# HEATMAP
fktemplate.data.heatmap[0].textfont.family = _FONT_FAMILY
fktemplate.data.heatmap[0].colorscale = "BlackBody"
fktemplate.data.heatmap[0].colorbar.outlinecolor = "black"
fktemplate.data.heatmap[0].colorbar.outlinewidth = 2
fktemplate.data.heatmap[0].colorbar.ticksuffix = "%"
fktemplate.data.heatmap[0].colorbar.x = 1
fktemplate.data.heatmap[0].colorbar.xpad = 10
fktemplate.data.heatmap[0].colorbar.y = 0.5
fktemplate.data.heatmap[0].colorbar.ypad = 20


# SCATTERMAPBOX
fktemplate.data.scattermapbox = [
    go.Scattermapbox(
        mode="markers",
        hovertemplate="%{customdata} - %{text}<br>(%{lat:.5f}, %{lon:.5f})<extra></extra>",
    )
]
