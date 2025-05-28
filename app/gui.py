import os
import wx
import wx.lib.agw.gradientbutton as GB
from block import BlockingManager
from utils import copy_file
from utils import format_quote
from utils import get_hosts_path
from utils import get_quote
from utils import is_valid_site

LOGO_PATH = "logo.png"
ICON_PATH = "icon.ico"
MOUNTAIN_SHADOW = wx.Colour(42, 93, 116)
MOUNTAIN_SHADE = wx.Colour(78, 129, 146)
MOUNTAIN_SKY = wx.Colour(7, 38, 61)
MOUNTAIN_SNOW = wx.Colour(245, 235, 223)


class BlockingApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        # --- Initialization ---
        self.hosts = get_hosts_path()
        self._copy_original_hosts(self.hosts)
        self.blocking_manager = BlockingManager(self.hosts)

        self.panel = wx.Panel(self)

        # --- Minimum frame size ---
        min_width = 450
        min_height = 550
        self.SetMinSize((min_width, min_height))

        # --- Logo/Image ---
        img = wx.Image(LOGO_PATH, wx.BITMAP_TYPE_ANY)
        # Resize the image if it's too large
        max_logo_height = 100
        if img.GetHeight() > max_logo_height:
            new_width = int(img.GetWidth() * max_logo_height / img.GetHeight())
            img.Rescale(new_width, max_logo_height, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(img)
        self.logo_ctrl = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)

        # --- Icon ---
        icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # --- Font ---
        self.button_font = wx.Font(
            10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        self.text_font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.quote_font = wx.Font(
            12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )

        # --- Quote ---
        quote = format_quote(full_quote=get_quote(), words_per_line=7)
        self.quote = wx.StaticText(
            self.panel,
            label=quote,
            size=(-1, 60),
            style=wx.ALIGN_CENTER,
        )
        self.quote.SetFont(self.quote_font)

        # --- Block Input ---
        self.block_input = wx.TextCtrl(self.panel, wx.ID_ANY, size=(-1, 30))
        self.block_input.SetForegroundColour(MOUNTAIN_SKY)
        self.block_input.SetFont(self.text_font)

        # --- Block Button ---
        self.block_button = GB.GradientButton(self.panel, label="Block", size=(60, 30))
        self._colour_gradient_button(self.block_button)
        self.block_button.SetFont(self.button_font)
        self.block_button.Bind(wx.EVT_BUTTON, self.on_block_button)

        # --- Selection Block ---
        self.blocked_list = wx.ListBox(
            self.panel,
            wx.ID_ANY,
            choices=self.blocking_manager.get_blocked_sites(),
            style=wx.LB_MULTIPLE,
        )
        self.blocked_list.SetForegroundColour(MOUNTAIN_SKY)
        self.blocked_list.SetFont(self.text_font)
        self.blocked_list.SetMaxClientSize

        # --- Unblock Button ---
        self.unblock_button = GB.GradientButton(
            self.panel, label="Unblock", size=(70, 30)
        )
        self._colour_gradient_button(self.unblock_button)
        self.unblock_button.SetFont(self.button_font)
        self.unblock_button.Bind(wx.EVT_BUTTON, self.on_unblock_button)

        # --- Unblock all Button ---
        self.unblock_all_button = GB.GradientButton(
            self.panel, label="Unblock all", size=(85, 30)
        )
        self._colour_gradient_button(self.unblock_all_button)
        self.unblock_all_button.SetFont(self.button_font)
        self.unblock_all_button.Bind(wx.EVT_BUTTON, self.on_unblock_all_button)

        self._do_layout()

    def _copy_original_hosts(self, hosts_file):
        if not os.path.exists(r"../data/original_hosts"):
            try:
                copy_file(hosts_file, r"../data/original_hosts")
            except Exception as e:
                print(f"An error occured during copy: {e}")

    def _colour_gradient_button(self, button):
        button.SetTopStartColour(MOUNTAIN_SKY)
        button.SetTopEndColour(MOUNTAIN_SKY)
        button.SetBottomStartColour(MOUNTAIN_SKY)
        button.SetBottomEndColour(MOUNTAIN_SKY)
        button.SetForegroundColour(MOUNTAIN_SNOW)
        button.SetPressedTopColour(MOUNTAIN_SHADOW)
        button.SetPressedBottomColour(MOUNTAIN_SHADOW)

    def _do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Logo in the center top
        logo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        logo_sizer.AddStretchSpacer(1)
        logo_sizer.Add(self.logo_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.CENTER, 10)
        logo_sizer.AddStretchSpacer(1)
        main_sizer.Add(logo_sizer, 0, wx.CENTER | wx.EXPAND | wx.ALL)

        # Quote
        main_sizer.Add(self.quote, 0, wx.CENTER | wx.EXPAND | wx.ALL, 30)

        # Block input and button in a row
        block_sizer = wx.BoxSizer(wx.HORIZONTAL)
        block_sizer.Add(self.block_input, 1, wx.ALL, 5)
        block_sizer.Add(self.block_button, 0, wx.ALL, 5)
        main_sizer.Add(block_sizer, 0, wx.EXPAND)

        # Selection block - takes full width
        main_sizer.Add(self.blocked_list, 1, wx.EXPAND | wx.ALL, 5)

        # Unblock buttons at the bottom left
        unblock_sizer = wx.BoxSizer(wx.HORIZONTAL)
        unblock_sizer.Add(self.unblock_button, 0, wx.ALL, 5)
        unblock_sizer.Add(self.unblock_all_button, 0, wx.ALL, 5)
        main_sizer.Add(unblock_sizer, 0, wx.ALIGN_LEFT | wx.BOTTOM | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def on_block_button(self, event):
        site_to_block = self.block_input.GetValue().strip()
        if not site_to_block:
            wx.MessageBox(
                "Please enter a website to block.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )
        elif site_to_block in self.blocking_manager.get_blocked_sites():
            wx.MessageBox(
                f"{site_to_block} is already in the block list.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )
        elif not is_valid_site(site_to_block):
            wx.MessageBox(
                f"{site_to_block} is not a valid site.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )
        else:
            self.blocking_manager.block(site_to_block)
            self.blocked_list.Set(self.blocking_manager.get_blocked_sites())
            self.block_input.SetValue("")

    def on_unblock_button(self, event):
        selected_indices = self.blocked_list.GetSelections()
        if not selected_indices:
            wx.MessageBox(
                "Please select one or more websites to unblock.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )
        else:
            sites_to_unblock = [
                self.blocked_list.GetString(i) for i in reversed(selected_indices)
            ]
            for site in sites_to_unblock:
                self.blocking_manager.unblock(site)
            self.blocked_list.Set(self.blocking_manager.get_blocked_sites())

    def on_unblock_all_button(self, event):
        sites_to_unblock = self.blocked_list.GetItems()
        if sites_to_unblock > 0:
            dlg = wx.MessageDialog(
                self,
                "Are you sure you want to unblock all websites?",
                "Confirm Unblock All",
                wx.YES_NO | wx.ICON_QUESTION,
            )
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                for site in sites_to_unblock:
                    self.blocking_manager.unblock(site)
                    self.blocked_list.Set(self.blocking_manager.get_blocked_sites())
            dlg.Destroy()
        else:
            wx.MessageBox(
                "The block list is empty.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )


def run_gui():
    app = wx.App()
    frame = BlockingApp(None, "Blanc")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    run_gui()
