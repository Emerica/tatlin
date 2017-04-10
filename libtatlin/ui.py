# -*- coding: utf-8 -*-
# Copyright (C) 2011 Denis Kobozev
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from __future__ import division

import wx
from wx import glcanvas
import PIL.Image
import PIL.ImageTk
#import EmbeddedIconData as eid

# this variable is set when the app is instantiated so that all the ui elements
# in this module can easily reference the app
app = None


def load_icon(fpath):
    return wx.Icon(fpath, wx.BITMAP_TYPE_PNG)


class ViewButtons(wx.FlexGridSizer):

    def __init__(self, parent):
        super(ViewButtons, self).__init__(3, 3)

        self.btn_front = wx.Button(parent, label='Front')
        self.btn_back  = wx.Button(parent, label='Back')
        self.btn_left  = wx.Button(parent, label='Left')
        self.btn_right = wx.Button(parent, label='Right')

        self.btn_top    = wx.Button(parent, label='Top')
        self.btn_bottom = wx.Button(parent, label='Bottom')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.btn_top,    0, wx.EXPAND)
        vbox.Add(self.btn_bottom, 0, wx.EXPAND)

        self.Add((0, 0),         0, wx.EXPAND)
        self.Add(self.btn_back,  0, wx.EXPAND)
        self.Add((0, 0),         0, wx.EXPAND)
        self.Add(self.btn_left,  0, wx.EXPAND)
        self.Add(vbox,           0, wx.EXPAND)
        self.Add(self.btn_right, 0, wx.EXPAND)
        self.Add((0, 0),         0, wx.EXPAND)
        self.Add(self.btn_front, 0, wx.EXPAND)
        self.Add((0, 0),         0, wx.EXPAND)

        # connect handlers
        self.btn_front.Bind( wx.EVT_BUTTON, self.on_view_front)
        self.btn_back.Bind(  wx.EVT_BUTTON, self.on_view_back)
        self.btn_left.Bind(  wx.EVT_BUTTON, self.on_view_left)
        self.btn_right.Bind( wx.EVT_BUTTON, self.on_view_right)
        self.btn_top.Bind(   wx.EVT_BUTTON, self.on_view_top)
        self.btn_bottom.Bind(wx.EVT_BUTTON, self.on_view_bottom)

    def on_view_front(self, event):
        app.on_view_front()

    def on_view_back(self, event):
        app.on_view_back()

    def on_view_left(self, event):
        app.on_view_left()

    def on_view_right(self, event):
        app.on_view_right()

    def on_view_top(self, event):
        app.on_view_top()

    def on_view_bottom(self, event):
        app.on_view_bottom()


