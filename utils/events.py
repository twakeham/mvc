class EventConnector(object):
    def connect(self) -> None:
        events = [attribute for attribute in dir(self) if attribute.endswith('event') and attribute != 'event']
        for event in events:
            name = event.replace('_', ' ').title().replace(' ', '').replace('Event', '')
            qt_name = name[0].lower() + name[1:]
            qt_signal = getattr(self, qt_name)
            qt_signal.connect(getattr(self, event))