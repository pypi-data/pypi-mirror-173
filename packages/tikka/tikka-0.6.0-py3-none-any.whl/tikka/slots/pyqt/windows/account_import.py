# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
from collections import OrderedDict
from typing import Optional

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from substrateinterface import Keypair, KeypairType
from substrateinterface.utils.ss58 import is_valid_ss58_address

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH, WALLETS_PASSWORD_LENGTH
from tikka.libs.derivation import detect_derivation
from tikka.libs.secret import generate_alphabetic
from tikka.slots.pyqt.resources.gui.windows.account_import_rc import (
    Ui_AccountImportDialog,
)


class AccountImportWindow(QDialog, Ui_AccountImportDialog):
    """
    AccountImportWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init import account window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext

        # Mnemonic language selector translated
        mnemonic_language_selector = OrderedDict(
            [
                ("en", self._("English")),
                ("fr", self._("French")),
                ("zh-hans", self._("Chinese simplified")),
                ("zh-hant", self._("Chinese traditional")),
                ("it", self._("Italian")),
                ("ja", self._("Japanese")),
                ("ko", self._("Korean")),
                ("es", self._("Spanish")),
            ]
        )
        for language_code, language_name in mnemonic_language_selector.items():
            self.mnemonicLanguageComboBox.addItem(language_name, userData=language_code)
        self.mnemonicLanguageComboBox.setCurrentIndex(
            self.mnemonicLanguageComboBox.findData(
                self.application.config.get("language")[:2]
            )
        )

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        self.mnemonicLanguageComboBox.currentIndexChanged.connect(
            self._on_mnemonic_changed
        )
        self.mnemonicLineEdit.textChanged.connect(self._on_mnemonic_changed)
        self.addressLineEdit.textChanged.connect(self._on_address_changed)
        self.derivationLineEdit.keyPressEvent = self._on_derivation_keypress_event
        self.passwordChangeButton.clicked.connect(self._generate_wallet_password)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        # fill form
        self._generate_wallet_password()

    def _on_mnemonic_changed(self):
        """
        Triggered when mnemonic is changed

        :return:
        """
        self.errorLabel.setText("")
        address = self.addressLineEdit.text().strip()
        if address == "":
            return

        if self.verify_user_entry() is not True:
            return

        address = self.addressLineEdit.text().strip()
        if self.address_already_exists(address):
            return

        self._generate_derivation()

    def _on_address_changed(self):
        """
        Triggered when address is changed

        :return:
        """
        self.errorLabel.setText("")
        mnemonic = self.mnemonicLineEdit.text().strip()
        if mnemonic == "":
            return

        if self.verify_user_entry() is not True:
            return

        address = self.addressLineEdit.text().strip()
        if self.address_already_exists(address):
            return

        self._generate_derivation()

    def _on_derivation_keypress_event(self, _: QKeyEvent):
        """
        Triggered when user enter text in derivationLineEdit

        :return:
        """
        self.verify_user_entry()

        address = self.addressLineEdit.text().strip()
        mnemonic = self.mnemonicLineEdit.text().strip()
        language_code = self.mnemonicLanguageComboBox.currentData()
        derivation_ = self.derivationLineEdit.text().strip()
        suri = mnemonic + derivation_
        try:
            keypair = Keypair.create_from_uri(
                suri,
                language_code=language_code,
                crypto_type=KeypairType.SR25519,
                ss58_format=self.application.currencies.get_current().ss58_format,
            )
        except Exception:
            self.derivationLineEdit.setEnabled(True)
            self.errorLabel.setText(self._("Derivation is not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return

        if keypair.ss58_address == address:
            self.derivationLineEdit.setEnabled(False)
            self.errorLabel.setText("")
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
        else:
            self.derivationLineEdit.setEnabled(True)
            self.errorLabel.setText(self._("Derivation does not match with address"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

    def address_already_exists(self, address: str) -> bool:
        """
        Modify form if address already exists

        :param address: Address to check
        :return:
        """
        if self.application.accounts.get_by_address(address) is not None:
            self.errorLabel.setText(self._("Account already exists!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return True

        return False

    def verify_user_entry(self) -> bool:
        """
        Verify user entry, return True if OK, False otherwise

        :return:
        """
        # verify mnemonic
        language_code = self.mnemonicLanguageComboBox.currentData()
        if not Keypair.validate_mnemonic(
            self.mnemonicLineEdit.text().strip(), language_code
        ):
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        # verify address
        if not is_valid_ss58_address(
            self.addressLineEdit.text().strip(),
            valid_ss58_format=self.application.currencies.get_current().ss58_format,
        ):
            self.errorLabel.setText(self._("Account address is not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        return True

    def _generate_derivation(self):
        """
        Generate derivation for address from mnemonic

        :return:
        """
        address = self.addressLineEdit.text().strip()
        mnemonic = self.mnemonicLineEdit.text().strip()
        langage_code = self.mnemonicLanguageComboBox.currentData()
        # get derivation
        derivation_ = detect_derivation(
            address,
            mnemonic,
            langage_code,
            ss58_format=self.application.currencies.get_current().ss58_format,
            crypto_type=KeypairType.SR25519,
        )
        if derivation_ is not None:
            self.derivationLineEdit.setText(derivation_)
            self.derivationLineEdit.setEnabled(False)
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
            if derivation_ == "":
                self.errorLabel.setText(
                    self._(
                        "WARNING : it is not secure to store a root account private key"
                    )
                )
        else:
            self.derivationLineEdit.setText("")
            self.derivationLineEdit.setEnabled(True)
            self.errorLabel.setText(
                self._(
                    "Derivation not detected : please enter derivation path manually"
                )
            )
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

    def _generate_wallet_password(self):
        """
        Generate new password for wallet encryption in UI

        :return:
        """
        self.passwordLineEdit.setText(generate_alphabetic(WALLETS_PASSWORD_LENGTH))

    def on_accepted_button(self):
        """
        Triggered when user click on ok button

        :return:
        """
        # user inputs
        mnemonic = self.mnemonicLineEdit.text().strip()
        name = self.nameLineEdit.text().strip()
        language_code = self.mnemonicLanguageComboBox.currentData()

        # generated inputs
        password = self.passwordLineEdit.text()
        derivation_ = self.derivationLineEdit.text().strip()

        self.application.accounts.create_new_account(
            mnemonic, language_code, derivation_, name, password
        )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    AccountImportWindow(application_).exec_()
