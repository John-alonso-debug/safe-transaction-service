import logging
import os

from django.apps import AppConfig, apps
from django.conf import settings

from kombu import Queue, Exchange
from celery import Celery
from celery._state import get_current_task
from celery.app.log import TaskFormatter
from celery.signals import setup_logging
from celery.utils.log import ColorFormatter

# task list:
from safe_transaction_service.tokens.tasks import *
from safe_transaction_service.notifications.tasks import *
from safe_transaction_service.history.tasks import *
from safe_transaction_service.contracts.tasks import *


logger = logging.getLogger(__name__)


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('safe_transaction_service')


##################################################################################


# default:
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
app.conf.task_always_eager = False
app.conf.timezone = "UTC"
app.conf.enable_utc = True

# celery queues
app.conf.task_queues = {
    Queue("default", Exchange("default"), routing_key="default"),
    #
    # tokens
    #
    Queue("tokens", Exchange("tokens"), routing_key="tokens.calculate_token_eth_price_task"),
    Queue("tokens", Exchange("tokens"), routing_key="tokens.fix_pool_tokens_task"),
    Queue("tokens", Exchange("tokens"), routing_key="tokens.get_token_info_from_blockchain"),
    #
    # notifications
    #
    Queue("notifications", Exchange("notifications"), routing_key="notifications.send_notification_task"),
    Queue("notifications", Exchange("notifications"), routing_key="notifications.send_notification_owner_task"),
    #
    # history group:
    #
    Queue("history", Exchange("history"), routing_key="history.index_new_proxies_task"),
    Queue("history", Exchange("history"), routing_key="history.index_internal_txs_task"),
    Queue("history", Exchange("history"), routing_key="history.index_safe_events_task"),
    Queue("history", Exchange("history"), routing_key="history.index_erc20_events_task"),
    Queue("history", Exchange("history"), routing_key="history.process_decoded_internal_txs_task"),
    Queue("history", Exchange("history"), routing_key="history.process_decoded_internal_txs_for_safe_task"),
    Queue("history", Exchange("history"), routing_key="history.check_reorgs_task"),
    Queue("history", Exchange("history"), routing_key="history.send_webhook_task"),
    Queue("history", Exchange("history"), routing_key="history.index_contract_metadata"),

    #
    # contracts group:
    #
    Queue("contracts", Exchange("contracts"), routing_key="contracts.index_contracts_metadata_task"),
    Queue("contracts", Exchange("contracts"), routing_key="contracts.xxx"),


}


# celery routes
app.conf.task_routes = {
    #
    # tokens tasks: mapper taskFn with queue.
    #
    "safe_transaction_service.tokens.tasks.calculate_token_eth_price_task": {
        "queue": "tokens",
        "routing_key": "tokens.calculate_token_eth_price_task"
    },
    "safe_transaction_service.tokens.tasks.fix_pool_tokens_task": {
        "queue": "tokens",
        "routing_key": "tokens.fix_pool_tokens_task"
    },
    "safe_transaction_service.tokens.tasks.get_token_info_from_blockchain": {
        "queue": "tokens",
        "routing_key": "tokens.get_token_info_from_blockchain"
    },

    #
    # notifications tasks:
    #
    "safe_transaction_service.notifications.tasks.send_notification_task": {
        "queue": "notifications",
        "routing_key": "notifications.send_notification_task"
    },
    "safe_transaction_service.notifications.tasks.send_notification_owner_task": {
        "queue": "notifications",
        "routing_key": "notifications.send_notification_owner_task"
    },

    #
    # history
    #
    "safe_transaction_service.history.tasks.index_new_proxies_task": {
        "queue": "history",
        "routing_key": "history.index_new_proxies_task"
    },

    "safe_transaction_service.history.tasks.index_internal_txs_task": {
        "queue": "history",
        "routing_key": "history.index_internal_txs_task"
    },
    "safe_transaction_service.history.tasks.index_safe_events_task": {
        "queue": "history",
        "routing_key": "history.index_safe_events_task"
    },
    "safe_transaction_service.history.tasks.index_erc20_events_task": {
        "queue": "history",
        "routing_key": "history.index_erc20_events_task"
    },
    "safe_transaction_service.history.tasks.process_decoded_internal_txs_task": {
        "queue": "history",
        "routing_key": "history.process_decoded_internal_txs_task"
    },
    "safe_transaction_service.history.tasks.process_decoded_internal_txs_for_safe_task": {
        "queue": "history",
        "routing_key": "history.process_decoded_internal_txs_for_safe_task"
    },
    "safe_transaction_service.history.tasks.check_reorgs_task": {
        "queue": "history",
        "routing_key": "history.check_reorgs_task"
    },
    "safe_transaction_service.history.tasks.send_webhook_task": {
        "queue": "history",
        "routing_key": "history.send_webhook_task"
    },
    "safe_transaction_service.history.tasks.index_contract_metadata": {
        "queue": "history",
        "routing_key": "history.index_contract_metadata"
    },

    #
    # contracts
    #
    "safe_transaction_service.contracts.tasks.index_contracts_metadata_task": {
        "queue": "contracts",
        "routing_key": "contracts.index_contracts_metadata_task"
    },
}


##################################################################################


class CeleryConfig(AppConfig):
    name = 'safe_transaction_service.taskapp'
    verbose_name = 'Celery Config'

    # Use Django logging instead of celery logger
    @setup_logging.connect
    def on_celery_setup_logging(**kwargs):
        pass

    # @after_setup_logger.connect
    # def setup_loggers(logger, *args, **kwargs):
    #     formatter = TaskFormatter('%(asctime)s [%(levelname)s] [%(processName)s] %(message)s')
    #     handler = logger.handlers[0]
    #     # handler = logging.StreamHandler()
    #     handler.setFormatter(formatter)
    #     # print(logger.handlers)
    #     # logger.addHandler(handler)

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


class IgnoreSucceededNone(logging.Filter):
    """
    Ignore the messages of the style (usually emitted when redis lock is active)
    `Task safe_transaction_service.history.tasks.index_internal_txs_task[89ad3c46-aeb3-48a1-bd6f-2f3684323ca8]
    succeeded in 1.0970600529108196s: None`
    """
    def filter(self, rec: logging.LogRecord):
        message = rec.getMessage()
        return not ('Task' in message and 'succeeded' in message and 'None' in message)


class PatchedCeleryFormatterOriginal(TaskFormatter):
    """
    Patched to work as an standard logging formatter. Basic version
    """
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, use_color=True)


class PatchedCeleryFormatter(ColorFormatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, use_color=True)

    def format(self, record):
        task = get_current_task()
        if task and task.request:
            # For gevent pool, task_id will be something like `7ab44cb4-aacf-444e-bc20-4cbaa2a7b082`. For logs
            # is better to get it short
            task_id = task.request.id[:8]
            # Task name usually has all the package, better cut the first part for logging
            task_name = task.name.split('.')[-1]

            record.__dict__.update(task_id=task_id,
                                   task_name=task_name)
        else:
            record.__dict__.setdefault('task_name', '???')
            record.__dict__.setdefault('task_id', '???')
        return ColorFormatter.format(self, record)
