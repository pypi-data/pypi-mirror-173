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
import logging
import sys
from collections import OrderedDict
from typing import Optional

from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from substrateinterface import Keypair, KeypairType

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH, WALLETS_PASSWORD_LENGTH
from tikka.libs.derivation import MEMBER_DERIVATION_PATH
from tikka.libs.secret import generate_alphabetic
from tikka.slots.pyqt.resources.gui.windows.account_derivation_create_rc import (
    Ui_AccountDerivationCreateDialog,
)


class AccountDerivationCreateWindow(QDialog, Ui_AccountDerivationCreateDialog):
    """
    AccountDerivationCreateWindow class
    """

    def __init__(
        self,
        application: Application,
        account: Account,
        parent: Optional[QWidget] = None,
    ):
        """
        Init import account window

        :param application: Application instance
        :param account: Account instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.account = account
        self._ = self.application.translator.gettext
        self.keypair = None
        self.password = None

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

        # Derivation selector translated
        for derivation_path in self.application.accounts.get_available_derivation_list(
            self.account
        ):
            if derivation_path == MEMBER_DERIVATION_PATH:
                self.derivationComboBox.addItem(
                    self._("Member"), userData=MEMBER_DERIVATION_PATH
                )
            else:
                self.derivationComboBox.addItem(
                    derivation_path, userData=derivation_path
                )

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        self.mnemonicLineEdit.textChanged.connect(self._generate_address)
        self.mnemonicLanguageComboBox.currentIndexChanged.connect(
            self._generate_address
        )
        self.derivationComboBox.currentIndexChanged.connect(self._generate_address)
        self.passwordChangeButton.clicked.connect(self._generate_wallet_password)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        # fill form
        self.rootAddressValueLabel.setText(self.account.address)
        self._generate_wallet_password()

    def _generate_address(self) -> bool:
        """
        Generate address from mnemonic

        :return:
        """
        self.errorLabel.setText("")
        language_code = self.mnemonicLanguageComboBox.currentData()
        mnemonic = self.mnemonicLineEdit.text().strip()
        derivation_path = self.derivationComboBox.currentData()
        suri = mnemonic + derivation_path
        if not Keypair.validate_mnemonic(mnemonic, language_code):
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        try:
            root_keypair = Keypair.create_from_mnemonic(
                mnemonic=mnemonic,
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.SR25519,
                language_code=language_code,
            )
        except Exception as exception:
            logging.exception(exception)
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        # if mnemonic address is not account address...
        if root_keypair.ss58_address != self.account.address:
            self.errorLabel.setText(
                self._("Mnemonic address is not the root account address!")
            )
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        try:
            self.keypair = Keypair.create_from_uri(
                suri=suri,
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.SR25519,
                language_code=language_code,
            )
        except Exception as exception:
            logging.exception(exception)
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        if self.keypair is not None:
            self.addressValueLabel.setText(self.keypair.ss58_address)
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)

        return True

    def _generate_wallet_password(self):
        """
        Generate new password for wallet encryption in UI

        :return:
        """
        self.password = generate_alphabetic(WALLETS_PASSWORD_LENGTH)
        self.passwordLineEdit.setText(self.password)

    def on_accepted_button(self):
        """
        Triggered when user click on ok button

        :return:
        """
        # user inputs
        mnemonic = self.mnemonicLineEdit.text().strip()
        derivation_path = self.derivationComboBox.currentData()
        language_code = self.mnemonicLanguageComboBox.currentData()
        name = self.nameLineEdit.text().strip()

        # generated inputs
        password = self.passwordLineEdit.text()

        # create derived account + wallet (and the read-only root account if not exists)
        self.application.accounts.create_new_account(
            mnemonic, language_code, derivation_path, name, password
        )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    account_ = Account(
        "5E6taVoL7eW8qpPKjDcf3GjyvFkkMB8EHkkqZksiWeViEkSP", name="test name"
    )
    AccountDerivationCreateWindow(application_, account_).exec_()
