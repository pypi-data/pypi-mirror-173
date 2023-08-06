from pathlib import Path
import re
from typing import Any

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QToolButton,
    QDialogButtonBox,
    QWidget,
    QLineEdit,
    QStyle,
    QFrame,
)
from PySide6.QtGui import (
    QValidator,
    QPixmap,
)
from PySide6.QtCore import (
    Qt,
)

from .metadata_editor_base import MetadataEditor
from .flowlayout import FlowLayout


class AnnexMetadataEditor(MetadataEditor):
    """Git-annex metadata editor

    Git-annex supports assigning metadata to any "annexed" file in a dataset.
    More precisely, such metadata are associated with the underlying annex-key,
    the content identifier. Therefore, multiple files that have the exact same
    content will also report the same metadata record. When a file with
    git-annex metadata is modified, the metadata of the previous version will
    be copied to the new annex-key when the modified file is saved in the
    dataset.

    Each metadata record can have any number of metadata fields, which each can
    have any number of values. For example, to tag files, the "tag" field is
    typically used, with values set to each tag that applies to the file.

    The field names are limited to alphanumerics (and [_-.]), and are case
    insensitive. The metadata values can contain any text.

    Importantly, both metadata field names and all values of a particular field
    are technically a set, there cannot be duplicate values.

    To remove an entire field from an existing metadata record, all of its
    values have to be removed.
    """
    # used as the widget title
    _widget_title = 'Annex metadata'

    def __init__(self, parent):
        super().__init__(parent)

        # all field edits
        self.__fields = []
        self.__path = None

        editor_layout = QVBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(editor_layout)
        # first the form with the fields
        self.__field_form = QFormLayout()
        # enforce alignment across platforms, flow layout looks weird
        # with centered items
        self.__field_form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.__field_form.setContentsMargins(0, 0, 0, 0)
        self.__field_form.addRow(
            QLabel('Field'),
            QLabel('Value'),
        )
        editor_layout.addLayout(self.__field_form)
        # button to add a field
        add_field_pb = QPushButton("Add field", self)
        add_field_pb.clicked.connect(self._on_addfield_clicked)
        addf_layout = QHBoxLayout()
        addf_layout.addWidget(add_field_pb)
        addf_layout.addStretch()
        editor_layout.addLayout(addf_layout)
        # button box to save/cancel
        bbx = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        # on cancel just disable the whole thing
        bbx.rejected.connect(lambda: self.setDisabled(True))
        # on save, validate and store
        bbx.accepted.connect(self._save_metadata)
        self.__bbx = bbx
        editor_layout.addWidget(bbx)
        editor_layout.addStretch()

    def set_path(self, path: Path):
        self.__path = path
        self._load_metadata()

    def _reset(self):
        # take care of cleaning up the underlying items
        field_items = [
            self.__field_form.itemAt(row, QFormLayout.LabelRole).widget()
            # start after header
            for row in range(1, self.__field_form.rowCount())
        ]
        for fi in field_items:
            self._discard_item(fi)
        self.__bbx.button(QDialogButtonBox.Save).setDisabled(True)

    def _load_metadata(self):
        res = _run_annex_metadata(self.__path)
        # just one record
        assert isinstance(res, dict)
        self._set_metadata_from_annexjson(res)

    def _set_metadata_from_annexjson(self, data):
        last_changed_marker = '-lastchanged'
        # clean slate
        self._reset()
        fields = data['fields']
        field_widgets = {}
        last_changed = {}
        for f in sorted(fields):
            if f == 'lastchanged':
                # we have no use for the overall timestamp ATM
                continue
            if f.endswith(last_changed_marker):
                # comes as an array of length 1
                last_changed[f[:-1 * len(last_changed_marker)]] = fields[f][0]
                continue

            fw, fv_layout = self._add_field(from_record=True)
            fw.set_value(f)
            for v in fields[f]:
                fv = self._add_field_value(fw, fv_layout)
                fv.set_value(v)
            self._add_field_value_add_pb(fw, fv_layout)
            field_widgets[f] = fw

        for f, fw in field_widgets.items():
            fw.set_state(
                QStyle.SP_FileDialogInfoView,
                f'Last changed: {last_changed.get(f, "")}'
            )
        self.enable_save()

    def _validate(self):
        warn_pm = QStyle.SP_MessageBoxWarning
        valid = True

        def _invalid(item, msg):
            item.set_state(warn_pm, msg)
            return False

        def _valid(item):
            item.set_state()

        data = {}
        fn_validator = ItemWidget._validators[self]
        for fni in ItemWidget._field_tracker[self]:
            # first check field name value, we don't accept invalid of empty
            if fn_validator.validate(fni.value, 0) != QValidator.Acceptable:
                valid = _invalid(
                    fni, 'Invalid value, set valid value or discard')
            else:
                _valid(fni)
            # now all values, may be empty to delete whole field
            fv_validator = ItemWidget._validators[fni]
            values = set()
            for fvi in ItemWidget._field_tracker[fni]:
                if fv_validator.validate(fvi.value, 0) != QValidator.Acceptable:
                    valid = _invalid(
                        fvi, 'Invalid value, set valid value or discard')
                else:
                    _valid(fvi)
                    values.add(fvi.value)
            data[fni.value] = list(values)
        return data, valid

    def enable_save(self):
        self.__bbx.button(QDialogButtonBox.Save).setEnabled(True)

    def _save_metadata(self):
        data, valid = self._validate()
        if not valid:
            self.__bbx.button(QDialogButtonBox.Save).setDisabled(True)
            return
        res = _run_annex_metadata(self.__path, data)
        # just one record
        assert isinstance(res, dict)
        self._set_metadata_from_annexjson(res)

    def _add_field(self, from_record=False):
        # field name edit, make the editor itself the parent
        # the items will group themselves by parent to validate as a set
        # within a group
        fn = ItemWidget(
            self, self, self,
            is_field_name=True,
            allow_discard=not from_record,
        )
        # layout to contain all field
        flow_layout = FlowLayout()
        flow_layout.setContentsMargins(0, 0, 0, 0)
        self.__field_form.addRow(fn, flow_layout)
        return fn, flow_layout

    def _on_addfield_clicked(self):
        fn, layout = self._add_field()
        # use the field name widget as a parent for the field value widgets
        # by that they will group themselves to act like a set during
        # validation
        self._add_field_value(fn, layout)
        self._add_field_value_add_pb(fn, layout)

    def _on_add_field_value_clicked(self, group_id, replace=None):
        row = self._find_form_row_by_name_widget(group_id)
        # the flow layout for all value widgets
        layout = self.__field_form.itemAt(row, QFormLayout.FieldRole)
        if replace is not None:
            replace.close()
            layout.removeWidget(replace)
            del replace
        self._add_field_value(group_id, layout)
        self._add_field_value_add_pb(group_id, layout)

    def _add_field_value(self, group_id, layout):
        # field value edit
        fv = ItemWidget(group_id, self, self)
        layout.addWidget(fv)
        return fv

    def _add_field_value_add_pb(self, group_id, layout):
        # '+' button to add a new value
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.StyledPanel)
        pb = QToolButton(frame)
        pb.setText('+')
        pb.clicked.connect(lambda: self._on_add_field_value_clicked(
            group_id, replace=frame))
        bl = QVBoxLayout()
        bl.setContentsMargins(0, 0, 0, 0)
        bl.addWidget(pb)
        frame.setLayout(bl)
        layout.addWidget(frame)
        self.enable_save()

    def _find_form_row_by_name_widget(self, widget):
        # start searching after header row
        for row in range(1, self.__field_form.rowCount()):
            label_at_row = self.__field_form.itemAt(
                row, QFormLayout.LabelRole).widget()
            if widget == label_at_row:
                return row
        raise ValueError(
            'Given widget does not correspond to field name widget')

    def _discard_item(self, item):
        self.enable_save()
        if isinstance(item.group_id, AnnexMetadataEditor):
            # the main editor is the group -> field name widget
            row = self._find_form_row_by_name_widget(item)
            layout = self.__field_form.itemAt(row, QFormLayout.FieldRole)
            i = layout.takeAt(0)
            while i:
                i.widget().close()
                i = layout.takeAt(0)
            i = self.__field_form.itemAt(row, QFormLayout.LabelRole).widget()
            i.close()
            self.__field_form.removeRow(row)
        else:
            # -> field value widget
            row = self._find_form_row_by_name_widget(item.group_id)
            layout = self.__field_form.itemAt(row, QFormLayout.FieldRole)
            item.close()
            layout.removeWidget(item)