class StlPanel(wx.Panel):

    supported_types = ['stl']

    def __init__(self, parent):
        super(StlPanel, self).__init__(parent)

        self._handlers_connected = False

        #----------------------------------------------------------------------
        # DIMENSIONS
        #----------------------------------------------------------------------

        static_box_dimensions = wx.StaticBox(self, label='Dimensions')
        sizer_dimensions = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        label_x = wx.StaticText(self, label='X:')
        self.entry_x = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        label_x_units = wx.StaticText(self, label='mm')

        label_y = wx.StaticText(self, label='Y:')
        self.entry_y = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        label_y_units = wx.StaticText(self, label='mm')

        label_z = wx.StaticText(self, label='Z:')
        self.entry_z = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        label_z_units = wx.StaticText(self, label='mm')

        label_factor = wx.StaticText(self, label='Factor:')
        self.entry_factor = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)

        grid_dimensions = wx.FlexGridSizer(4, 3, 5, 5)
        grid_dimensions.Add(label_x,           0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.entry_x,      0, wx.EXPAND)
        grid_dimensions.Add(label_x_units,     0, wx.ALIGN_CENTER_VERTICAL)
        grid_dimensions.Add(label_y,           0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.entry_y,      0, wx.EXPAND)
        grid_dimensions.Add(label_y_units,     0, wx.ALIGN_CENTER_VERTICAL)
        grid_dimensions.Add(label_z,           0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.entry_z,      0, wx.EXPAND)
        grid_dimensions.Add(label_z_units,     0, wx.ALIGN_CENTER_VERTICAL)
        grid_dimensions.Add(label_factor,      0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.entry_factor, 0, wx.EXPAND)
        grid_dimensions.AddGrowableCol(1)

        sizer_dimensions.Add(grid_dimensions, 0, wx.EXPAND | wx.ALL, border=5)

        #----------------------------------------------------------------------
        # MOVE
        #----------------------------------------------------------------------

        static_box_move = wx.StaticBox(self, label='Move')
        sizer_move = wx.StaticBoxSizer(static_box_move, wx.VERTICAL)

        self.btn_center = wx.Button(self, label='Center model')

        sizer_move.Add(self.btn_center, 0, wx.EXPAND | wx.ALL, border=5)

        #----------------------------------------------------------------------
        # ROTATE
        #----------------------------------------------------------------------

        static_box_rotate = wx.StaticBox(self, label='Rotate')
        sizer_rotate = wx.StaticBoxSizer(static_box_rotate, wx.VERTICAL)

        self.btn_x_90 = wx.Button(self, label='+90')
        label_rotate_x = wx.StaticText(self, label='X:')
        self.entry_rotate_x = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        sizer_entry_x = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entry_x.Add(self.entry_rotate_x, 1, wx.ALIGN_CENTER_VERTICAL)

        self.btn_y_90 = wx.Button(self, label='+90')
        label_rotate_y = wx.StaticText(self, label='Y:')
        self.entry_rotate_y = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        sizer_entry_y = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entry_y.Add(self.entry_rotate_y, 1, wx.ALIGN_CENTER_VERTICAL)

        self.btn_z_90 = wx.Button(self, label='+90')
        label_rotate_z = wx.StaticText(self, label='Z:')
        self.entry_rotate_z = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        sizer_entry_z = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entry_z.Add(self.entry_rotate_z, 1, wx.ALIGN_CENTER_VERTICAL)

        grid_rotate = wx.FlexGridSizer(3, 3, 5, 5)
        grid_rotate.Add(self.btn_x_90,       0)
        grid_rotate.Add(label_rotate_x,      0, wx.ALIGN_CENTER_VERTICAL)
        grid_rotate.Add(sizer_entry_x,       0, wx.EXPAND)
        grid_rotate.Add(self.btn_y_90,       0)
        grid_rotate.Add(label_rotate_y,      0, wx.ALIGN_CENTER_VERTICAL)
        grid_rotate.Add(sizer_entry_y,       0, wx.EXPAND)
        grid_rotate.Add(self.btn_z_90,       0)
        grid_rotate.Add(label_rotate_z,      0, wx.ALIGN_CENTER_VERTICAL)
        grid_rotate.Add(sizer_entry_z,       0, wx.EXPAND)
        grid_rotate.AddGrowableCol(2)

        sizer_rotate.Add(grid_rotate, 0, wx.EXPAND | wx.ALL, border=5)

        #----------------------------------------------------------------------
        # DISPLAY
        #----------------------------------------------------------------------

        static_box_display = wx.StaticBox(self, label='Display')
        sizer_display = wx.StaticBoxSizer(static_box_display, wx.VERTICAL)

        view_buttons = ViewButtons(self)
        self.check_ortho = wx.CheckBox(self, label='Orthographic projection')
        self.btn_reset_view = wx.Button(self, label='Reset view')

        box_display = wx.BoxSizer(wx.VERTICAL)
        box_display.Add(view_buttons,        0, wx.ALIGN_CENTER | wx.TOP, border=5)
        box_display.Add(self.check_ortho,    0, wx.EXPAND | wx.TOP,       border=5)
        box_display.Add(self.btn_reset_view, 0, wx.EXPAND | wx.TOP,       border=5)

        sizer_display.Add(box_display, 0, wx.EXPAND | wx.ALL, border=5)

        box = wx.BoxSizer(wx.VERTICAL)

        box.Add(sizer_dimensions, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        box.Add(sizer_move,       0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        box.Add(sizer_rotate,     0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        box.Add(sizer_display,    0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)

        self.SetSizer(box)

    def connect_handlers(self):
        if self._handlers_connected:
            return

        #----------------------------------------------------------------------
        # DIMENSIONS
        #----------------------------------------------------------------------

        self.entry_x.Bind(wx.EVT_KILL_FOCUS, self.on_entry_x_focus_out)
        self.entry_x.Bind(wx.EVT_TEXT_ENTER, self.on_entry_x_focus_out)

        self.entry_y.Bind(wx.EVT_KILL_FOCUS, self.on_entry_y_focus_out)
        self.entry_y.Bind(wx.EVT_TEXT_ENTER, self.on_entry_y_focus_out)

        self.entry_z.Bind(wx.EVT_KILL_FOCUS, self.on_entry_z_focus_out)
        self.entry_z.Bind(wx.EVT_TEXT_ENTER, self.on_entry_z_focus_out)

        self.entry_factor.Bind(wx.EVT_KILL_FOCUS, self.on_entry_factor_focus_out)
        self.entry_factor.Bind(wx.EVT_TEXT_ENTER, self.on_entry_factor_focus_out)

        #----------------------------------------------------------------------
        # ROTATE
        #----------------------------------------------------------------------

        self.entry_rotate_x.Bind(wx.EVT_KILL_FOCUS, self.on_entry_rotate_x_focus_out)
        self.entry_rotate_x.Bind(wx.EVT_TEXT_ENTER, self.on_entry_rotate_x_focus_out)

        self.entry_rotate_y.Bind(wx.EVT_KILL_FOCUS, self.on_entry_rotate_y_focus_out)
        self.entry_rotate_y.Bind(wx.EVT_TEXT_ENTER, self.on_entry_rotate_y_focus_out)

        self.entry_rotate_z.Bind(wx.EVT_KILL_FOCUS, self.on_entry_rotate_z_focus_out)
        self.entry_rotate_z.Bind(wx.EVT_TEXT_ENTER, self.on_entry_rotate_z_focus_out)

        self.btn_x_90.Bind(wx.EVT_BUTTON, self.on_x_90_clicked)
        self.btn_y_90.Bind(wx.EVT_BUTTON, self.on_y_90_clicked)
        self.btn_z_90.Bind(wx.EVT_BUTTON, self.on_z_90_clicked)

        #----------------------------------------------------------------------
        # MOVE
        #----------------------------------------------------------------------

        self.btn_center.Bind(wx.EVT_BUTTON, self.on_center_clicked)

        #----------------------------------------------------------------------
        # DISPLAY
        #----------------------------------------------------------------------

        self.check_ortho.Bind(   wx.EVT_CHECKBOX, self.on_set_ortho)
        self.btn_reset_view.Bind(wx.EVT_BUTTON,   self.on_reset_clicked)

        self._handlers_connected = True

    def on_entry_x_focus_out(self, event):
        app.dimension_changed('width', self.entry_x.GetValue())
        event.Skip()

    def on_entry_y_focus_out(self, event):
        app.dimension_changed('depth', self.entry_y.GetValue())
        event.Skip()

    def on_entry_z_focus_out(self, event):
        app.dimension_changed('height', self.entry_z.GetValue())
        event.Skip()

    def on_entry_factor_focus_out(self, event):
        app.scaling_factor_changed(self.entry_factor.GetValue())
        event.Skip()

    def on_entry_rotate_x_focus_out(self, event):
        app.rotation_changed('x', self.entry_rotate_x.GetValue())
        self.model_angle_changed()
        event.Skip()

    def on_entry_rotate_y_focus_out(self, event):
        app.rotation_changed('y', self.entry_rotate_y.GetValue())
        self.model_angle_changed()
        event.Skip()

    def on_entry_rotate_z_focus_out(self, event):
        app.rotation_changed('z', self.entry_rotate_z.GetValue())
        self.model_angle_changed()
        event.Skip()

    def on_x_90_clicked(self, event):
        self.rotate_relative('x', 90)

    def on_y_90_clicked(self, event):
        self.rotate_relative('y', 90)

    def on_z_90_clicked(self, event):
        self.rotate_relative('z', 90)

    def rotate_relative(self, axis, angle):
        current_angle = float(app.get_property('rotation-' + axis))
        angle = current_angle + angle
        app.rotation_changed(axis, angle)
        self.model_angle_changed()

    def set_initial_values(self):
        self._set_size_properties()
        self._set_rotation_properties()

    def _set_size_properties(self):
        self.entry_x.SetValue(app.get_property('width'))
        self.entry_y.SetValue(app.get_property('depth'))
        self.entry_z.SetValue(app.get_property('height'))
        self.entry_factor.SetValue(app.get_property('scaling-factor'))

    def _set_rotation_properties(self):
        self.entry_rotate_x.SetValue(app.get_property('rotation-x'))
        self.entry_rotate_y.SetValue(app.get_property('rotation-y'))
        self.entry_rotate_z.SetValue(app.get_property('rotation-z'))

    def model_size_changed(self):
        self._set_size_properties()

    def model_angle_changed(self):
        self._set_rotation_properties()

    def on_center_clicked(self, event):
        app.on_center_model()

    def on_reset_clicked(self, event):
        app.on_reset_view()

    def on_set_ortho(self, event):
        app.on_set_ortho(event.GetEventObject().GetValue())


class GcodePanel(wx.Panel):

    supported_types = ['gcode']

    def __init__(self, parent):
        super(GcodePanel, self).__init__(parent)

        self._handlers_connected = False

        #----------------------------------------------------------------------
        # DIMENSIONS
        #----------------------------------------------------------------------

        static_box_dimensions = wx.StaticBox(self, label='Dimensions')
        sizer_dimensions = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        label_width = wx.StaticText(self, label='X:')
        self.label_width_value = wx.StaticText(self)

        label_depth = wx.StaticText(self, label='Y:')
        self.label_depth_value = wx.StaticText(self)

        label_height = wx.StaticText(self, label='Z:')
        self.label_height_value = wx.StaticText(self)

        grid_dimensions = wx.GridSizer(3, 2, 5, 5)
        grid_dimensions.Add(label_width,             0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_width_value,  0, wx.ALIGN_CENTER)
        grid_dimensions.Add(label_depth,             0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_depth_value,  0, wx.ALIGN_CENTER)
        grid_dimensions.Add(label_height,            0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_height_value, 0, wx.ALIGN_CENTER)

        sizer_dimensions.Add(grid_dimensions, 0, wx.EXPAND | wx.ALL, border=5)

        #----------------------------------------------------------------------
        # DISPLAY
        #----------------------------------------------------------------------

        static_box_display = wx.StaticBox(self, label='Display')
        sizer_display = wx.StaticBoxSizer(static_box_display, wx.VERTICAL)

        label_layers = wx.StaticText(self, label='Layers')
        self.slider_layers = wx.Slider(self, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.check_arrows = wx.CheckBox(self, label='Show arrows')
        self.check_3d = wx.CheckBox(self, label='3D view')
        view_buttons = ViewButtons(self)
        self.check_ortho = wx.CheckBox(self, label='Orthographic projection')
        self.btn_reset_view = wx.Button(self, label='Reset view')

        box_display = wx.BoxSizer(wx.VERTICAL)
        box_display.Add(label_layers,        0, wx.ALIGN_LEFT)
        box_display.Add(self.slider_layers,  0, wx.EXPAND | wx.TOP, border=5)
        box_display.Add(self.check_arrows,   0, wx.EXPAND | wx.TOP, border=5)
        box_display.Add(self.check_3d,       0, wx.EXPAND | wx.TOP, border=5)
        box_display.Add(view_buttons,        0, wx.ALIGN_CENTER | wx.TOP, border=5)
        box_display.Add(self.check_ortho,    0, wx.EXPAND | wx.TOP, border=5)
        box_display.Add(self.btn_reset_view, 0, wx.EXPAND | wx.TOP, border=5)

        sizer_display.Add(box_display, 0, wx.EXPAND | wx.ALL, border=5)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(sizer_dimensions, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        box.Add(sizer_display,    0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)

        self.SetSizer(box)

    def connect_handlers(self):
        if self._handlers_connected:
            return

        self.slider_layers.Bind( wx.EVT_SCROLL,   self.on_slider_moved)
        self.check_arrows.Bind(  wx.EVT_CHECKBOX, self.on_arrows_toggled)
        self.btn_reset_view.Bind(wx.EVT_BUTTON,   self.on_reset_clicked)
        self.check_3d.Bind(      wx.EVT_CHECKBOX, self.on_set_mode)
        self.check_ortho.Bind(   wx.EVT_CHECKBOX, self.on_set_ortho)

        self._handlers_connected = True

    def on_slider_moved(self, event):
        app.on_layers_changed(event.GetEventObject().GetValue())

    def on_arrows_toggled(self, event):
        app.on_arrows_toggled(event.GetEventObject().GetValue())

    def on_reset_clicked(self, event):
        app.on_reset_view()

    def on_set_mode(self, event):
        val = event.GetEventObject().GetValue()
        self.check_ortho.Enable(val)
        app.on_set_mode(val)

    def on_set_ortho(self, event):
        app.on_set_ortho(event.GetEventObject().GetValue())

    def set_initial_values(self):
        layers_max = app.get_property('layers_range_max')
        if layers_max > 1:
            self.slider_layers.SetRange(1, layers_max)
            self.slider_layers.SetValue(app.get_property('layers_value'))
            self.slider_layers.Show()
        else:
            self.slider_layers.Hide()

        self.check_arrows.SetValue(True) # check the box
        self.check_3d.SetValue(True)

        self.label_width_value.SetLabel(app.get_property('width'))
        self.label_depth_value.SetLabel(app.get_property('depth'))
        self.label_height_value.SetLabel(app.get_property('height'))

    def set_3d_view(self, value):
        self.check_3d.SetValue(value)

class XburnPanel(wx.Panel):
    supported_types = ['gcode']

    def __init__(self, parent):
        super(XburnPanel, self).__init__(parent)
        self.model_file = None
        self._handlers_connected = False

        #----------------------------------------------------------------------
        # DIMENSIONS
        #----------------------------------------------------------------------

        static_box_dimensions = wx.StaticBox(self, label='Original Image')
        self.imageHolder = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        static_box_dimensions = wx.StaticBox(self, label='Filtered Image')
        self.prevHolder = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        self.originalImage = None
        self.originalImageHolder = None

        self.previewImage = None
        self.previewImageHolder = None


        static_box_dimensions = wx.StaticBox(self, label='Filter Settings')
        self.filterHolder = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        self.shadeSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labelshades = wx.StaticText( self, wx.ID_ANY, "Shades", (10, 255), wx.DefaultSize, 0 )
        self.labelshades.Wrap( -1 )
        self.shades = wx.Slider( self, wx.ID_ANY, app.shades, 2, 256,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.shadeinput = wx.TextCtrl(self, wx.ID_ANY,str(app.shades))
        self.filterHolder.Add(self.labelshades, 0, wx.ALL)
        self.shadeSizer.Add(self.shades, 0,  wx.ALL|wx.EXPAND, 5)
        self.shadeSizer.Add(self.shadeinput, 0, wx.ALL)
        self.filterHolder.Add(self.shadeSizer, 0, wx.ALL)
        self.shades.Bind(wx.EVT_SLIDER, self.shadeScroll)


        self.wvSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labelwv = wx.StaticText( self, wx.ID_ANY, "White Value", (10, 255), wx.DefaultSize, 0 )
        self.labelwv.Wrap( -1 )
        self.wv = wx.Slider( self, wx.ID_ANY, app.wv, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.wvinput = wx.TextCtrl(self, wx.ID_ANY,str(app.wv))
        self.filterHolder.Add(self.labelwv, 0, wx.ALL)
        self.wvSizer.Add(self.wv, 0,  wx.ALL|wx.EXPAND, 5)
        self.wvSizer.Add(self.wvinput, 0, wx.ALL)
        self.filterHolder.Add(self.wvSizer, 0, wx.ALL)

        self.previewSkip = wx.CheckBox(self, label = 'Preview skipped White')
        self.previewSkip.SetValue(app.wvpreview)
        self.filterHolder.Add(self.previewSkip, 0, wx.ALL)

        self.wv.Bind(wx.EVT_SLIDER, self.wvScroll)
        self.previewSkip.Bind(wx.EVT_CHECKBOX,self.wvChecked)

        self.apply = wx.Button(self, id=-1, label='Apply Changes')
        self.apply.Bind(wx.EVT_BUTTON, self.generate)
        # optional tooltip
        self.apply.SetToolTip(wx.ToolTip("Click to regenerate main preview and code file."))
        self.filterHolder.Add(self.apply, 0, wx.ALL)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.imageHolder, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        self.box.Add(self.prevHolder, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        self.box.Add(self.filterHolder, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)



        self.SetSizer(self.box)
    def generate(self, e):
        app.open_and_display_file(app.filename, "gcode")

    def wvChecked(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        print val
        #self.wvinput.SetValue(str(val))
        app.wvpreview = val
        self.updateShadesFilter(app.shades)

    def wvScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.wvinput.SetValue(str(val))
        app.wv = val
        self.updateShadesFilter(app.shades)

    def shadeScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.shadeinput.SetValue(str(val))
        app.shades = val
        self.updateShadesFilter(app.shades)

    def connect_handlers(self):
        if self._handlers_connected:
            return

        self._handlers_connected = True


    def set_initial_values(self, image):
        self.image_file = image
        self.originalImage = wx.Image(self.image_file, wx.BITMAP_TYPE_ANY)

        W = self.originalImage.GetWidth()
        H = self.originalImage.GetHeight()

        if W > H:
            self.NewW = 300
            self.NewH = 300 * H / W
        else:
            self.NewH = 200
            self.NewW = 200 * W / H

        self.originalImage = self.originalImage.Scale(self.NewW,self.NewH)
        self.originalImageHolder = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.originalImage ))

        self.imageHolder.Add(self.originalImageHolder, 0, wx.ALL|wx.CENTER, 5)
        aimage = wx.EmptyImage(self.NewW,self.NewH)
        self.previewImageHolder = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(aimage))
        #self.prevHolder.Add(self.previewImageHolder, 0, wx.ALL|wx.CENTER, 5)
        self.prevHolder.Add(self.previewImageHolder, 0, wx.ALL|wx.CENTER, 5)

        self.updateShadesFilter(app.shades)


    def updateShadesFilter(self, value):
        self.previewImage = PIL.Image.open(self.image_file)
        #Do stuff
        #ok.. convert to P with adatptive palette, limit colors to a value
        self.previewImage = self.previewImage.resize((int(self.NewW),int(self.NewH)),PIL.Image.ANTIALIAS)
        self.previewImage = self.previewImage.convert('P', palette=PIL.Image.ADAPTIVE,
            colors=int(value))
        #Then convert that to greyscale.
        self.previewImage = self.previewImage.convert('L')
        if app.wvpreview:
            self.drawSkip()
        aimage = wx.EmptyImage(*self.previewImage.size)
        aimage.SetData(self.previewImage.convert("RGB").tobytes())
        #aimage.SetAlphaData(self.previewImage.convert("RGBA").tobytes()[3::4])
        self.previewImageHolder.SetBitmap(wx.BitmapFromImage(aimage))

        #self.prevHolder.Refresh()

    def drawSkip(self):
        newimage = []
        for pixel in self.previewImage.getdata():
            if int(pixel) >= int(app.wv):
                #Turn it red, #TODO, set a pref option for this color
                newimage.append((255,0,0,0))
            else:
                newimage.append((pixel,pixel,pixel,0))
        self.previewImage = PIL.Image.new('RGB', self.previewImage.size)
        self.previewImage.putdata(newimage)

    def openFile(self):
        pass
        #self.updateShadesFilter(self.shades)

    def updatePreview(self, val=-1):
        #This is a nasty hack for white value preview updates.... FIXME
        if val > -1:
            self.wv = val
        #Create a list to store preview image data
        newimage = []
        #Loop over each pixel
        for pixel in self.result.getdata():
            #if the pixel is whiter that self.wv, turn it red.
            if int(pixel) >= int(self.wv):
                #Turn it red, #TODO, set a pref option for this color
                newimage.append((255,0,0,0))
            else:
                #Use the pixel as is
                newimage.append((pixel,pixel,pixel,0))
        #Make a dummy image to store as RGB
        #Converting leads to issues....
        prev = Image.new('RGB', self.result.size)
        #Put the new array data into the image
        prev.putdata(newimage)
        #Create a tk image
        tkresult = PIL.ImageTk.PhotoImage(prev)
        #Attach it to the preview pane.
        self.preview.configure(image=tkresult)
        self.preview.image=tkresult


class XburnPanel2(wx.Panel):
    supported_types = ['gcode']

    def __init__(self, parent):
        super(XburnPanel2, self).__init__(parent)
        self.model_file = None
        self._handlers_connected = False

        static_box_dimensions = wx.StaticBox(self, label='Machine and Laser Settings')
        self.machineHolder = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        #TODO: change shades as this changes and shades is too high.
        # Warning, auto? I dunno.
        self.stepsSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labelsteps = wx.StaticText( self, wx.ID_ANY, "Total Pwm Steps", (10, 255), wx.DefaultSize, 0 )
        self.labelsteps.Wrap( -1 )
        self.steps = wx.Slider( self, wx.ID_ANY, 255, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.stepsinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labelsteps, 0, wx.ALL)
        self.stepsSizer.Add(self.steps, 0,  wx.ALL|wx.EXPAND, 5)
        self.stepsSizer.Add(self.stepsinput, 0, wx.ALL)
        self.machineHolder.Add(self.stepsSizer, 0, wx.ALL)

        self.laserhighSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labellaserhigh = wx.StaticText( self, wx.ID_ANY, "Laster Max Pwm Value", (10, 255), wx.DefaultSize, 0 )
        self.labellaserhigh.Wrap( -1 )
        self.laserhigh = wx.Slider( self, wx.ID_ANY, 255, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.laserhighinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labellaserhigh, 0, wx.ALL)
        self.laserhighSizer.Add(self.laserhigh, 0,  wx.ALL|wx.EXPAND, 5)
        self.laserhighSizer.Add(self.laserhighinput, 0, wx.ALL)
        self.machineHolder.Add(self.laserhighSizer, 0, wx.ALL)

        self.laserlowSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labellaserlow = wx.StaticText( self, wx.ID_ANY, "Laster Max Pwm Value", (10, 255), wx.DefaultSize, 0 )
        self.labellaserlow.Wrap( -1 )
        self.laserlow = wx.Slider( self, wx.ID_ANY, 255, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.laserlowinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labellaserlow, 0, wx.ALL)
        self.laserlowSizer.Add(self.laserlow, 0,  wx.ALL|wx.EXPAND, 5)
        self.laserlowSizer.Add(self.laserlowinput, 0, wx.ALL)
        self.machineHolder.Add(self.laserlowSizer, 0, wx.ALL)

        self.burnrateSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labelburnrate = wx.StaticText( self, wx.ID_ANY, "Feedrate while burning.", (10, 255), wx.DefaultSize, 0 )
        self.labelburnrate.Wrap( -1 )
        self.burnrate = wx.Slider( self, wx.ID_ANY, 255, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.burnrateinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labelburnrate, 0, wx.ALL)
        self.burnrateSizer.Add(self.burnrate, 0,  wx.ALL|wx.EXPAND, 5)
        self.burnrateSizer.Add(self.burnrateinput, 0, wx.ALL)
        self.machineHolder.Add(self.burnrateSizer, 0, wx.ALL)

        self.skiprateSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labelskiprate = wx.StaticText( self, wx.ID_ANY, "Feedrate while skipping.", (10, 255), wx.DefaultSize, 0 )
        self.labelskiprate.Wrap( -1 )
        self.skiprate = wx.Slider( self, wx.ID_ANY, 255, 0, 255,  wx.DefaultPosition, (200,-1), wx.SL_HORIZONTAL )
        self.skiprateinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labelskiprate, 0, wx.ALL)
        self.skiprateSizer.Add(self.skiprate, 0,  wx.ALL|wx.EXPAND, 5)
        self.skiprateSizer.Add(self.skiprateinput, 0, wx.ALL)
        self.machineHolder.Add(self.skiprateSizer, 0, wx.ALL)

        self.laseronSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labellaseron = wx.StaticText( self, wx.ID_ANY, "Gcode Command for Laser On.", (10, 255), wx.DefaultSize, 0 )
        self.labellaseron.Wrap( -1 )
        self.laseroninput = wx.TextCtrl(self, wx.ID_ANY,'M3')
        self.machineHolder.Add(self.labellaseron, 0, wx.ALL)
        self.laseronSizer.Add(self.laseroninput, 0, wx.ALL)
        self.machineHolder.Add(self.laseronSizer, 0, wx.ALL)


        self.laseroffSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labellaseroff = wx.StaticText( self, wx.ID_ANY, "Gcode Command for Laser Off.", (10, 255), wx.DefaultSize, 0 )
        self.labellaseroff.Wrap( -1 )
        self.laseroffinput = wx.TextCtrl(self, wx.ID_ANY,'M5')
        self.machineHolder.Add(self.labellaseroff, 0, wx.ALL)
        self.laseroffSizer.Add(self.laseroffinput, 0, wx.ALL)
        self.machineHolder.Add(self.laseroffSizer, 0, wx.ALL)


        self.lasermodSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.labellasermod = wx.StaticText( self, wx.ID_ANY, "Gcode Command for Laser Mod.", (10, 255), wx.DefaultSize, 0 )
        self.labellasermod.Wrap( -1 )
        self.lasermodinput = wx.TextCtrl(self, wx.ID_ANY,'')
        self.machineHolder.Add(self.labellasermod, 0, wx.ALL)
        self.lasermodSizer.Add(self.lasermodinput, 0, wx.ALL)
        self.machineHolder.Add(self.lasermodSizer, 0, wx.ALL)


        static_box_dimensions = wx.StaticBox(self, label='Output Settings')
        self.outputHolder = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.machineHolder, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        self.box.Add(self.outputHolder, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)


        self.SetSizer(self.box)
    def connect_handlers(self):
        if self._handlers_connected:
            return

        self._handlers_connected = True


    def set_initial_values(self, ):
        pass



class StartupPanel(wx.Panel):

    def __init__(self, parent):
        super(StartupPanel, self).__init__(parent)

        text = wx.StaticText(self, label='No files loaded')
        self.btn_open = wx.Button(self, wx.ID_OPEN)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((0, 0),        1, wx.EXPAND)
        box.Add(text,          0, wx.ALIGN_CENTER | wx.ALL,                         border=5)
        box.Add(self.btn_open, 0, wx.ALIGN_CENTER | wx.RIGHT | wx.BOTTOM | wx.LEFT, border=5)
        box.Add((0, 0),        1, wx.EXPAND)

        self.SetSizer(box)


class MainWindow(wx.Frame):

    def __init__(self):
        self._app_name = 'Tatlin'

        super(MainWindow, self).__init__(None, title=self._app_name)

        self._file_modified = False
        self._filename = None

        file_menu = wx.Menu()
        item_open = file_menu.Append(wx.ID_OPEN, '&Open', 'Open file')
        self.recent_files_menu = wx.Menu()
        self.recent_files_item = file_menu.AppendMenu(wx.ID_ANY, '&Recent files',
                self.recent_files_menu)
        item_save = file_menu.Append(wx.ID_SAVE, '&Save', 'Save changes')
        item_save.Enable(False)
        item_save_as = file_menu.Append(wx.ID_SAVEAS, 'Save As...\tShift+Ctrl+S',
                'Save under a different filename')
        item_save_as.Enable(False)
        item_quit = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit %s' % self._app_name)

        self.menu_items_file = [item_save, item_save_as]

        help_menu = wx.Menu()
        item_about = help_menu.Append(wx.ID_ABOUT, '&About %s' % self._app_name)

        self.menubar = wx.MenuBar()
        self.menubar.Append(file_menu, '&File')
        self.menubar.Append(help_menu, '&Help')

        self.Bind(wx.EVT_MENU, app.on_file_open, item_open)
        self.Bind(wx.EVT_MENU, app.on_file_save, item_save)
        self.Bind(wx.EVT_MENU, app.on_file_save_as, item_save_as)
        self.Bind(wx.EVT_MENU, app.on_quit, item_quit)
        self.Bind(wx.EVT_MENU, app.on_about, item_about)

        self.box_scene = wx.BoxSizer(wx.HORIZONTAL)

        self.panel_startup = StartupPanel(self)
        self.panel_startup.btn_open.Bind(wx.EVT_BUTTON, app.on_file_open)

        self.box_main = wx.BoxSizer(wx.VERTICAL)
        self.box_main.Add(self.panel_startup, 1, wx.EXPAND)

        self.SetMenuBar(self.menubar)
        self.statusbar = self.CreateStatusBar()
        self.SetSizer(self.box_main)

        # Set minimum frame size so that the widgets contained within are not squashed.
        # I wish there was a reliable way to set the minimum size based on minimum
        # sizes of widgets contained in the frame, but wxPython ignores the dimensions
        # of window decorations (borders and titlebar) in addition to other minor quirks.
        # Hardcoding the minimum size seems no less portable and reliable, and also
        # much easier.
        self.SetSizeHints(400, 700, self.GetMaxWidth(), self.GetMaxHeight())
        self.Center()

        self.Bind(wx.EVT_CLOSE, app.on_quit)
        self.Bind(wx.EVT_ICONIZE, self.on_iconize)
        tb = wx.ToolBar( self, -1 , style=wx.TB_HORIZONTAL|wx.TB_DOCKABLE|wx.TB_3DBUTTONS|wx.TB_TEXT|wx.TB_NODIVIDER|wx.TB_NOALIGN )
        self.ToolBar = tb
        #self.toolbar.AddLabelTool(1, label, wx.Bitmap(imageName))
        topen = tb.AddLabelTool( 101, "Open", wx.Bitmap("icons/open.png"))
        tb.AddLabelTool(102, "Export", wx.Bitmap("icons/save.png"))

        tb.AddSeparator()   # Invisible spacer

        tb.AddLabelTool(103, "3d/2d", wx.Bitmap("icons/globe.png"))
        tb.AddLabelTool(104, "Top View", wx.Bitmap("icons/home.png"))
        tarrows = tb.AddLabelTool(105, "Show Arrows", wx.Bitmap("icons/left.png"))
        self.Bind(wx.EVT_TOOL, app.on_file_open, topen)
        self.Bind(wx.EVT_TOOL, app.on_arrows_toggled, tarrows)
        #self.Bind(wx.EVT_TOOL, app.on_file_open, topen)
        #self.
        #tb.AddTool(106,wx.Bitmap("icons/right.png"))
        #tb.AddTool(107,wx.Bitmap("icons/up.png"))
        #tb.AddTool(107,wx.Bitmap("icons/down.png"))

        tb.AddSeparator()   # Invisible spacer

        # A way to insert a custom separator.
        #import EmbeddedIconData as eid
        #tb.AddControl( wx.StaticBitmap( tb, wx.ID_ANY, eid.GetSeparatorBitmap() ) )

        tb.Realize()

    def on_arrows_toggled(self, event):
        app.on_arrows_toggled()

    def set_icon(self, icon):
        self.SetIcon(icon)

    def quit(self):
        self.Destroy()

    def show_all(self):
        self.Show()

    def get_size(self):
        return self.GetSize()

    def set_size(self, size):
        self.SetSize(size)

    def set_file_widgets(self, scene, panel, panel2):
        # remove startup panel if present
        if self._filename is None:
            self.box_main.Remove(self.panel_startup)
            self.panel_startup.Destroy()

            self.box_main.Add(self.box_scene, 1, wx.EXPAND)

        # remove previous scene and panel, if any, destroying the widgets
        self.box_scene.Clear(True)
        self.box_scene.Add(panel2, 0, wx.EXPAND)
        self.box_scene.Add(scene, 1, wx.EXPAND)

        self.box_scene.Add(panel, 0, wx.EXPAND)
        self.box_scene.ShowItems(True)
        self.Layout() # without this call, wxPython does not draw the new widgets until window resize

    def menu_enable_file_items(self, enable=True):
        for item in self.menu_items_file:
            item.Enable(enable)

    def update_recent_files_menu(self, recent_files):
        for menu_item in self.recent_files_menu.GetMenuItems():
            self.recent_files_menu.DeleteItem(menu_item)

        for recent_file in recent_files:
            item = self.recent_files_menu.Append(wx.ID_ANY, recent_file[0])

            def callback(f, t):
                return lambda x: app.open_and_display_file(f, t)

            self.Bind(wx.EVT_MENU, callback(recent_file[1], recent_file[2]), item)

        self.recent_files_item.Enable(len(recent_files) > 0)

    def update_status(self, text):
        self.statusbar.SetStatusText(text)

    def on_iconize(self, event):
        if not self.IsIconized():
            # call Layout() when the frame is unminimized; otherwise the window
            # will be blank if the frame was minimized while the model was loading
            self.Layout()
        event.Skip()

    @property
    def file_modified(self):
        return self._file_modified

    @file_modified.setter
    def file_modified(self, value):
        self._file_modified = value
        self._title_changed()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self._title_changed()

    def _title_changed(self):
        """Format and set title."""
        title = self._app_name
        if self._filename is not None:
            filename = self._filename
            if self._file_modified:
                filename = '*' + filename
            title = filename + ' - ' + title

        self.SetTitle(title)


class OpenDialog(wx.FileDialog):

    ftypes = (None, 'gcode', 'stl')

    def __init__(self, parent, directory=None):
        super(OpenDialog, self).__init__(parent, 'Open',
                wildcard='Gcode and STL files (*.gcode;*.nc;*.stl)|*.gcode;*.nc;*.stl|Gcode files (*.*)|*.*|STL files (*.*)|*.*',
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if directory is not None:
            self.SetDirectory(directory)

    def get_path(self):
        if self.ShowModal() == wx.ID_CANCEL:
            return None
        return self.GetPath()

    def get_type(self):
        return self.ftypes[self.GetFilterIndex()]


class OpenErrorAlert(wx.MessageDialog):

    def __init__(self, fpath, error):
        msg = "Error opening file %s: %s" % (fpath, error)
        super(OpenErrorAlert, self).__init__(None, msg, 'Error', wx.OK | wx.ICON_ERROR)

    def show(self):
        self.ShowModal()


class SaveDialog(wx.FileDialog):

    def __init__(self, parent, directory=None):
        super(SaveDialog, self).__init__(parent, 'Save As', wildcard='STL files (*.stl)|*.stl',
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if directory is not None:
            self.SetDirectory(directory)

    def get_path(self):
        if self.ShowModal() == wx.ID_CANCEL:
            return None
        return self.GetPath()


class QuitDialog(wx.Dialog):
    RESPONSE_CANCEL  = 0
    RESPONSE_DISCARD = 1
    RESPONSE_SAVE_AS = 2
    RESPONSE_SAVE    = 3

    def __init__(self, parent):
        super(QuitDialog, self).__init__(parent, title='Save changes?')

        label = wx.StaticText(self, label='Save changes to the file before closing?')

        self.btn_discard = wx.Button(self, label='Discard')
        self.btn_cancel  = wx.Button(self, wx.ID_CANCEL)
        self.btn_save_as = wx.Button(self, wx.ID_SAVEAS)
        self.btn_save    = wx.Button(self, wx.ID_SAVE)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_discard, 1)
        hbox.Add(self.btn_cancel,  1, wx.LEFT, border=5)
        hbox.Add(self.btn_save_as, 1, wx.LEFT, border=5)
        hbox.Add(self.btn_save,    1, wx.LEFT, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(label, 1, wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox,  0, wx.EXPAND | wx.ALIGN_BOTTOM | wx.RIGHT | wx.BOTTOM | wx.LEFT, border=5)

        self.SetSizer(vbox)
        self.SetSize((400, 90))

        self.btn_discard.Bind(wx.EVT_BUTTON, self.on_discard)
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.on_cancel)
        self.btn_save_as.Bind(wx.EVT_BUTTON, self.on_save_as)
        self.btn_save.Bind(   wx.EVT_BUTTON, self.on_save)

    def on_discard(self, event):
        self.EndModal(self.RESPONSE_DISCARD)

    def on_cancel(self, event):
        self.EndModal(self.RESPONSE_CANCEL)

    def on_save_as(self, event):
        self.EndModal(self.RESPONSE_SAVE_AS)

    def on_save(self, event):
        self.EndModal(self.RESPONSE_SAVE)

    def show(self):
        return self.ShowModal()


class ProgressDialog(wx.ProgressDialog):

    def __init__(self, text):
        super(ProgressDialog, self).__init__('Loading', text, 100)

        self.value = 0

    def step(self, count, limit):
        self.value = max(0, min(int(count / limit * 100), 100))
        self.Update(self.value)

    def hide(self):
        self.Hide()

    def destroy(self):
        self.Destroy()


class AboutDialog(object):

    def __init__(self):
        from datetime import datetime

        info = wx.AboutDialogInfo()

        info.SetName('Tatlin')
        info.SetVersion('v%s' % app.TATLIN_VERSION)
        info.SetIcon(app.icon)
        info.SetDescription('Gcode and STL viewer for 3D printing')
        info.SetCopyright('(C) 2011-%s Denis Kobozev' % datetime.strftime(datetime.now(), '%Y'))
        info.SetWebSite('http://dkobozev.github.io/tatlin/')
        info.AddDeveloper('Denis Kobozev <d.v.kobozev@gmail.com>')
        info.SetLicence(app.TATLIN_LICENSE)

        dialog = wx.AboutBox(info)


class BaseScene(glcanvas.GLCanvas):

    def __init__(self, parent):
        super(BaseScene, self).__init__(parent, -1, size=(128, 128))
        self.Hide()

        self.initialized = False
        self.context = glcanvas.GLContext(self)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self._on_erase_background)
        self.Bind(wx.EVT_SIZE,             self._on_size)
        self.Bind(wx.EVT_PAINT,            self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN,        self._on_mouse_down)
        self.Bind(wx.EVT_MOTION,           self._on_mouse_motion)

        # make it unnecessary for the scene to be in focus to respond to the
        # mouse wheel by binding the mouse wheel event to the parent; if we
        # bound the event to the scene itself, the user would have to click on
        # the scene before scrolling each time the scene loses focus (users who
        # have the fortune of being able to use a window manager that has a
        # setting for focus-follows-mouse wouldn't care either way, since their
        # wm would handle it for them)
        parent.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)

        methods = ['init', 'display', 'reshape', 'button_press', 'button_motion', 'wheel_scroll']
        for method in methods:
            if not hasattr(self, method):
                raise Exception('Method %s() is not implemented' % method)

    def invalidate(self):
        self.Refresh(False)

    def _on_erase_background(self, event):
        pass # Do nothing, to avoid flashing on MSW. Doesn't seem to be working, though :(

    def _on_size(self, event):
        wx.CallAfter(self._set_viewport)
        event.Skip()

    def _set_viewport(self):
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        self.reshape(size.width, size.height)

    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)

        if not self.initialized:
            self.init()
            self.initialized = True

        size = self.GetClientSize()
        self.display(size.width, size.height)

        self.SwapBuffers()

    def _on_mouse_down(self, event):
        self.SetFocus()
        x, y = event.GetPosition()
        self.button_press(x, y)

    def _on_mouse_motion(self, event):
        x, y = event.GetPosition()

        left   = event.LeftIsDown()
        middle = event.MiddleIsDown()
        right  = event.RightIsDown()

        self.button_motion(x, y, left, middle, right)

    def _on_mouse_wheel(self, event):
        self.wheel_scroll(event.GetWheelRotation())


class BaseApp(wx.App):

    def __init__(self):
        super(BaseApp, self).__init__()

        global app
        app = self

    def run(self):
        self.MainLoop()

    def process_ui_events(self):
        self.Yield()

    def set_wait_cursor(self):
        wx.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))

    def set_normal_cursor(self):
        wx.SetCursor(wx.NullCursor)


class TestApp(BaseApp):

    def __init__(self):
        super(TestApp, self).__init__()

        self.window = MainWindow()
        self.window.show_all()

    def show_gcode_mode(self):
        glarea = wx.Panel(self.window)
        glarea.SetBackgroundColour((0, 0, 0))
        panel = GcodePanel(self.window)
        self.window.set_file_widgets(glarea, panel)

    def show_stl_mode(self):
        glarea = wx.Panel(self.window)
        glarea.SetBackgroundColour((0, 0, 0))
        panel = StlPanel(self.window)
        self.window.set_file_widgets(glarea, panel)

    def enable_file_menus(self):
        self.window.menu_enable_file_items()

    def on_file_open(self, event):
        dialog = OpenDialog(self.window)
        path = dialog.get_path()
        #This should now be an image
        print path
        #Run Xburn with last settings and create a workfile
        #lol just load it...? why all the progress bars if,
        if path:
            progress_dialog = ProgressDialog('Loading image')
            import time
            for i in range(10):
                print i
                progress_dialog.step(i, 9)
                time.sleep(0.1)
            progress_dialog.destroy()

            progress_dialog = ProgressDialog('Reading file...')
            import time
            for i in range(10):
                print i
                progress_dialog.step(i, 9)
                time.sleep(0.1)
            progress_dialog.destroy()

            progress_dialog = ProgressDialog('Loading model...')
            for i in range(10):
                print i
                progress_dialog.step(i, 9)
                time.sleep(0.1)
            progress_dialog.destroy()

            if path.endswith('.stl'):
                self.show_stl_mode()
            else:
                self.show_gcode_mode()

    def on_file_save(self, event):
        print 'save'

    def on_file_save_as(self, event):
        print 'save as'

    def on_quit(self, event):
        self.window.Close()

    def on_about(self, event):
        print 'about'


if __name__ == '__main__':
    app = TestApp()
    app.show_stl_mode()
    app.run()
