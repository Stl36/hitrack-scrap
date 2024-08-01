from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from payload import dbhost, dbport, database, dbpassword, dbusername
import enum


# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{dbusername}:{dbpassword}@{dbhost}:{dbport}/{database}')
Base = declarative_base()


class PriotiyEnum(enum.Enum):
    HIGH = 'high'
    AVERAGE = 'average'


class DBTrigger(Base):
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True)
    trigger_string = Column(JSON)
    priotity = Column(Enum(PriotiyEnum), default=PriotiyEnum.HIGH)
    # item = Column(String)
    # name = Column(String)
    # location = Column(String)
    # group = Column(String)
    # type = Column(String)
    # model = Column(String)
    # serial = Column(String)
    # status = Column(String)
    # last_communication = Column(String)
    # site_id = Column(String)
    # ip_address_1 = Column(String)
    # ip_address_2 = Column(String)
    active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


def __repr__(self):
       # return (f"<Device(item='{self.item}', name='{self.name}', active={self.active}, "
       #         f"model={self.active}, serial={self.serial}), status={self.status}>, site_id={self.site_id}")
       return (f"<DBTrigger(trigger_string='{self.trigger_string}', active='{self.active}', "
               f"updated_at='{self.updated_at}')>")

# Создаем таблицы, если их нет

Base.metadata.create_all(engine)

# Создаем сессию для взаимодействия с базой данных

Session = sessionmaker(bind=engine)
session = Session()


class TriggerManager:
    def __init__(self, triggers):
        self.triggers = triggers

    def update_database(self):
        # Получаем текущие активные триггеры из базы данных
        active_triggers = session.query(DBTrigger).filter(DBTrigger.active == True).all()

        # Определяем актуальные триггеры, которые есть в текущем списке
        # current_items = {trigger for trigger in self.triggers}
        current_items = self.triggers

        active_items = [trigger.trigger_string for trigger in active_triggers]

        # Добавляем новые устройства или обновляем существующие
        for trigger_dict in self.triggers:
            if trigger_dict not in active_items:
                # Добавляем новое устройство в базу данных
                # new_trigger = DBTrigger(
                #     item=device_dict['Item'],
                #     name=device_dict['Name'],
                #     location=device_dict['Location'],
                #     group=device_dict['Group'],
                #     type=device_dict['Type'],
                #     model=device_dict['Model'],
                #     serial=device_dict['Serial'],
                #     status=device_dict['Status'],
                #     #last_communication=datetime.strptime(device_dict['Last Communication'], '%Y/%m/%d %H:%M:%S'),
                #     last_communication=device_dict['Last Communication'],
                #     site_id=device_dict['Site ID'],
                #     ip_address_1=device_dict['IP Address 1'],
                #     ip_address_2=device_dict['IP Address 2'],
                #     active=True,
                #     updated_at=datetime
                # )
                new_trigger = DBTrigger(
                    trigger_string=trigger_dict
                )
                session.add(new_trigger)
            else:
                # # Обновляем существующее устройство
                # existing_device = session.query(DBTrigger).filter(DBTrigger.item == device_dict['Item']).one()
                # existing_device.name = device_dict['Name']
                # existing_device.location = device_dict['Location']
                # existing_device.group = device_dict['Group']
                # existing_device.type = device_dict['Type']
                # existing_device.model = device_dict['Model']
                # existing_device.serial = device_dict['Serial']
                # existing_device.status = device_dict['Status']
                # existing_device.last_communication = datetime.strptime(device_dict['Last Communication'], '%Y/%m/%d %H:%M:%S')
                # existing_device.site_id = device_dict['Site ID']
                # existing_device.ip_address_1 = device_dict['IP Address 1']
                # existing_device.ip_address_2 = device_dict['IP Address 2']
                # existing_device.active = True
                existing_trigger = session.query(DBTrigger).filter(DBTrigger.trigger_string == trigger_dict).one()
                existing_trigger.updated_at = datetime.utcnow()

        # Помечаем неактивные устройства, которых нет в текущем списке
        # for active_device in active_triggers:
        #     if active_device.item not in current_items:
        #         active_device.active = False
        #         active_device.last_communication = datetime.utcnow()
        for active_trigger in active_triggers:
            if active_trigger.trigger_string not in self.triggers:
                active_trigger.active = False
                active_trigger.updated_at = datetime.utcnow()

        # Удаляем неактивные устройства через 5 минут
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        session.query(DBTrigger).filter(DBTrigger.active == False,
                                        DBTrigger.updated_at < five_minutes_ago).delete()

        # Выполняем изменения в базе данных
        session.commit()

