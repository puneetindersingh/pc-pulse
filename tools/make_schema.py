#!/usr/bin/env python3
"""Generates settings-schema.json for the PC Pulse applet."""
import json, sys

TYPES = {
    "Claude weekly limit": "claude_week", "Claude 5 hour limit": "claude_5h",
    "Uptime": "uptime", "CPU usage": "cpu", "CPU temperature": "cpu_temp",
    "Load average": "load", "RAM": "ram", "Swap": "swap", "GPU usage": "gpu",
    "GPU temperature": "gpu_temp", "GPU memory (VRAM)": "vram",
    "Disk space": "disk", "Disk read+write": "disk_io",
    "Network download": "net_down", "Network upload": "net_up",
    "Battery (laptop)": "battery", "Bluetooth / wireless device battery": "device_bat", "Weather": "weather", "Clock / date": "clock", "Custom command": "custom",
}
STYLES = {"Default for type": "auto", "Ring": "ring", "Bar": "bar",
          "Graph (history)": "graph", "Weather icon": "weather", "Clock face": "clock", "Text only": "text"}

def w(on, t, style="auto", label="", color="", arg=""):
    return {"enabled": on, "type": t, "label": label, "style": style, "color": color, "arg": arg}

DEFAULT_WIDGETS = [
    w(True, "claude_week", "ring", "", "#D97757"),
    w(True, "uptime"),
    w(True, "cpu", "graph", "", "#5AA9FF"),
    w(True, "ram", "ring", "", "#B48CFF"),
    w(True, "gpu", "ring", "", "#4CD6A0"),
    w(False, "weather", "auto", "", "#FFD54F", ""),
    w(False, "device_bat", "ring", "", "#81C784", ""),
    w(False, "claude_5h", "ring", "", "#D97757"),
    w(False, "cpu_temp", "bar", "", "#FF8A65"),
    w(False, "gpu_temp", "bar", "", "#4CD6A0"),
    w(False, "vram", "ring", "", "#26C6DA"),
    w(False, "swap", "ring", "", "#9575CD"),
    w(False, "load", "graph", "", "#FFD54F"),
    w(False, "disk", "bar", "", "#90A4AE", "/"),
    w(False, "disk_io", "graph", "", "#F06292"),
    w(False, "net_down", "graph", "", "#4FC3F7"),
    w(False, "net_up", "graph", "", "#AED581"),
    w(False, "battery", "ring", "", "#81C784"),
    w(False, "clock", "text", "", "", "%H:%M"),
    w(False, "custom", "text", "KERNEL", "", "uname -r"),
]

def color(desc, default, tip=None):
    d = {"type": "colorchooser", "default": default, "description": desc}
    if tip: d["tooltip"] = tip
    return d

def spin(desc, default, lo, hi, step=1, units="", tip=None):
    d = {"type": "spinbutton", "default": default, "min": lo, "max": hi, "step": step,
         "units": units, "description": desc}
    if tip: d["tooltip"] = tip
    return d

def sw(desc, default, tip=None):
    d = {"type": "switch", "default": default, "description": desc}
    if tip: d["tooltip"] = tip
    return d

def combo(desc, default, opts):
    return {"type": "combobox", "default": default, "options": opts, "description": desc}

def entry(desc, default, tip=None):
    d = {"type": "entry", "default": default, "description": desc}
    if tip: d["tooltip"] = tip
    return d