class ItemWidget(QFrame):
    # track fields for a particular path across all class
    # instances
    _field_tracker = dict()
    _validators = dict()

    def __init__(self,
                 group_id: Any,
                 editor: AnnexMetadataEditor,
                 parent: QWidget,
                 is_field_name: bool = False,
                 allow_discard: bool = True):
        super().__init__(parent)
        self.__annex_metadata_editor = editor
        self.__group_id = group_id
        if group_id not in ItemWidget._field_tracker:
            items_widgets = set()
            ItemWidget._field_tracker[group_id] = items_widgets
            ItemWidget._validators[group_id] = \
                AnnexMetadataFieldNameValidator(group_id, editor) \
                if is_field_name else \
                AnnexMetadataValueValidator(group_id, editor)
        # register item in the group of its parent
        items = self._field_tracker[group_id]
        items.add(self)

        self.setFrameStyle(QFrame.StyledPanel)
        # all components in a horizontal arrangement
        layout = QHBoxLayout()
        # tight fit
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # edit first
        edit = QLineEdit(self)
        edit.setClearButtonEnabled(True)
        edit.textChanged.connect(self._on_textchanged)
        edit.editingFinished.connect(self._on_editingfinished)
        edit.setValidator(ItemWidget._validators[group_id])
        layout.addWidget(edit)
        self.__editor = edit
        # state label
        state = QLabel(self)
        self.__state_label = state
        layout.addWidget(state)
        # discard button
        db = QToolButton(self)
        db.setIcon(self.style().standardIcon(QStyle.SP_DialogDiscardButton))
        if allow_discard:
            db.clicked.connect(lambda: editor._discard_item(self))
        else:
            db.setDisabled(True)
            db.setToolTip(
                'Field present in existing record. '
                'Discard all values and save, to delete the entire field.'
            )
        layout.addWidget(db)

    def closeEvent(self, *args, **kwargs):
        # unregister this item from its parent group
        if self.__group_id in self._field_tracker:
            self._field_tracker[self.__group_id].discard(self)
        # if this item is itself a group_id, remove entire group
        self._field_tracker.pop(self, None)
        self._validators.pop(self, None)
        # normal handling
        super().closeEvent(*args, **kwargs)

    @property
    def group_id(self):
        return self.__group_id

    @property
    def value(self):
        return self.__editor.text()

    def _on_textchanged(self):
        # clear any checkmarks (empty pixmap)
        self.set_state()
        self.__annex_metadata_editor.enable_save()
        # TODO make resize to minimum work
        return
        #edit = self.__editor
        #text = edit.text()
        #if len(text) < 4:
        #    text = 'mmmm'
        #px_width = QFontMetrics(edit.font()).size(
        #    Qt.TextSingleLine, text).width()
        #edit.setFixedWidth(px_width)

    def _on_editingfinished(self):
        # put a little checkmark behind the edit as an indicator that
        # the current field name is OK
        self.set_state(QStyle.SP_DialogApplyButton)

    def set_state(self, stdpixmap=None, tooltip=None):
        if stdpixmap is None:
            pixmap = QPixmap(0, 0)
        else:
            pixmap = self.style().standardPixmap(stdpixmap)
        # shrink the standard pixmap to the height of the editor
        # if it happens to be humongous in some platform
        if pixmap.size().height() > self.__editor.size().height():
            pixmap = pixmap.scaledToHeight(self.__editor.size().height())
        self.__state_label.setPixmap(pixmap)

        if not tooltip:
            tooltip = ''
        self.__state_label.setToolTip(tooltip)

    def set_value(self, value):
        self.__editor.setText(value)


