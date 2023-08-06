from fluvii.fluvii_app import FluviiTableApp
from .metrics import NubiumMetricsManager
from fluvii.metrics import MetricsManagerConfig


class NubiumTableApp(FluviiTableApp):
    def _init_metrics_manager(self):
        if not self.metrics_manager:
            metrics_config = MetricsManagerConfig(
                hostname=self._config.hostname,
                app_name=self._config.app_name
            )
            self.metrics_manager = NubiumMetricsManager(
                metrics_config=metrics_config, pusher_config=self._config.metrics_pusher_config)
