import platform
from pathlib import Path
from typing import Optional, Dict, Any

from nicegui import events, ui


class BaseFilePicker(ui.dialog):
    """
    Base dialog for navigating the local filesystem and selecting files or folders.

    :param directory: The directory to start in.
    :param title: The dialog title.
    :param allow_files: Whether file selection is permitted.
    :param allow_folders: Whether folder selection is permitted.
    :param multiple: Whether multiple selection is allowed.
    :param show_hidden: Whether hidden files should be shown.
    :param filters: Mapping of allowed file extensions to descriptions.
    """

    def __init__(
            self,
            directory: str,
            *,
            title: str,
            allow_files: bool,
            allow_folders: bool,
            multiple: bool = False,
            show_hidden: bool = False,
            filters: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize a BaseFilePicker.

        :param directory: The path to start browsing.
        :param title: The title displayed at the top of the dialog.
        :param allow_files: Enable selecting files.
        :param allow_folders: Enable selecting folders.
        :param multiple: Allow multiple selections.
        :param show_hidden: Include hidden files in the listing.
        :param filters: File extension filters (e.g. {'.py': 'Python Files'}).
        """
        super().__init__()
        self.path = Path(directory).expanduser()
        self.title = title
        self.allow_files = allow_files
        self.allow_folders = allow_folders
        self.multiple = multiple
        self.show_hidden = show_hidden
        self.filters = set(filters.keys()) if filters else None

        self._init_dialog()
        self._update_grid()

    def _init_dialog(self) -> None:
        with self, ui.card():
            ui.label(self.title).classes('text-lg font-medium')
            if platform.system() == 'Windows':
                import win32api  # type: ignore
                drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
                self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self._change_drive)

            grid_opts: Dict[str, Any] = {
                'columnDefs': [
                    {'field': 'name', 'headerName': 'Name'},
                ],
                'rowSelection': 'multiple' if self.multiple else 'single',
                ':getRowId': '(params) => params.data.path',
            }
            self.grid = ui.aggrid(grid_opts, html_columns=[0]).classes('w-96')
            self.grid.on('cellDoubleClicked', self._on_double_click)

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)

    def _change_drive(self) -> None:
        """
        Change the current path to the selected drive (Windows only).
        """
        self.path = Path(self.drives_toggle.value).expanduser()
        self._update_grid()

    def _update_grid(self) -> None:
        """
        Update the file/folder listing in the grid based on the current path and filters.
        """
        entries = list(self.path.glob('*'))
        if not self.show_hidden:
            entries = [p for p in entries if not p.name.startswith('.')]
        if self.filters is not None:
            entries = [p for p in entries if p.is_dir() or p.suffix in self.filters]
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))

        rows = []
        if self.path.parent != self.path:
            rows.append({'name': '<i class="material-icons">folder_open</i> ..', 'path': str(self.path.parent)})
        for p in entries:
            icon = 'folder' if p.is_dir() else 'insert_drive_file'
            display = (
                f'<i class="material-icons">{icon}</i> <strong>{p.name}</strong>' if p.is_dir()
                else f'<i class="material-icons">{icon}</i> {p.name}'
            )
            rows.append({'name': display, 'path': str(p)})

        self.grid.options['rowData'] = rows
        self.grid.update()

    def _on_double_click(self, e: events.GenericEventArguments) -> None:
        """
        Handle double-click event in the grid to navigate into folders or select files.

        :param e: Event arguments containing the clicked row data.
        """
        selected_path = Path(e.args['data']['path'])
        if selected_path.is_dir():
            self.path = selected_path
            self._update_grid()
        elif self.allow_files:
            self.submit([str(selected_path)])

    async def _handle_ok(self) -> None:
        """
        Handle OK button click: validate selected items and submit them if valid.
        """
        rows = await self.grid.get_selected_rows()
        raw_paths = [r['path'] for r in rows]
        valid_paths: list[str] = []
        invalid_paths: list[str] = []
        for p_str in raw_paths:
            p = Path(p_str)
            if (p.is_file() and self.allow_files) or (p.is_dir() and self.allow_folders):
                valid_paths.append(p_str)
            else:
                invalid_paths.append(p_str)
        if invalid_paths:
            msg = f"Invalid selection: {invalid_paths}. "
            if self.allow_files and not self.allow_folders:
                msg += "Please select files only."
            elif self.allow_folders and not self.allow_files:
                msg += "Please select folders only."
            else:
                msg += "Please select valid items."
            ui.notify(msg, color='negative')
            return
        if not valid_paths:
            ui.notify("No items selected.", color='negative')
            return
        self.submit(valid_paths)


class OpenFilePicker(BaseFilePicker):
    """
    Dialog for selecting one or multiple files with optional filters and custom title.

    :param directory: The directory to start in.
    :param title: Custom dialog title.
    :param multiple: Allow selecting multiple files.
    :param show_hidden: Show hidden files.
    :param filters: File extension filters.
    """

    def __init__(
            self,
            directory: str = '.',
            *,
            title: Optional[str] = None,
            multiple: bool = False,
            show_hidden: bool = False,
            filters: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize an OpenFilePicker.

        :param directory: The starting directory.
        :param title: Custom title (default: 'Open File').
        :param multiple: Enable multiple file selection.
        :param show_hidden: Include hidden files.
        :param filters: File extension filters.
        """
        super().__init__(
            directory,
            title=title or 'Open File',
            allow_files=True,
            allow_folders=False,
            multiple=multiple,
            show_hidden=show_hidden,
            filters=filters,
        )


class OpenFolderPicker(BaseFilePicker):
    """
    Dialog for selecting a single folder with custom title.

    :param directory: The directory to start in.
    :param title: Custom dialog title.
    :param show_hidden: Show hidden folders.
    """

    def __init__(
            self,
            directory: str = '.',
            *,
            title: Optional[str] = None,
            show_hidden: bool = False,
    ) -> None:
        """
        Initialize an OpenFolderPicker.

        :param directory: The starting directory.
        :param title: Custom title (default: 'Open Folder').
        :param show_hidden: Include hidden folders.
        """
        super().__init__(
            directory,
            title=title or 'Open Folder',
            allow_files=False,
            allow_folders=True,
            multiple=False,
            show_hidden=show_hidden,
            filters=None,
        )


class SaveFilePicker(BaseFilePicker):
    """
    Dialog for choosing a directory and entering a file name to save, with overwrite prompt and custom title.

    :param directory: The directory to start in.
    :param title: Custom dialog title.
    :param show_hidden: Show hidden folders.
    :param default_name: The default file name.
    :param filters: File extension filters.
    """

    def __init__(
            self,
            directory: str = '.',
            *,
            title: Optional[str] = None,
            show_hidden: bool = False,
            default_name: str = '',
            filters: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize a SaveFilePicker.

        :param directory: The starting directory.
        :param title: Custom title (default: 'Save File').
        :param show_hidden: Include hidden folders.
        :param default_name: Pre-filled file name input.
        :param filters: File extension filters.
        """
        self.default_name = default_name
        super().__init__(
            directory,
            title=title or 'Save File',
            allow_files=False,
            allow_folders=True,
            multiple=False,
            show_hidden=show_hidden,
            filters=filters,
        )

    def _init_dialog(self) -> None:
        """
        Initialize the dialog UI components including file name input and overwrite logic.
        """
        with self, ui.card():
            ui.label(self.title).classes('text-lg font-medium')
            if platform.system() == 'Windows':
                import win32api  # type: ignore
                drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
                self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self._change_drive)

            grid_opts: Dict[str, Any] = {
                'columnDefs': [
                    {'field': 'name', 'headerName': 'Name'},
                ],
                'rowSelection': 'single',
                ':getRowId': '(params) => params.data.path',
            }
            self.grid = ui.aggrid(grid_opts, html_columns=[0]).classes('w-96')
            self.grid.on('cellDoubleClicked', self._on_double_click)

            self.name_input = ui.input(label='File name', value=self.default_name).classes('w-full').props('solo')

            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)

    async def _handle_ok(self) -> None:
        """
        Handle OK button click by validating the input filename and prompting for overwrite if necessary.
        """
        folder = self.path
        filename = self.name_input.value.strip()
        if not filename:
            ui.notify('Please enter a file name', color='negative')
            return
        file_path = folder / filename
        if file_path.exists():
            dlg = ui.dialog()
            with dlg, ui.card():
                ui.label(f"'{filename}' already exists. Overwrite?")
                with ui.row().classes('w-full justify-end'):
                    ui.button('No', on_click=dlg.close).props('outline')
                    ui.button('Yes', on_click=lambda: (dlg.close(), self.submit([str(file_path)])))
            dlg.open()
        else:
            self.submit([str(file_path)])