# # Пример:
# if __name__ == '__main__':
#     devices_list = [
#         {'Item': '1', 'Name': 'i07-VSPG370-453450-bkp', 'Location': 'M10', 'Group': 'IEP', 'Type': 'Storage', 'Model': 'VSP G370 (S2)', 'Serial': '453450', 'Status': ' Dynamic sparing start(Drive copy)', 'Last Communication': '2024/07/31 14:29:02', 'Site ID': 'PFW0090', 'IP Address 1': '192.168.207.206', 'IP Address 2': '192.168.207.205'},
#         {'Item': '2', 'Name': 'i07-VSPG800-443670', 'Location': 'M10', 'Group': 'IEP', 'Type': 'Enterprise RAID', 'Model': 'VSP F/G/N 800/600/400/200', 'Serial': '443670', 'Status': ' 1 recent SIM.', 'Last Communication': '2024/07/31 14:28:58', 'Site ID': 'PCC0030', 'IP Address 1': '192.168.207.104', 'IP Address 2': ''},
#         {'Item': '3', 'Name': 'i07-VSPG800-443754', 'Location': 'M10', 'Group': 'IEP', 'Type': 'Enterprise RAID', 'Model': 'VSP F/G/N 800/600/400/200', 'Serial': '443754', 'Status': ' 1 recent SIM.', 'Last Communication': '2024/07/31 14:23:33', 'Site ID': 'PCC0030', 'IP Address 1': '192.168.207.101', 'IP Address 2': ''},
#         {'Item': '4', 'Name': 'i07-VSPG900-417703', 'Location': 'M10', 'Group': 'IEP', 'Type': 'Storage', 'Model': 'VSP G900 (H)', 'Serial': '417703', 'Status': ' Dynamic sparing start(Drive copy)', 'Last Communication': '2024/07/31 14:31:44', 'Site ID': 'PFW0090', 'IP Address 1': '192.168.210.42', 'IP Address 2': '192.168.210.43'},
#         {'Item': '5', 'Name': 'i16-hcp-40435', 'Location': 'M10', 'Group': 'IEP', 'Type': 'Content Platform', 'Model': 'HCP', 'Serial': '40435', 'Status': ' Irreparable Objects Present', 'Last Communication': '2024/07/31 14:31:29', 'Site ID': 'PCC0030', 'IP Address 1': '192.168.35.10', 'IP Address 2': '192.168.35.21'},
#         {'Item': '6', 'Name': 'i67-VSPG900-417534', 'Location': 'M9', 'Group': 'IEP', 'Type': 'Storage', 'Model': 'VSP G900 (H)', 'Serial': '417534', 'Status': ' Dynamic sparing normal end(Drive copy)', 'Last Communication': '2024/07/31 14:29:47', 'Site ID': 'PFW0090', 'IP Address 1': '172.27.228.208', 'IP Address 2': '172.27.228.207'},
#         {'Item': '7', 'Name': 'i68-hcp-40434', 'Location': 'M9', 'Group': 'IEP', 'Type': 'Content Platform', 'Model': 'HCP', 'Serial': '40434', 'Status': ' 2 Errors', 'Last Communication': '2024/07/31 14:28:22', 'Site ID': 'PCC0030', 'IP Address 1': '172.26.18.21', 'IP Address 2': '172.26.18.10'}
#     ]
#
# trigger_manager = TriggerManager(devices_list)
#
# while True:
#     trigger_manager.update_database()
#     time.sleep(60)  # Проверка каждую минуту