s = {
    "layout": {
        "type": "layout",
        "pages": ["pg_widgets", "pg_look", "pg_text", "pg_behaviour"],
        "pg_widgets": {"type": "page", "title": "Widgets", "sections": ["sec_widgets"]},
        "pg_look": {"type": "page", "title": "Background", "sections": ["sec_glass", "sec_shape", "sec_graphics"]},
        "pg_text": {"type": "page", "title": "Text and colours", "sections": ["sec_text", "sec_alerts"]},
        "pg_behaviour": {"type": "page", "title": "Behaviour", "sections": ["sec_update", "sec_click", "sec_claude", "sec_weather", "sec_devices"]},
        "sec_widgets": {"type": "section", "title": "Widgets in the strip, left to right. Add, remove, reorder and edit them here.",
                        "keys": ["widgets", "widgets_help"]},
        "sec_glass": {"type": "section", "title": "Glass",
                      "keys": ["glass_on", "glass_top", "glass_bottom", "glass_opacity", "border_color", "border_width", "shadow_on"]},
        "sec_shape": {"type": "section", "title": "Shape and spacing",
                      "keys": ["strip_height", "v_offset", "radius", "pad_x", "pad_y", "seg_spacing", "separators", "separator_color"]},
        "sec_graphics": {"type": "section", "title": "Rings, bars and graphs",
                         "keys": ["gfx_size", "ring_width", "bar_width", "graph_width", "graph_points", "track_color", "graph_fill"]},
        "sec_text": {"type": "section", "title": "Text",
                     "keys": ["font_family", "show_captions", "caption_size", "caption_color", "value_size", "value_color", "value_min_width", "text_shadow", "show_units"]},
        "sec_alerts": {"type": "section", "title": "Alert colours (percent widgets and temperatures in °C)",
                       "keys": ["warn_at", "warn_color", "hot_at", "hot_color", "color_value_text"]},
        "sec_update": {"type": "section", "title": "Updating",
                       "keys": ["refresh_ms", "smooth_samples", "custom_every"]},
        "sec_click": {"type": "section", "title": "Clicks",
                      "keys": ["drag_reorder", "left_click", "middle_click", "custom_click_cmd", "menu_details", "menu_toggles"]},
        "sec_claude": {"type": "section", "title": "Claude Code",
                       "keys": ["claude_file", "claude_stale_hours", "claude_show_reset", "stats_cmd"]},
        "sec_weather": {"type": "section", "title": "Weather (Open-Meteo, no key needed)",
                        "keys": ["weather_units", "weather_every", "weather_caption"]},
        "sec_devices": {"type": "section", "title": "Wireless device batteries",
                        "keys": ["logi_enabled", "logi_every"]},
    },
    "widgets": {
        "type": "list", "description": "Widgets", "height": 420,
        "columns": [
            {"id": "enabled", "title": "On", "type": "boolean", "default": True},
            {"id": "type", "title": "Widget", "type": "string", "options": TYPES, "default": "cpu"},
            {"id": "style", "title": "Style", "type": "string", "options": STYLES, "default": "auto"},
            {"id": "label", "title": "Caption (blank = default)", "type": "string", "default": ""},
            {"id": "color", "title": "Colour (#hex, blank = default)", "type": "string", "default": ""},
            {"id": "arg", "title": "Option", "type": "string", "default": ""},
        ],
        "default": DEFAULT_WIDGETS,
    },
    "widgets_help": {"type": "label", "description":
        "Option column: Disk space = mount path (/). Network = interface (blank = all). "
        "Battery (laptop) = device name from /sys/class/power_supply (blank = first). "
        "Bluetooth / wireless device battery = part of the device name, for example NuPhy or MX Vertical (blank = first found; hover the widget to see names). "
        "Weather = latitude,longitude, for example 51.51,-0.13 (fetched from Open-Meteo). Clock = strftime format (%H:%M, %a %d). "
        "Custom command = shell command; first line of output is shown, a bare number 0 to 100 also fills the ring. "
        "CPU/GPU temperature = hwmon sensor name to force (k10temp, coretemp, amdgpu)."},

    "glass_on": sw("Glass background", True),
    "glass_top": color("Glass colour, top", "rgb(150,165,200)"),
    "glass_bottom": color("Glass colour, bottom", "rgb(70,82,115)"),
    "glass_opacity": {"type": "scale", "default": 60, "min": 0, "max": 100, "step": 1, "show-value": True,
                      "description": "Glass opacity (%)"},
    "border_color": color("Border colour", "rgba(255,255,255,0.38)"),
    "border_width": spin("Border width", 1, 0, 4, 1, "px"),
    "shadow_on": sw("Top highlight line", True),
    "strip_height": spin("Strip height (0 = panel height minus 8 px)", 0, 0, 120, 1, "px"),
    "v_offset": spin("Vertical nudge (negative = up)", 0, -10, 10, 1, "px"),
    "radius": spin("Corner radius", 15, 0, 30, 1, "px"),
    "pad_x": spin("Inner padding, sides", 10, 0, 30, 1, "px"),
    "pad_y": spin("Inner padding, top and bottom", 0, 0, 10, 1, "px"),
    "seg_spacing": spin("Space between widgets", 4, 0, 30, 1, "px"),
    "separators": sw("Dividers between widgets", True),
    "separator_color": color("Divider colour", "rgba(255,255,255,0.30)"),
    "gfx_size": spin("Ring size", 22, 12, 34, 1, "px"),
    "ring_width": spin("Ring thickness", 3.2, 1, 8, 0.2, "px"),
    "bar_width": spin("Bar length", 34, 12, 80, 1, "px"),
    "graph_width": spin("Graph width", 34, 16, 120, 1, "px"),
    "graph_points": spin("Graph history", 40, 10, 300, 5, "samples"),
    "track_color": color("Empty track colour", "rgba(0,0,0,0.28)"),
    "graph_fill": sw("Fill under graphs", True),
    "font_family": entry("Font (blank = theme font)", "", "Any installed font, for example Inter, Ubuntu, JetBrains Mono"),
    "show_captions": sw("Show captions above values", True),
    "caption_size": spin("Caption size", 7, 5, 14, 0.5, "pt"),
    "caption_color": color("Caption colour", "rgba(255,255,255,0.80)"),
    "value_size": spin("Value size", 10, 6, 20, 0.5, "pt"),
    "value_color": color("Value colour", "rgb(255,255,255)"),
    "value_min_width": spin("Value minimum width (stops jitter)", 34, 0, 120, 1, "px"),
    "text_shadow": sw("Text shadow", True),
    "show_units": sw("Show units (%, °C, GB)", True),
    "warn_at": spin("Warning from", 75, 1, 100, 1, ""),
    "warn_color": color("Warning colour", "rgb(255,179,71)"),
    "hot_at": spin("Critical from", 90, 1, 100, 1, ""),
    "hot_color": color("Critical colour", "rgb(255,107,107)"),
    "color_value_text": sw("Colour the value text too", True),
    "refresh_ms": spin("Refresh every", 1000, 250, 10000, 250, "ms"),
    "smooth_samples": spin("GPU smoothing", 3, 1, 20, 1, "samples", "The AMD busy counter jumps a lot; the strip shows the mean of this many readings"),
    "custom_every": spin("Run custom commands every", 30, 1, 3600, 1, "s"),
    "left_click": combo("Left click", "menu", {"Open the menu": "menu", "Open Claude stats page": "stats",
                                                 "Open system monitor": "sysmon", "Open settings": "settings", "Run custom command": "custom"}),
    "middle_click": combo("Middle click", "sysmon", {"Nothing": "none", "Open Claude stats page": "stats",
                                                      "Open system monitor": "sysmon", "Open settings": "settings", "Run custom command": "custom"}),
    "custom_click_cmd": entry("Custom click command", "gnome-system-monitor"),
    "menu_details": sw("Menu shows live details", True),
    "menu_toggles": sw("Menu shows on/off switches for widgets", True),
    "claude_file": entry("Limits file (blank = auto)", "",
                         "JSON with rate_limits.seven_day / five_hour, written by the bundled claude-statusline.py (see README). Auto reads ~/.cache/pc-pulse/claude-limits.json"),
    "claude_stale_hours": spin("Dim the figure when older than", 6, 1, 168, 1, "h"),
    "claude_show_reset": sw("Show time to reset in the caption", True),
    "drag_reorder": sw("Drag widgets in the panel to reorder them", True, "Hold left click on a widget, drag it sideways, let go"),
    "logi_enabled": sw("Read exact % from Logitech devices (HID++)", True,
                       "The Linux driver gives only Full/High/Low for some Logitech mice; this asks the device itself through the receiver"),
    "logi_every": spin("Check Logitech devices every", 5, 1, 60, 1, "min"),
    "weather_units": combo("Units", "celsius", {"Celsius, km/h": "celsius", "Fahrenheit, mph": "fahrenheit"}),
    "weather_every": spin("Update weather every", 15, 5, 180, 5, "min"),
    "weather_caption": combo("Weather caption", "condition", {"Condition (Partly cloudy)": "condition",
                                "Feels like": "feels", "Today low / high": "range", "Plain caption": "plain"}),
    "stats_cmd": entry("Stats page command (optional)", "", "A command that opens your own usage stats page; adds a menu entry and a click action"),
}
json.dump(s, open(sys.argv[1], "w"), indent=2, ensure_ascii=False)
print("ok", len(s))
