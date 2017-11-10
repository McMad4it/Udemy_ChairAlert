from src.common.database import Database
from src.models.alerts.alert import Alert

__author__ = 'neil'

Database.initialise()

alerts_needing_update = Alert.find_needing_updates()

for alert in alerts_needing_update:
    alert.load_item_price()
    alert.send_email_if_price_reached()
