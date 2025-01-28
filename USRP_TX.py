#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: USRP TX
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import blocks, gr
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import USRP_TX_epy_block_2 as epy_block_2  # embedded python block
import sip



class USRP_TX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "USRP TX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("USRP TX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "USRP_TX")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0 = '0'
        self.samp_rate = samp_rate = int(8e6)
        self.gain = gain = 11
        self.cos_freq = cos_freq = 1e6
        self.carrier_freq = carrier_freq = 915e6

        ##################################################
        # Blocks
        ##################################################

        self._variable_qtgui_entry_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_entry_0_tool_bar.addWidget(Qt.QLabel("'variable_qtgui_entry_0'" + ": "))
        self._variable_qtgui_entry_0_line_edit = Qt.QLineEdit(str(self.variable_qtgui_entry_0))
        self._variable_qtgui_entry_0_tool_bar.addWidget(self._variable_qtgui_entry_0_line_edit)
        self._variable_qtgui_entry_0_line_edit.returnPressed.connect(
            lambda: self.set_variable_qtgui_entry_0(str(str(self._variable_qtgui_entry_0_line_edit.text()))))
        self.top_layout.addWidget(self._variable_qtgui_entry_0_tool_bar)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, "Hello World!", 'Payload', True, True, 'Payload', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_edit_box_msg_0_win)
        self._gain_range = Range(0, 76, 1, 11, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "TX Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.epy_block_2 = epy_block_2.blk(preamble_len=11, syncword="1110010")
        self._cos_freq_range = Range(500e3, 8e6, 1e4, 1e6, 200)
        self._cos_freq_win = RangeWidget(self._cos_freq_range, self.set_cos_freq, "Carrier Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._cos_freq_win)
        self._carrier_freq_range = Range(905e6, 930e6, 1e4, 915e6, 200)
        self._carrier_freq_win = RangeWidget(self._carrier_freq_range, self.set_carrier_freq, "Carrier Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._carrier_freq_win)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_2, 'MSG_In'))
        self.msg_connect((self.epy_block_2, 'Packet'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.blocks_message_strobe_0, 'set_msg'))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "USRP_TX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_entry_0(self):
        return self.variable_qtgui_entry_0

    def set_variable_qtgui_entry_0(self, variable_qtgui_entry_0):
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_entry_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_entry_0)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_cos_freq(self):
        return self.cos_freq

    def set_cos_freq(self, cos_freq):
        self.cos_freq = cos_freq

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq




def main(top_block_cls=USRP_TX, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
