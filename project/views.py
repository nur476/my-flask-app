from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from project import db
from project.models import Otobus, User, Firma, Terminal, Gecis

class AdminModelView(ModelView):
    def is_accessible(self):#erişim izni kontrolü
        return current_user.is_authenticated #kullanıcı oturum açtımı açmadı mı kontrol eder.

class UserAdmin(AdminModelView):
    column_list = ('id', 'name', 'email', 'password', 'contact_number', 'bakiye', 'bakiye_ortak')
    column_labels = {
        'id': 'ID',
        'name': 'Name', 
        'email': 'Email Address', 
        'password': 'Password',
        'contact_number': 'Contact Number',
        'bakiye': 'Balance',
        'bakiye_ortak': 'Shared Balance'
    }
    column_filters = ('name', 'email', 'contact_number')

class FirmaAdmin(AdminModelView):
    column_list = ('id', 'name', 'created_at', 'contact_person', 'contact_number')
    column_labels = {
        'id': 'ID',
        'name': 'Company Name',
        'created_at': 'Created At',
        'contact_person': 'Contact Person',
        'contact_number': 'Contact Number'
    }
    column_filters = ('name', 'created_at', 'contact_person', 'contact_number')

class OtobusAdmin(AdminModelView):
    column_list = ('id', 'agent', 'user', 'plaka', 'bakiye', 'tag_id','created_at')
    column_labels = {
        'id': 'ID',
        'agent': 'Agent ID',
        'user': 'User ID',
        'plaka': 'License Plate',
        'bakiye': 'Balance',
        'tag_id':'Tag İd',
        'created_at': 'Created At'
    }
    column_filters = ('agent', 'user', 'plaka', 'bakiye','tag_id', 'created_at')

class TerminalAdmin(AdminModelView):
    column_list = ('name', 'ekstra', 'contact_person', 'contact_number', 'ucret', 'created_at')
    column_labels = {
        'name': 'Terminal Name',
        'ekstra': 'Extra',
        'contact_person': 'Contact Person',
        'contact_number': 'Contact Number',
        'ucret': 'Fee',
        'created_at': 'Created At'
    }
    column_filters = ('name', 'ekstra', 'contact_person', 'contact_number', 'ucret', 'created_at')

class GecisAdmin(AdminModelView):
    column_list = ('id', 'gecis_zamani', 'bus_id', 'terminal_id', 'odeme')
    column_labels = {
        'id': 'ID',
        'gecis_zamani': 'Transition Time',
        'bus_id': 'Bus ID',
        'terminal_id': 'Terminal ID',
        'odeme': 'Payment'
    }
    column_filters = ('gecis_zamani', 'bus_id', 'terminal_id', 'odeme')

    
    def create_model(self, form):# Yeni bir geçiş kaydı oluşturur ve otobüsün bakiyesini günceller. 
                                 # Otobüs bulunamazsa, kaydı siler ve hata döner.
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self.session.commit()

            # Otobüs bakiyesi güncelleme
            otobus = Otobus.query.get(model.bus_id)
            if otobus:
                if otobus.bakiye - model.odeme < 20:
                    # Bakiye yetersiz, işlemi geri al
                    self.session.delete(model)
                    self.session.commit()
                    return False, "Bakiye yetersiz"
                else:
                    otobus.bakiye -= model.odeme
                    self.session.commit()

                    # Kullanıcı bakiyesi güncelleme
                    user = User.query.get(otobus.user_id)
                    if user:
                        user.bakiye -= model.odeme
                        self.session.commit()
                    else:
                        # Kullanıcı bulunamadı, işlemi geri al
                        otobus.bakiye += model.odeme
                        self.session.delete(model)
                        self.session.commit()
                        return False, "Kullanıcı bulunamadı"
                    
                    return True
            else:
                # Otobüs bulunamadı, işlemi geri al
                self.session.delete(model)
                self.session.commit()
                return False, "Otobüs bulunamadı"
        except Exception as e:
            self.session.rollback()
            return False, str(e)

        #Mevcut bir geçiş kaydını günceller.
        #otobüsün bakiyesini eski ve yeni ödeme arasında günceller.
    def update_model(self, form, model):
        try:
            #Güncellenecek olan geçiş kaydını veritabanından alır.
            original_model = self.session.query(self.model).get(model.id)  # Güncellenecek kaydı bulur.
            original_odeme = original_model.odeme # Eski ödeme miktarını saklar.
            
            form.populate_obj(model)
            self.session.commit()
            
            otobus = Otobus.query.get(model.bus_id)# İlgili otobüsü bulur.
            if otobus:
                otobus.bakiye += original_odeme  #önceki ödemeyi geri al

                if otobus.bakiye-model.bakiye<20:
                    otobus.bakiye-=original_odeme
                    self.session.commit()
                    return False, "bakiye yetersiz"
                else:
                 otobus.bakiye -= model.odeme  ## Yeni ödemeyi düşer.ödemeyi günceller
                 self.session.commit()
                return True

            else:
                return False, "Otobüs bulunamadı"
                
        except Exception as e:
            self.session.rollback()
            return False, str(e)

