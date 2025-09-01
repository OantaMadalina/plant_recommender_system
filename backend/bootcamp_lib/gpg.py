# This file should be kept compatible with Python 3.7 syntax

import os
import json
import codecs
import threading

import boto3
import gnupg

from bootcamp_lib.logger import Logger


class GPGException(Exception):
    """GPG exception during a GPG encryption/decryption operation"""


class SilentGPG(gnupg.GPG):
    """GPG overwritten class which won't show warnings on gpg --version check"""
    def _collect_output(self, process, result, writer=None, stdin=None):
        stderr = codecs.getreader(self.encoding)(process.stderr)
        rr = threading.Thread(target=self._read_response, args=(stderr, result))
        rr.daemon = True
        gnupg.logger.debug('stderr reader: %r', rr)
        rr.start()

        stdout = process.stdout
        dr = threading.Thread(target=self._read_data, args=(stdout, result, self.on_data))
        dr.daemon = True
        gnupg.logger.debug('stdout reader: %r', dr)
        dr.start()

        dr.join()
        rr.join()
        if writer is not None:
            writer.join(0.01)
        process.wait()
        result.returncode = rc = process.returncode
        # Don't show the warning if we're doing the imports
        if rc != 0 and not (rc == 2 and "--import" in process.args):
            gnupg.logger.warning('gpg returned a non-zero error code: %d', rc)
        if stdin is not None:
            try:
                stdin.close()
            except IOError:  # pragma: no cover
                pass
        stderr.close()
        stdout.close()
        return rc


class GPG:
    def __init__(
            self, secret_id: str, secret_string: str, public_key_secret_string: str = "",
            recepient_secret_secret: str = "", secrets_client=None):
        self.secret_id = secret_id
        self.secret_string = secret_string
        self.public_key_secret_string = public_key_secret_string
        self.recepient_secret_secret = recepient_secret_secret
        self.secrets_client = secrets_client or boto3.client("secretsmanager")
        self.recipient = ""

        self._import_key()

    def _import_key(self):
        gpg_homedir = "/tmp/.gnupg"
        try:
            os.mkdir(gpg_homedir, mode=0o700)
        except FileExistsError:
            pass

        keys = None
        keys_public = None

        try:
            secret_data = self.secrets_client.get_secret_value(SecretId=self.secret_id)
            keys_dict = json.loads(secret_data["SecretString"])
            if self.secret_string:
                keys = self._format_key(keys_dict[self.secret_string])
            if self.public_key_secret_string:
                keys_public = self._format_key(keys_dict[self.public_key_secret_string])
            if self.recepient_secret_secret:
                self.recipient = keys_dict[self.recepient_secret_secret]

        except Exception:
            Logger().exception("Error retrieving GPG keys")
            raise Exception("Error retrieving GPG keys")

        self._gpg = SilentGPG(gnupghome=gpg_homedir)
        if keys:
            self._gpg.import_keys(keys)
        if keys_public:
            self._gpg.import_keys(keys_public)

    def _format_key(self, key: str):
        start = key.find("BLOCK-----")
        end = key.find("-----END PGP")
        return key[:start + 10] + key[start + 10: end].replace(" ", "\n") + key[end:]

    def encrypt(self, input_path, output_path, armor=False):
        with open(input_path, "rb") as file:
            filename = os.path.basename(input_path)
            try:
                result = self._gpg.encrypt_file(
                    file, output=output_path, recipients=self.recipient, armor=armor,
                    always_trust=True
                )
            except Exception as ex:
                raise GPGException(f"GPG encryption for file '{filename}' failed with error '{ex}'")
            if result.status != "encryption ok":
                raise GPGException(
                    f"GPG encryption for file '{filename}' failed with error '{result.status}'")

    def decrypt(self, input_path, output_path):
        with open(input_path, "rb") as enc_file:
            filename = os.path.basename(input_path)
            try:
                result = self._gpg.decrypt_file(enc_file, output=output_path)
            except Exception as ex:
                raise GPGException(f"GPG decryption for file '{filename}' failed with error '{ex}'")
            if result.status != "decryption ok":
                raise GPGException(
                    f"GPG decryption for file '{filename}' failed with error '{result.status}'")


if (library_path := os.getenv("LD_LIBRARY_PATH")):
    os.environ["LD_LIBRARY_PATH"] += ":/opt/lib"
else:
    os.environ["LD_LIBRARY_PATH"] = "/opt/lib"


if (library_path := os.getenv("PATH")):
    os.environ["PATH"] += ":/opt/bin"
else:
    os.environ["PATH"] = "/opt/bin"
