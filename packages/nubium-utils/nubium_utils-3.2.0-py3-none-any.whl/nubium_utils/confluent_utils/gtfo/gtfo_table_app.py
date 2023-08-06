from .gtfo_app import GtfoApp
from fluvii.fluvii_app import FluviiTableApp
from fluvii.transaction import TableTransaction


class GtfoTableApp(GtfoApp):
    def __init__(self, app_function, consume_topic, **kwargs):
        super().__init__(app_function, [consume_topic], **kwargs)

    def _get_app(self, *args, **kwargs):
        if not kwargs.get('transaction_cls'):
            kwargs['transaction_cls'] = TableTransaction
        return FluviiTableApp(*args, fluvii_config=self._config, **kwargs)
