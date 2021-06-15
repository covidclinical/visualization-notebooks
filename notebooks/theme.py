"""
Helpers to apply high-level themes to altair charts.
"""
def apply_theme(
    base,
    title_dy=-10,
    title_anchor="middle",
    title_font_size=22,
    subtitle_font_size=16,
    axis_title_font_size=16,
    axis_y_title_font_size=16,
    axis_label_font_size=14,
    axis_title_padding=10,
    axis_tick_color='white',
    axis_domain_width=1.5,
    label_angle=0,
    legend_orient="right",
    legend_title_orient="top",
    legend_stroke_color="lightgray",
    legend_padding=10,
    legend_symbol_type="circle",
    legend_title_font_size=16,
    label_font_size=14,
    header_label_font_size=13,
    header_label_orient='bottom',
    point_size=70
):
    return base.configure(
        font='Roboto Condensed',
    ).configure_header(
        titleFontSize=16,
        titleFontWeight='bold',
        labelOrient=header_label_orient,
        labelFontSize=header_label_font_size
    ).configure_title(
        fontSize=title_font_size,
        subtitleFontSize=subtitle_font_size,
        fontWeight=500,
        anchor=title_anchor,
        align="left",
        dy=title_dy,
        subtitlePadding=5
    ).configure_axis(
        # domainWidth=2,
        labelFontSize=axis_label_font_size,
        labelFontWeight=300,
        titleFontSize=axis_title_font_size,
        titleFontWeight=400,
        labelLimit=1000,
        titlePadding=axis_title_padding,
        tickColor=axis_tick_color,
        domainWidth=axis_domain_width,
        domainColor='black'
        # labelAngle=label_angle
    ).configure_axisX(
        labelAngle=0
    ).configure_axisY(
        titleFontSize=axis_y_title_font_size,
        domain=False
    ).configure_legend(
        titleFontSize=legend_title_font_size,
        titleFontWeight=400,
        labelFontSize=label_font_size,
        labelFontWeight=300,
        padding=legend_padding,
        cornerRadius=0,
        orient=legend_orient,
        fillColor="white",
        symbolStrokeWidth=2,
        strokeColor=legend_stroke_color,
        symbolType=legend_symbol_type,
        titleOrient=legend_title_orient,
        gradientLength=50
    ).configure_concat(
        spacing=0
    ).configure_view(
        fill='#F3F5F5',
        strokeWidth=0
        # stroke='black'
        # strokeWidth=2
    ).configure_point(
        size=point_size
    )