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

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QWidget
from substrateinterface import Keypair, KeypairType

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH, WALLETS_PASSWORD_LENGTH
from tikka.libs.secret import generate_alphabetic
from tikka.slots.pyqt.resources.gui.windows.wallet_restore_rc import (
    Ui_WalletRestoreDialog,
)


class WalletRestoreWindow(QDialog, Ui_WalletRestoreDialog):
    """
    WalletRestoreWindow class
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
            self._generate_address
        )
        self.mnemonicLineEdit.textChanged.connect(self._generate_address)
        self.passwordChangeButton.clicked.connect(self._generate_wallet_password)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

        # fill form
        self.derivationValueLabel.setText(self.account.path)
        self.addressValueLabel.setText(self.account.address)
        self.nameValueLabel.setText(self.account.name)
        self._generate_wallet_password()

    def _generate_address(self) -> bool:
        """
        Generate address from mnemonic

        :return:
        """
        self.errorLabel.setText("")
        language_code = self.mnemonicLanguageComboBox.currentData()
        derivation_path = "" if self.account.path is None else self.account.path
        suri = self.mnemonicLineEdit.text().strip() + derivation_path
        if suri == "":
            return False
        try:
            address = Keypair.create_from_uri(
                suri,
                ss58_format=self.application.currencies.get_current().ss58_format,
                crypto_type=KeypairType.SR25519,
                language_code=language_code,
            ).ss58_address
        except Exception as exception:
            logging.exception(exception)
            self.errorLabel.setText(self._("Mnemonic or language not valid!"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        # if mnemonic address is not account address...
        if address != self.account.address:
            self.errorLabel.setText(
                self._("Mnemonic address is not the account address!")
            )
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)
            return False

        self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
        return True

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
        derivation_path = "" if self.account.path is None else self.account.path
        suri = self.mnemonicLineEdit.text().strip() + derivation_path
        language_code = self.mnemonicLanguageComboBox.currentData()

        # generated inputs
        password = self.passwordLineEdit.text()

        # create keypair from mnemonic to get seed as hexadecimal
        keypair = Keypair.create_from_uri(
            suri,
            language_code=language_code,
            crypto_type=KeypairType.SR25519,
            ss58_format=self.application.currencies.get_current().ss58_format,
        )

        wallet = self.application.wallets.get(keypair.ss58_address)
        if wallet is None:
            # create and store Wallet instance
            wallet = self.application.wallets.create(keypair, password)
            self.application.wallets.add(wallet)
        else:
            # display confirm dialog and get response
            button = QMessageBox.question(
                self,
                self._("Change wallet password?"),
                self._(
                    "A wallet already exists for this account. Change password for {address} wallet?"
                ).format(address=wallet.address),
            )
            if button == QMessageBox.Yes:
                # create and store Wallet instance
                new_wallet = self.application.wallets.create(keypair, password)
                self.application.wallets.update(new_wallet)

        self.application.accounts.unlock(self.account, password)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    account_ = Account(
        "5D2YjANfzuGvJWc3gykeFokJoboi57WAqbaVdo8VJzduFNsB", path="//2", name="test name"
    )
    WalletRestoreWindow(application_, account_).exec_()
