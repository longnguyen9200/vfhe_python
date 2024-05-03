from model import DataModel, EncryptionService, DecryptionService

class DataController:
    def __init__(self):
        self.data_model = DataModel()
        self.encryption_serrvice = EncryptionService()
        self.decryption_service = DecryptionService()

    def set_selected_option(self, option):
        self.data_model.set_selected_option(option)

    def set_file_path(self, file_path):
        self.data_model.set_file_path(file_path)

    def set_value(self, n_number, coef_modulus, plain_modulus):
        self.data_model.set_value(n_number,coef_modulus,plain_modulus)

    def set_decrypt_value(self,c0_path, c1_path, sk_path, plaintext_modulus):
        self.data_model.set_decrypt_value(c0_path,c1_path,sk_path,plaintext_modulus)

    def get_data_encrypt(self):
        return {
            'selected_option': self.data_model.selected_option,
            'file_path': self.data_model.file_path,
            'n_number': self.data_model.n_number,
            'coef_modulus': self.data_model.coef_modulus,
            'poly_modulus': self.data_model.poly_modulus,
            'plaintext_modulus': self.data_model.plaintext_modulus,
            'base': self.data_model.base
        }
    
    def get_data_decrypt(self):
        return {
        'selected_option': self.data_model.selected_option,
        'c0_path': self.data_model.c0_path,
        'c1_path': self.data_model.c1_path,
        'sk': self.data_model.sk,
        'plaintext_modulus': self.data_model.plaintext_modulus
    }

    def process_encryption(self,data):
        self.encryption_serrvice.process_encyption(data)

    def process_decryption(self,data):
        self.decryption_service.process_decryption(data)