class AnnexMetadataValueValidator(QValidator):
    def __init__(self, group_id: Any, parent: QWidget):
        super().__init__(parent)
        self.__group_id = group_id

    def validate(self, input: str, pos: int, compare_lower=False):
        # we cannot ever invalidate, because a user could always
        # enter another char to make it right
        if not input:
            return QValidator.Intermediate

        # check all items from this group
        matching_items = sum(
            (input.lower() == i.value.lower()
             if compare_lower
             else input == i.value)
            for i in ItemWidget._field_tracker[self.__group_id]
        )
        if matching_items > 1:
            return QValidator.Intermediate
        else:
            return QValidator.Acceptable


class AnnexMetadataFieldNameValidator(AnnexMetadataValueValidator):
    # from https://git-annex.branchable.com/metadata
    _valid_regex = re.compile('^[a-z0-9.\-_]+$')

    def validate(self, input: str, pos: int):
        if not AnnexMetadataFieldNameValidator._valid_regex.match(
                input.lower()):
            return QValidator.Invalid
        # otherwise like normal, but case-insensitive
        return super().validate(input, pos, compare_lower=True)


def _run_annex_metadata(path, data=None):
    from datalad.runner import (
        GitRunner,
        StdOutCapture,
    )
    from datalad.utils import get_dataset_root
    import json
    runner = GitRunner()
    cmd = ['git', 'annex', 'metadata', '--json', '--batch']
    dsroot = get_dataset_root(path)
    j = {
        'file': str(path.relative_to(dsroot)),
    }
    if data:
        j['fields'] = data
    out = runner.run(
        cmd,
        cwd=str(dsroot),
        stdin=f'{json.dumps(j)}\n'.encode('utf-8'),
        protocol=StdOutCapture,
    )
    res = json.loads(out['stdout'])
    return res
