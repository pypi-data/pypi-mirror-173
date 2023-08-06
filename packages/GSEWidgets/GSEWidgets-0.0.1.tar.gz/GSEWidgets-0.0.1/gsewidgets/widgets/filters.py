#!/usr/bin/python3
# ----------------------------------------------------------------------
# GSEWidgets - Collection of gui widgets to be used in GSE software.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2022  GSECARS, The University of Chicago, USA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from pathlib import Path
from qtpy.QtCore import QObject, QEvent
from qtpy.QtWidgets import QLineEdit
from typing import Optional

__all__ = {"FileNameEventFilter", "FilePathEventFilter"}


class FileNameEventFilter(QObject):
    """Used to create file name focus out event filters to replace invalid characters with underscores."""

    def __init__(self, invalid_characters: Optional[str] = '<>"/\\|?*#&$: ') -> None:
        super(FileNameEventFilter, self).__init__()

        self._invalid_characters = invalid_characters

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter file name on focus out events."""
        if event.type() == QEvent.FocusOut:
            # Validate string
            text = widget.text()
            for character in self._invalid_characters:
                text = text.replace(character, "_")
            # Replace old text with the validated text
            widget.setText(text)

        return False


class FilePathEventFilter(FileNameEventFilter):
    """Used to create file path focus out event filters to replace invalid characters with underscores."""

    def __init__(self, invalid_characters: Optional[str] = '<>"|?*#&$: ') -> None:
        super(FilePathEventFilter, self).__init__(invalid_characters=invalid_characters)

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        """Filter file path on focus out events."""
        super(FilePathEventFilter, self).eventFilter(widget=widget, event=event)
        if event.type() == QEvent.FocusOut:
            text = widget.text()
            # Check/create file path
            file_path = Path(text)
            if not file_path.exists():
                file_path.mkdir(parents=True)
            # Replace the text with a PosixPath
            widget.setText(f"{file_path.as_posix()}/")
        return False
